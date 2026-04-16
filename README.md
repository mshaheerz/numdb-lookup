# NumDB-Lookup

Phone Number Intelligence Tool v3.0 - The most comprehensive phone number OSINT toolkit. 21 lookup methods, 11 free (no API key), advanced techniques including Google dorking, social media probing, breach detection, ENUM/DNS, disposable number detection, and more.

## Features

- **21 lookup methods** (11 free + 10 API-based)
- **Run All Lookups** - comprehensive scan with a single command
- **Interactive colorful menu** with ASCII banner and color-coded output
- **OSINT techniques** - Google dorking, social media checks, email recovery probes
- **Advanced analysis** - ENUM/DNS, VoIP detection, disposable number detection
- **Breach data** - check if number appears in data leaks
- **HLR lookups** - real-time network and portability status
- **Fraud scoring** - spam, scam, and abuse detection
- **Geolocation** - latitude/longitude coordinates via OpenStreetMap
- **Country registry** - DNC lists, telecom regulators, complaint URLs
- **Config file** for saving API keys - set once, use forever

## Lookup Methods

### Free (No API Key Needed)

| # | Method | What It Provides |
|---|--------|------------------|
| 1 | **Normal Lookup** | 22 fields: all formats (E.164, National, RFC3966), country details, carrier, timezone, area code, subscriber number, validation reason |
| 2 | **Geolocation Lookup** | Latitude, longitude, full address, bounding box via OpenStreetMap Nominatim |
| 3 | **Google Dorking (OSINT)** | 8 Google dork URLs: social media, paste sites, documents, forums, spam reports, messaging groups, classifieds |
| 4 | **Social Media Check** | Live probes for WhatsApp, Telegram, Viber, Skype + lookup URLs for Truecaller, Sync.me, Facebook |
| 5 | **Spam/Reputation Check** | Probes Nomorobo, ShouldIAnswer, Tellows + manual check URLs |
| 6 | **Web Presence Scanner** | 20+ URLs across people search, social platforms, business directories, breach databases |
| 7 | **OVH Telecom Scanner** | OVH VoIP range detection, VoIP provider matching, telecom regulator links |
| 8 | **Disposable/Virtual Detection** | Detects Google Voice, TextNow, Burner, Twilio, 40+ virtual providers with risk scoring |
| 9 | **Email Recovery Probe** | Probes Microsoft, Apple, Google, Twitter/X, Instagram to discover linked accounts |
| 10 | **ENUM/DNS Lookup** | ENUM NAPTR records, SIP/VoIP endpoint discovery, multi-root DNS check |
| 11 | **DNC & Country Registry** | Do Not Call registry, telecom regulator, emergency numbers, portability info for 10+ countries |

### API-Based

| # | Method | API Key | What It Provides |
|---|--------|---------|------------------|
| 12 | **Truecaller API** | `truecaller` | Caller name, profile, email, badges, photo |
| 13 | **Numverify API** | `numverify` | Validation, formatting, carrier, line type, location |
| 14 | **Abstract API** | `abstract_api` | Validation, formatting, country, carrier |
| 15 | **Veriphone API** | `veriphone` | Verification, E.164 format, type, carrier, region |
| 16 | **IPQualityScore API** | `ipqualityscore` | Fraud score, active/VOIP/prepaid flags, spam/abuse detection |
| 17 | **NumLookupAPI** | `numlookupapi` | Carrier, caller info, line type, country |
| 18 | **Telnyx Number Lookup** | `telnyx` | HLR data, MCC/MNC, caller name, ported status, city/state |
| 19 | **Neutrino API** | `neutrino` | HLR status, current/original/ported network, roaming info |
| 20 | **LeakCheck (Breach Data)** | `leakcheck` | Data breach check, breach count, sources, associated emails/usernames |
| 21 | **CNAM Lookup** | `opencnam` | Caller Name database lookup (US/Canada) |

## Installation

```bash
git clone https://github.com/mshaheerz/numdb-lookup.git
cd numdb-lookup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to Run

```bash
python3 main.py
```

The interactive menu handles everything:

```
  ╔══════════════════════════════════════════════════╗
  |                   MAIN MENU                      |
  ╚══════════════════════════════════════════════════╝

    [1]  Normal Lookup              (no API key needed)
    [2]  Geolocation Lookup         (no API key needed)
    [3]  Truecaller API             (API key: configured)
    [4]  Numverify API              (API key: configured)
    [5]  Abstract API               (API key: missing)
    [6]  Veriphone API              (API key: missing)
    [7]  IPQualityScore API         (API key: missing)
    [8]  NumLookupAPI               (API key: missing)
    [9]  Telnyx Number Lookup       (API key: missing)
    [10] Neutrino API               (API key: missing)
    [11] LeakCheck (Breach Data)    (API key: missing)
    [12] CNAM Lookup                (API key: missing)
    [13] Google Dorking (OSINT)     (no API key needed)
    [14] Social Media Check         (no API key needed)
    [15] Spam/Reputation Check      (no API key needed)
    [16] Web Presence Scanner       (no API key needed)
    [17] OVH Telecom Scanner        (no API key needed)
    [18] Disposable/Virtual Detection (no API key needed)
    [19] Email Recovery Probe       (no API key needed)
    [20] ENUM/DNS Lookup            (no API key needed)
    [21] DNC & Country Registry     (no API key needed)
    ──────────────────────────────────────────────────
    [22] Run All Lookups            (comprehensive scan)
    [23] Settings
    [24] Exit

  Enter your choice:
```

## Run All Lookups

Option **22** runs every configured lookup at once and displays:
- A colored summary table showing which lookups succeeded, failed, or were skipped
- Individual result tables for each successful lookup
- Final stats (succeeded / failed / skipped)

## Setting Up API Keys

1. Launch the tool: `python3 main.py`
2. Select **Settings** from the menu
3. Choose **Add / Edit API Key**
4. Select the service and paste your key
5. Keys are saved to `config.json` - you only need to do this once

> **Note:** Neutrino API requires a compound key in format `userid|apikey`
> CNAM (OpenCNAM) requires format `account_sid|auth_token`

## Getting API Keys

| Service | Sign Up | Free Tier |
|---------|---------|-----------|
| Truecaller | [developer.truecaller.com](https://developer.truecaller.com) | Limited |
| Numverify | [numverify.com](https://numverify.com) | 100 req/month |
| Abstract API | [abstractapi.com](https://www.abstractapi.com/api/phone-validation-api) | 100 req/month |
| Veriphone | [veriphone.io](https://veriphone.io) | 1000 req/month |
| IPQualityScore | [ipqualityscore.com](https://www.ipqualityscore.com) | 5000 req/month |
| NumLookupAPI | [numlookupapi.com](https://numlookupapi.com) | 100 req/month |
| Telnyx | [telnyx.com](https://telnyx.com) | Sign-up credit |
| Neutrino API | [neutrinoapi.net](https://www.neutrinoapi.net) | 50 req/day |
| LeakCheck | [leakcheck.io](https://leakcheck.io) | Limited free |
| OpenCNAM | [opencnam.com](https://www.opencnam.com) | Limited free |

## Project Structure

```
numdb-lookup/
├── main.py                          # Entry point
├── requirements.txt                 # Dependencies
├── config.json                      # API keys (auto-created, gitignored)
├── core/
│   ├── config.py                    # Config manager with auto-migration
│   ├── menu.py                      # Interactive menu + Run All Lookups
│   ├── display.py                   # Colors, banner, formatting, summary table
│   ├── validator.py                 # Phone number validation
│   └── lookups/
│       ├── base.py                  # BaseLookup abstract class
│       ├── normal.py                # Offline phonenumbers lookup (22 fields)
│       ├── geocoding.py             # Lat/Lng via OpenStreetMap Nominatim
│       ├── truecaller.py            # Truecaller API
│       ├── numverify.py             # Numverify API
│       ├── abstract_api.py          # Abstract API
│       ├── veriphone.py             # Veriphone API
│       ├── ipqualityscore.py        # IPQualityScore API
│       ├── numlookupapi.py          # NumLookupAPI
│       ├── telnyx.py                # Telnyx HLR/Number Lookup
│       ├── neutrino.py              # Neutrino API (HLR + validation)
│       ├── leakcheck.py             # LeakCheck breach data
│       ├── cnam.py                  # CNAM caller name database
│       ├── google_dork.py           # Google dorking OSINT
│       ├── social_media.py          # Social media presence check
│       ├── reputation.py            # Spam/reputation check
│       ├── web_presence.py          # Web presence scanner
│       ├── ovh.py                   # OVH VoIP telecom scanner
│       ├── disposable.py            # Disposable/virtual number detection
│       ├── email_recovery.py        # Email recovery probe
│       ├── enum_dns.py              # ENUM/DNS VoIP lookup
│       └── dnc_registry.py          # DNC & country-specific registry
```

## Dependencies

- `phonenumbers` - Offline phone number parsing and validation
- `requests` - HTTP client for API calls
- `colorama` - Cross-platform terminal color support

## Contributing

Feel free to contribute by submitting pull requests or opening issues.

## License

This project is licensed under the MIT License.
