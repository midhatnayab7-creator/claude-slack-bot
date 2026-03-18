import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import anthropic

load_dotenv()

# --- Clients ---
slack_app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)
anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = (
    "You are a helpful AI assistant in Slack. Be concise, friendly, and clear. "
    "Format responses for Slack (use *bold*, _italic_, bullet points with •)."
)

# Per-user conversation history: { user_id: [{"role": ..., "content": ...}, ...] }
conversation_history: dict[str, list] = {}
MAX_HISTORY = 10


def get_claude_reply(user_id: str, user_text: str) -> str:
    history = conversation_history.setdefault(user_id, [])
    history.append({"role": "user", "content": user_text})

    response = anthropic_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    reply = response.content[0].text

    history.append({"role": "assistant", "content": reply})

    # Keep only the last MAX_HISTORY messages
    if len(history) > MAX_HISTORY:
        conversation_history[user_id] = history[-MAX_HISTORY:]

    return reply


# --- Event: @mention in any channel ---
@slack_app.event("app_mention")
def handle_mention(event, say):
    user_id = event["user"]
    # Strip the bot mention prefix (<@BOTID>) from the text
    text = event.get("text", "")
    # Remove leading mention token
    if "<@" in text:
        text = text.split(">", 1)[-1].strip()

    reply = get_claude_reply(user_id, text)
    # Reply in thread if there is one, otherwise start one
    thread_ts = event.get("thread_ts") or event.get("ts")
    say(text=reply, thread_ts=thread_ts)


# --- Event: Direct Message ---
@slack_app.event("message")
def handle_dm(event, say):
    # Ignore bot messages and message edits
    if event.get("bot_id") or event.get("subtype"):
        return

    # Only handle DMs (channel_type == "im")
    if event.get("channel_type") != "im":
        return

    user_id = event["user"]
    text = event.get("text", "").strip()
    if not text:
        return

    reply = get_claude_reply(user_id, text)
    say(text=reply)


# --- Flask adapter ---
flask_app = Flask(__name__)
handler = SlackRequestHandler(slack_app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "bot": "Claude Slack Bot", "port": 5002}, 200


if __name__ == "__main__":
    print("=" * 50)
    print("  Claude Slack Bot running on port 5002")
    print("  Endpoint: POST /slack/events")
    print("=" * 50)
    port = int(os.environ.get("PORT", 5002))
    flask_app.run(host="0.0.0.0", port=port, debug=False)
