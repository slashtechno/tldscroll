import os
import dotenv
# Slack imports
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler 


def main():
    dotenv.load_dotenv()
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

    if (not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN) or not (SLACK_BOT_TOKEN.startswith("xoxb-") and SLACK_APP_TOKEN .startswith("xapp-")):
        # FATA, ERRO, DEBU, or WARN for equal spacing
        print("FATA: Invalid Slack tokens")


    app = App(token=SLACK_BOT_TOKEN)
    SocketModeHandler(app, SLACK_APP_TOKEN).start()