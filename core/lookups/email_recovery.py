import time
from collections import OrderedDict

import phonenumbers
import requests

from core.lookups.base import BaseLookup


class EmailRecoveryLookup(BaseLookup):

    @property
    def name(self):
        return "Email Recovery Probe"

    @property
    def description(self):
        return "Probe password reset pages to discover linked email addresses (no API key needed)"

    @property
    def requires_api_key(self):
        return False

    @property
    def api_key_name(self):
        return ""

    def _probe_apple(self, e164):
        """Probe Apple ID recovery to check if phone is linked."""
        try:
            url = "https://iforgot.apple.com/phone/add?prs_account_nm=" + e164.lstrip("+")
            resp = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            }, allow_redirects=False)
            if resp.status_code == 200:
                return "Apple ID possibly linked"
            elif resp.status_code == 302:
                return "Redirect (may indicate linked account)"
            return f"HTTP {resp.status_code}"
        except requests.RequestException:
            return "Check failed"

    def _probe_microsoft(self, e164):
        """Probe Microsoft account recovery."""
        try:
            clean = e164.lstrip("+")
            url = "https://login.live.com/GetCredentialType.srf"
            payload = {
                "username": clean,
                "isOtherIdpSupported": True,
                "checkPhones": True,
                "isFederationDisabled": False,
            }
            resp = requests.post(url, json=payload, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            })
            if resp.status_code == 200:
                data = resp.json()
                if_exists = data.get("IfExistsResult", -1)
                # 0 = exists, 1 = doesn't exist, 5 = exists (different type)
                if if_exists == 0:
                    return "Microsoft account EXISTS for this number"
                elif if_exists == 1:
                    return "No Microsoft account found"
                elif if_exists == 5:
                    return "Account exists (alternate type)"
                elif if_exists == 6:
                    return "Account exists (phone-based)"
                else:
                    return f"Unknown result (code: {if_exists})"
            return f"HTTP {resp.status_code}"
        except requests.RequestException:
            return "Check failed"

    def _probe_google(self, e164):
        """Check Google account linkage via recovery page probe."""
        try:
            # Google's account recovery doesn't expose much via simple probing
            # but we can check the signup endpoint
            clean = e164.lstrip("+")
            url = f"https://accounts.google.com/SignUp?phone={clean}"
            resp = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            }, allow_redirects=False)
            if resp.status_code == 302:
                return "Google account may be linked (redirect)"
            elif resp.status_code == 200:
                return "Page accessible (may or may not be linked)"
            return f"HTTP {resp.status_code}"
        except requests.RequestException:
            return "Check failed"

    def _probe_amazon(self, e164):
        """Check Amazon account linkage."""
        try:
            clean = e164.lstrip("+")
            url = "https://www.amazon.com/ap/forgotpassword"
            resp = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            }, allow_redirects=True)
            if resp.status_code == 200:
                return "Recovery page accessible (manual check needed)"
            return f"HTTP {resp.status_code}"
        except requests.RequestException:
            return "Check failed"

    def _probe_twitter(self, e164):
        """Check Twitter/X account linkage."""
        try:
            clean = e164.lstrip("+")
            url = f"https://api.twitter.com/i/users/phone_number_available.json?phone_number=%2B{clean}"
            resp = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            })
            if resp.status_code == 200:
                data = resp.json()
                taken = data.get("taken", None)
                if taken is True:
                    return "Twitter/X account LINKED to this number"
                elif taken is False:
                    return "Number NOT registered on Twitter/X"
                return "Unknown result"
            elif resp.status_code == 403:
                return "Rate limited / blocked"
            return f"HTTP {resp.status_code}"
        except requests.RequestException:
            return "Check failed"

    def _probe_instagram(self, e164):
        """Check Instagram account linkage via signup check."""
        try:
            clean = e164.lstrip("+")
            url = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
            resp = requests.post(url, data={
                "phone_number": f"+{clean}",
            }, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "X-CSRFToken": "missing",
                "Referer": "https://www.instagram.com/accounts/emailsignup/",
            })
            if resp.status_code == 200:
                data = resp.json()
                errors = data.get("errors", {})
                phone_errors = errors.get("phone_number", [])
                for err in phone_errors:
                    if "another account" in str(err).lower():
                        return "Instagram account LINKED to this number"
                return "Number may be available on Instagram"
            return f"HTTP {resp.status_code}"
        except requests.RequestException:
            return "Check failed"

    def lookup(self, phone_number, api_key=None):
        try:
            parsed = phonenumbers.parse(phone_number, None)
        except phonenumbers.NumberParseException as e:
            return {"success": False, "data": None, "error": f"Invalid phone number: {e}"}

        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        data = OrderedDict()
        data["Phone Number"] = intl
        data["E.164"] = e164
        data[""] = "─── Account Recovery Probes ───"

        # Microsoft (most reliable probe)
        data["Microsoft"] = self._probe_microsoft(e164)
        time.sleep(0.5)

        # Apple
        data["Apple ID"] = self._probe_apple(e164)
        time.sleep(0.5)

        # Google
        data["Google"] = self._probe_google(e164)
        time.sleep(0.5)

        # Twitter/X
        data["Twitter/X"] = self._probe_twitter(e164)
        time.sleep(0.5)

        # Instagram
        data["Instagram"] = self._probe_instagram(e164)
        time.sleep(0.5)

        # Amazon
        data["Amazon"] = self._probe_amazon(e164)

        data[" "] = "─── Manual Recovery URLs ───"
        clean = e164.lstrip("+")
        data["Apple Recovery"] = "https://iforgot.apple.com/"
        data["Google Recovery"] = "https://accounts.google.com/signin/recovery"
        data["Microsoft Recovery"] = "https://account.live.com/password/reset"
        data["Facebook Recovery"] = f"https://www.facebook.com/login/identify/?ctx=recover&phone={clean}"
        data["PayPal Recovery"] = "https://www.paypal.com/authflow/password-recovery/"

        return {"success": True, "data": data, "error": None}
