# Claude Slack Bot

A general-purpose Claude AI assistant for Slack. Responds to DMs and @mentions using the Anthropic API.

---

## Quick Start

### 1. Install dependencies
```bash
cd C:\Users\kk\slack-bot
pip install -r requirements.txt
```

### 2. Fill in your `.env`
Open `.env` and replace the placeholder values:
```
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run the bot
```bash
python slack_bot.py
```

### 4. Expose it with ngrok (for local development)
```bash
ngrok http 5002
```
Copy the HTTPS URL shown (e.g. `https://abc123.ngrok-free.app`).

---

## Slack App Setup (one-time)

### Step 1 — Create the Slack App
1. Go to https://api.slack.com/apps
2. Click **Create New App** → **From scratch**
3. Name it (e.g. "Claude Assistant"), pick your workspace → **Create App**

### Step 2 — Add Bot Token Scopes
Go to **OAuth & Permissions** → **Scopes** → **Bot Token Scopes**, add:
- `chat:write`
- `app_mentions:read`
- `im:history`
- `im:read`
- `im:write`
- `channels:history` *(needed if you want channel DM reads)*

### Step 3 — Enable Events API
1. Go to **Event Subscriptions** → toggle **Enable Events** ON
2. Set **Request URL** to:
   ```
   https://<your-ngrok-url>/slack/events
   ```
   Slack will immediately verify this URL — make sure the bot is running first.
3. Under **Subscribe to bot events**, add:
   - `app_mention`
   - `message.im`
4. Click **Save Changes**

### Step 4 — Install the App
Go to **OAuth & Permissions** → **Install to Workspace** → **Allow**

Copy the **Bot User OAuth Token** (starts with `xoxb-`) into `.env`.

### Step 5 — Get the Signing Secret
Go to **Basic Information** → **App Credentials** → copy **Signing Secret** into `.env`.

---

## Using the Bot

| Action | How |
|--------|-----|
| **DM the bot** | Find the bot in Slack sidebar, send any message |
| **@mention in a channel** | Type `@Claude Assistant your question` |
| **Conversation memory** | Bot remembers the last 10 messages per user |

---

## File Structure
```
slack-bot/
├── slack_bot.py      # Flask + Slack Bolt server (port 5002)
├── .env              # Your API keys (never commit this)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Slack shows "Your URL didn't respond" | Make sure `python slack_bot.py` is running AND ngrok is active |
| Bot doesn't reply to DMs | Check `im:history` and `message.im` scopes are added |
| `KeyError: SLACK_BOT_TOKEN` | Make sure `.env` is filled in and in the same folder |
| Bot replies twice | You may have duplicate event subscriptions — check your Slack app settings |
