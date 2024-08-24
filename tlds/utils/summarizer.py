from typing import Literal
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Types
# https://github.com/cdgriffith/Box
from dynaconf.utils.boxing import DynaBox
from slack_sdk.web.client import WebClient
from slack_sdk.errors import SlackApiError


class Summarizer:
    def __init__(self, llm: DynaBox):
        model = llm.model if llm.model is not None else "llama3.1:8b"

        if llm.get("ollama") is not None and llm.get("openai") is None:
            self._llm = ChatOllama(model=model, base_url=llm.ollama.base_url)
        elif llm.get("openai") is not None and llm.get("ollama") is None:
            self._llm = ChatOpenAI(
                model=model,
                api_key=llm.openai.api_key,
                base_url=llm.openai.base_url,
            )
        else:
            raise ValueError(
                "Either llm.ollama or llm.openai must be set. Only one can be set."
            )

    def summarize(self, messages: list, bot_user_id: str, client: WebClient) -> str:
        """
        Summarize a conversation thread.
        """

        # https://python.langchain.com/v0.1/docs/modules/model_io/prompts/quick_start/#lcel
        # Create a message history for the conversation
        context_messages = [
            (
                "system",
                # "Summarize the messages in this conversation. Only output the summary. To mention a user, use <@user_id>. If there's only one message in the conversation, just summarize that message.",
                "Summarize the messages in this conversation. Only output the summary. To mention a user, use <@user_id> (Slack syntax). Even if there's only one message in the conversation, try to provide a summary of that message so that someone just reading the summary can understand the major points of the conversation (or standalone message). If you cannot retrieve the user ID, don't try mentioning the user as it most likely means it's an app/bot message.",
            ),
        ]
        for m in messages:
            try:
                user = m["user"]
            except KeyError:
                try: 
                    bot = client.bots_info(
                        bot=m["bot_id"],
                    )
                    user = bot.data["bot"]["user_id"] 
                except KeyError:
                    user = "(UNABLE TO RETRIEVE USER ID)"
            if user == bot_user_id:
                continue
            print(f"{user}: {m['text']}")
            context_messages.append(("user", f"<@{user}>: {m['text']}"))

        prompt_template = ChatPromptTemplate.from_messages(context_messages)

        chain = prompt_template | self._llm | StrOutputParser()

        return chain.invoke({})

    def on_request(
        self, channel_id: str, message_ts: str, user_id: str, client: WebClient, visibility: Literal["public", "ephemeral"] = "public"
    ):
        """
        Summarize a message, or thread, given a channel ID and message timestamp.
        If the message is in a thread, only the message will be summarized.
        If the message is a top-level message, the message and all replies will be summarized.

        The bot ignores its own messages when summarizing.
        """
        try:
            replies = client.conversations_replies(
            channel=channel_id,
            ts=message_ts,
        )
        except SlackApiError as e:
            if e.response.data["error"] == "not_in_channel":
                dm = client.conversations_open(users=user_id).data["channel"]["id"]
                client.chat_postEphemeral(
                    channel=dm,
                    text=f"You tried to summarize a message in <#{channel_id}>, but I don't have access to that channel. Please invite me to the channel and try again.",
                    user=user_id,
                )
                return
            raise e
        # messages = []
        # for m in replies.data["messages"]:
        # print(f"{m['user']}: {m['text']}")
        # messages.append(f"<@{m['user']}>: {m['text']}")
        # say("Summary of the thread:\n" + "\n".join(messages), thread_ts=shortcut["message"]["ts"])

        # Get the bot username so it can be ignored in the summary
        bot_user_id = client.auth_test().data["user_id"]

        summary = self.summarize(
            messages=replies.data["messages"], bot_user_id=bot_user_id, client=client
        )
        print(f"Summary: {summary}")
        
        if visibility == "public":
            link = client.chat_getPermalink(
                channel=channel_id,
                message_ts=message_ts,
            )
            client.chat_postMessage(
                channel=channel_id,
                text=f"Summary of <{link.data['permalink']}|the message/thread> requested by <@{user_id}>:\n{summary}",
                thread_ts=message_ts,
                mrkdwn=True,
            )
        else:
            # From the docs: "Ephemeral messages in threads are only shown if there is already an active thread.""
            kwargs_to_pass = {
                "channel": channel_id,
                "text": summary,
                "user": user_id,
            }

            if len(replies.data["messages"]) == 1:
                client.chat_postEphemeral(
                    **kwargs_to_pass,
                )
            else: 
                kwargs_to_pass["thread_ts"] = message_ts
                client.chat_postEphemeral(
                    **kwargs_to_pass,
                )
