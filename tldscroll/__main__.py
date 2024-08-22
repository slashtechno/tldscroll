import os
import dotenv

# Slack imports
from slack_bolt import App, BoltResponse
from slack_bolt.adapter.socket_mode import SocketModeHandler

# To avoid a log message about unhandled requests
from slack_bolt.error import BoltUnhandledRequestError

# Type hinting
from slack_sdk.web.client import WebClient
from slack_bolt.context.say import Say

from tldscroll.utils import Summarizer


# app = None
dotenv.load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

if (not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN) or not (
    SLACK_BOT_TOKEN.startswith("xoxb-") and SLACK_APP_TOKEN.startswith("xapp-")
):
    # FATA, ERRO, DEBU, or WARN for equal spacing
    print("FATA: Invalid Slack tokens")
    exit(1)


app = App(token=SLACK_BOT_TOKEN, raise_error_for_unhandled_request=True)
summarizer = Summarizer()

@app.message(":wave:")
# https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
def message_hello(message, say, client: WebClient):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")
    # This will only send a message to the user who triggered the event
    client.chat_postEphemeral(
        text="Hey there!",
        channel=message["channel"],
        user=message["user"],
    )

@app.shortcut("summary")
def handle_shortcut(ack, client: WebClient, shortcut: dict, say: Say):
    ack()
    summarizer.on_request(
        channel_id=shortcut["channel"]["id"],
        message_ts=shortcut["message"]["ts"],
        say=say,
        client=client,
    )

# https://github.com/slackapi/bolt-python/issues/299#issuecomment-823590042    
@app.error
def handle_errors(error):
    if isinstance(error, BoltUnhandledRequestError):
        return BoltResponse(status=200, body="")
    else:
        return BoltResponse(status=500, body="Something Wrong")

def main():
    global app
    SocketModeHandler(app, SLACK_APP_TOKEN).start()


if __name__ == "__main__":
    main()
