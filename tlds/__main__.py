import dotenv
import re

# Slack imports
from slack_bolt import App, BoltResponse
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web.client import WebClient

# To avoid a log message about unhandled requests
from slack_bolt.error import BoltUnhandledRequestError

# Types
from slack_bolt.context.respond import Respond
from slack_sdk.errors import SlackApiError

from tlds.utils import Summarizer
from tlds import settings

dotenv.load_dotenv()
SLACK_BOT_TOKEN = settings.slack_bot_token
SLACK_APP_TOKEN = settings.slack_app_token


app = App(token=SLACK_BOT_TOKEN, raise_error_for_unhandled_request=True)
summarizer = Summarizer(settings.llm)


@app.shortcut("summary")
def handle_shortcut(ack, client: WebClient, shortcut: dict, respond: Respond):
    ack()
    summarizer.on_request(
        channel_id=shortcut["channel"]["id"],
        message_ts=shortcut["message"]["ts"],
        user_id=shortcut["user"]["id"],
        client=client,
        visibility="ephemeral",
    )


@app.command("/tlds")
def summarize_command(ack, client: WebClient, command: dict, respond: Respond):
    ack()
    channel_id = (command["channel_id"],)

    # Parse permalink
    # https://api.slack.com/methods/chat.getPermalink#examples
    # https://api.slack.com/methods/conversations.history#single-message
    match = re.search(r"/archives/(\w+)/p(\d+)(?:\s*)(public|ephemeral)?", command["text"])
    if not match:
        respond("Invalid permalink. Command must be in the format `/tlds <permalink> <public|ephemeral>`. If public or ephemeral is not specified, the default is ephemeral.")
        return
    channel_id = match.group(1)
    message_ts = f"{match.group(2)[:10]}.{match.group(2)[10:]}"
    visibility = match.group(3) or "ephemeral"
    
    summarizer.on_request(
        channel_id=channel_id,
        message_ts=message_ts,
        user_id=command["user_id"],
        client=client,
        visibility=visibility,
    )


# https://github.com/slackapi/bolt-python/issues/299#issuecomment-823590042
@app.error
def handle_errors(error, body, respond: Respond):
    if isinstance(error, BoltUnhandledRequestError):
        return BoltResponse(status=200, body="")
    else:
        print(f"Error: {error.response.data["error"]}")
        try:
            respond(
                "Something went wrong. If this persists, please contact <@U075RTSLDQ8>."
            )
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
        return BoltResponse(status=500, body="Something Wrong")


def main():
    global app
    SocketModeHandler(app, SLACK_APP_TOKEN).start()


if __name__ == "__main__":
    main()
