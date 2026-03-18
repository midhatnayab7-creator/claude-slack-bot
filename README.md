# Claude Slack Bot

AI-powered Slack bot that responds to DMs and @mentions using the **Anthropic Claude API**. Built with Python, Flask, and Slack Bolt.

---

## Features

- **DM Conversations** — Send a direct message to the bot and get intelligent AI responses
- **@Mention Support** — Mention the bot in any channel to ask questions
- **Conversation Memory** — Remembers the last 10 messages per user for context-aware replies
- **Threaded Replies** — Responds in threads when mentioned in channels
- **Slack-Formatted Output** — Responses use bold, italic, and bullet points for clean readability
- **Health Check Endpoint** — Built-in `/health` route for monitoring
- **Render-Ready** — Includes `Procfile` and `render.yaml` for one-click cloud deployment

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core language |
| **Flask** | Web server |
| **Slack Bolt** | Slack event handling |
| **Anthropic API** | Claude AI (claude-sonnet-4-6) |
| **python-dotenv** | Environment variable management |

---

## How It Works

```
User sends message in Slack (DM or @mention)
        ↓
Slack forwards event to Flask server (/slack/events)
        ↓
Bot retrieves user's conversation history (last 10 messages)
        ↓
Sends message + history to Claude API
        ↓
Claude generates a response
        ↓
Bot replies in Slack (in thread if @mentioned)
```

---

## Usage

| Action | How |
|--------|-----|
| **DM the bot** | Find the bot in Slack sidebar → send any message |
| **@mention in a channel** | Type `@Claude Assistant your question` |
| **Conversation memory** | Bot remembers the last 10 messages per user |

---

## Author

**Midhat Nayab** — [GitHub](https://github.com/midhatnayab7-creator)

---

Built with Flask & Anthropic Claude API
