import subprocess
from collections import OrderedDict

import phonenumbers

from core.lookups.base import BaseLookup


class ENUMLookup(BaseLookup):

    @property
    def name(self):
        return "ENUM/DNS Lookup"

    @property
    def description(self):
        return "ENUM DNS lookup for VoIP SIP/NAPTR records (no API key needed)"

    @property
    def requires_api_key(self):
        return False

    @property
    def api_key_name(self):
        return ""

    def _build_enum_domain(self, e164):
        """Convert E.164 number to ENUM domain.
        +14155552671 -> 1.7.6.2.5.5.5.5.1.4.1.e164.arpa
        """
        digits = e164.lstrip("+")
        reversed_digits = ".".join(reversed(digits))
        return f"{reversed_digits}.e164.arpa"

    def _dns_lookup(self, domain, record_type="NAPTR"):
        """Perform DNS lookup using system dig/nslookup."""
        results = []

        # Try dig first
        try:
            cmd = ["dig", "+short", domain, record_type]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if proc.returncode == 0 and proc.stdout.strip():
                for line in proc.stdout.strip().split("\n"):
                    if line.strip():
                        results.append(line.strip())
                return results
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Fallback to nslookup
        try:
            cmd = ["nslookup", f"-type={record_type}", domain]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if proc.returncode == 0 and proc.stdout.strip():
                for line in proc.stdout.strip().split("\n"):
                    line = line.strip()
                    if record_type.lower() in line.lower() or "service" in line.lower():
                        results.append(line)
                return results
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Fallback to Python socket-based DNS
        try:
            import socket
            answers = socket.getaddrinfo(domain, None)
            for answer in answers:
                results.append(str(answer))
            return results
        except (socket.gaierror, Exception):
            pass

        return results

    def _check_enum_providers(self, e164):
        """Check against known ENUM providers."""
        digits = e164.lstrip("+")
        reversed_digits = ".".join(reversed(digits))

        # List of ENUM roots to check
        enum_roots = [
            ("e164.arpa", "ITU Official ENUM"),
            ("e164.org", "Public ENUM"),
            ("e164.info", "ENUM Info"),
            ("nrenum.net", "NRE ENUM (US)"),
            ("enum.opentelecoms.net", "Open Telecoms ENUM"),
        ]

        results = OrderedDict()
        for root, label in enum_roots:
            domain = f"{reversed_digits}.{root}"
            records = self._dns_lookup(domain, "NAPTR")
            if records:
                results[label] = "; ".join(records[:3])
            else:
                results[label] = "No records"

        return results

    def lookup(self, phone_number, api_key=None):
        try:
            parsed = phonenumbers.parse(phone_number, None)
        except phonenumbers.NumberParseException as e:
            return {"success": False, "data": None, "error": f"Invalid phone number: {e}"}

        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        enum_domain = self._build_enum_domain(e164)

        data = OrderedDict()
        data["Phone Number"] = intl
        data["E.164"] = e164
        data["ENUM Domain"] = enum_domain

        # Primary ENUM lookup (e164.arpa)
        data[""] = "─── NAPTR Records ───"
        naptr_records = self._dns_lookup(enum_domain, "NAPTR")
        if naptr_records:
            data["NAPTR Found"] = "Yes"
            for i, record in enumerate(naptr_records[:5], 1):
                data[f"Record {i}"] = record

            # Parse SIP/IAX URIs from NAPTR records
            sip_uris = []
            for record in naptr_records:
                if "sip:" in record.lower() or "sips:" in record.lower():
                    sip_uris.append(record)
                elif "iax:" in record.lower():
                    sip_uris.append(record)

            if sip_uris:
                data["VoIP Endpoints"] = "; ".join(sip_uris[:3])
                data["VoIP Registered"] = "Yes - SIP/IAX endpoint found"
            else:
                data["VoIP Endpoints"] = "None found in records"
        else:
            data["NAPTR Found"] = "No"
            data["Note"] = "No ENUM records - number not registered in DNS"

        # Check multiple ENUM roots
        data[" "] = "─── Multi-Root ENUM Check ───"
        provider_results = self._check_enum_providers(e164)
        for label, result in provider_results.items():
            data[label] = result

        # Additional DNS checks
        data["  "] = "─── Additional DNS ───"

        # SRV record check
        srv_records = self._dns_lookup(f"_sip._udp.{enum_domain}", "SRV")
        data["SIP SRV Records"] = "; ".join(srv_records[:3]) if srv_records else "None"

        # TXT record check
        txt_records = self._dns_lookup(enum_domain, "TXT")
        data["TXT Records"] = "; ".join(txt_records[:3]) if txt_records else "None"

        return {"success": True, "data": data, "error": None}
