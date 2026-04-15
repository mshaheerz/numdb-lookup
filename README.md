# NumDB-Lookup

Phone Number Intelligence Tool - Look up phone number details using 6 different methods from a single colorful interactive terminal menu.

## Features

- **Interactive colorful menu** with ASCII banner and color-coded output
- **6 lookup methods** (1 offline + 5 API-based)
- **Config file** for saving API keys - set once, use forever
- **Settings portal** to manage API keys from the menu
- **Production-ready** folder structure with base class pattern

## Lookup Methods

| # | Method | API Key Required | What It Provides |
|---|--------|-----------------|------------------|
| 1 | **Normal Lookup** | No (offline) | Timezone, location, carrier, number type |
| 2 | **Truecaller API** | Yes | Caller identification and details |
| 3 | **Numverify API** | Yes | Validation, formatting, carrier, line type |
| 4 | **Abstract API** | Yes | Validation, formatting, country, carrier |
| 5 | **Veriphone API** | Yes | Verification, type, carrier, region |
| 6 | **IPQualityScore API** | Yes | Fraud scoring, carrier, abuse detection |

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

That's it! The interactive menu handles everything:

```
  ╔══════════════════════════════════════════════════╗
  |                   MAIN MENU                      |
  ╚══════════════════════════════════════════════════╝

    [1] Normal Lookup       (no API key needed)
    [2] Truecaller API      (API key: configured)
    [3] Numverify API       (API key: missing)
    [4] Abstract API        (API key: missing)
    [5] Veriphone API       (API key: missing)
    [6] IPQualityScore API  (API key: missing)
    ──────────────────────────────────────
    [7] Settings
    [8] Exit

  Enter your choice:
```

### Setting Up API Keys

1. Launch the tool: `python3 main.py`
2. Select **Settings** from the menu
3. Choose **Add / Edit API Key**
4. Select the service and paste your key
5. Keys are saved to `config.json` - you only need to do this once

### Getting API Keys

| Service | Sign Up |
|---------|---------|
| Truecaller | [developer.truecaller.com](https://developer.truecaller.com) |
| Numverify | [numverify.com](https://numverify.com) |
| Abstract API | [abstractapi.com](https://www.abstractapi.com/api/phone-validation-api) |
| Veriphone | [veriphone.io](https://veriphone.io) |
| IPQualityScore | [ipqualityscore.com](https://www.ipqualityscore.com) |

## Project Structure

```
numdb-lookup/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── config.json                # API keys (auto-created, gitignored)
├── core/
│   ├── config.py              # Config manager
│   ├── menu.py                # Interactive menu system
│   ├── display.py             # Colors, banner, formatting
│   ├── validator.py           # Phone number validation
│   └── lookups/
│       ├── base.py            # BaseLookup abstract class
│       ├── normal.py          # Offline phonenumbers lookup
│       ├── truecaller.py      # Truecaller API
│       ├── numverify.py       # Numverify API
│       ├── abstract_api.py    # Abstract API
│       ├── veriphone.py       # Veriphone API
│       └── ipqualityscore.py  # IPQualityScore API
```

## Dependencies

- `phonenumbers` - Offline phone number parsing and validation
- `requests` - HTTP client for API calls
- `colorama` - Cross-platform terminal color support

## Contributing

Feel free to contribute by submitting pull requests or opening issues.

## License

This project is licensed under the MIT License.
