# botbor — TokenHarbor Auto-Register Bot

Automated TokenHarbor account registration, free model activation, and 9router injection.

## Features
- Auto-register via temp email
- Free model consent (`mimo-v2.5:free`)
- API key creation + testing
- 9router SQLite injection
- Batch mode (N accounts)

## Setup
```bash
git clone https://github.com/temamumtaza/ApiBor.git
cd ApiBor
pip install -r requirements.txt
```
No machine activation or runtime license key is required. After installing the
dependencies, run the bot directly with `python3 bot.py`.

## Usage
```bash
python3 bot.py                    # Interactive menu
python3 bot.py 1                  # Register 1 account
python3 bot.py 1 --no-inject      # Register without 9router inject
python3 bot.py batch 5            # Register 5 accounts
python3 bot.py batch 5 --inject   # Register 5 + inject to 9router
python3 bot.py test               # Test all API keys
python3 bot.py list               # List accounts & keys
python3 bot.py inject             # Inject all to 9router
python3 bot.py 9router            # Show 9router entries
```

## Proxy (Optional)
```bash
export BOTBOR_PROXY="http://user:pass@proxy:port"
# or add to .env file
```

## Runtime licensing
The bot does not require a license key at runtime.
