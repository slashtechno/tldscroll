import os
import dotenv
import re

# Slack imports
from slack_bolt import App, BoltResponse
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web.client import WebClient

# To avoid a log message about unhandled requests
from slack_bolt.error import BoltUnhandledRequestError

# Types
from slack_bolt.context.say import Say
from slack_bolt.context.respond import Respond
from slack_sdk.errors import SlackApiError
from tlds.utils import Summarizer


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


@app.command("/tlds")
def summarize_command(ack, client: WebClient, command: dict, respond: Respond):
    ack()
    channel_id = command["channel_id"],

    # Parse permalink
    # https://api.slack.com/methods/chat.getPermalink#examples
    # https://api.slack.com/methods/conversations.history#single-message
    match = re.search(r'/archives/(\w+)/p(\d+)', command["text"])
    if not match:
        respond("Invalid permalink")
        return
    channel_id = match.group(1)
    message_ts = f"{match.group(2)[:10]}.{match.group(2)[10:]}"

    summarizer.on_request(
        channel_id=channel_id,
        message_ts=message_ts,
        say=respond,
        client=client,
    )

# https://github.com/slackapi/bolt-python/issues/299#issuecomment-823590042    
@app.error
def handle_errors(error, body, respond):
    if isinstance(error, BoltUnhandledRequestError):
        return BoltResponse(status=200, body="")
    else:
        print(f"Error: {error.response.data["error"]}")
        try:
            respond("Something went wrong. If this persists, please contact <@U075RTSLDQ8>.")
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
        return BoltResponse(status=500, body="Something Wrong")

def main():
    global app
    SocketModeHandler(app, SLACK_APP_TOKEN).start()


if __name__ == "__main__":
    main()
