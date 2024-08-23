from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Type hints
# https://github.com/cdgriffith/Box
from dynaconf.utils.boxing import DynaBox
from slack_bolt.context.say import Say
from slack_sdk.web.client import WebClient


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
            raise ValueError("Either llm.ollama or llm.openai must be set. Only one can be set.")
    def summarize(self, messages: list, bot_user_id: str) -> str:
        """
        Summarize a conversation thread.
        """

        # https://python.langchain.com/v0.1/docs/modules/model_io/prompts/quick_start/#lcel
        # Create a message history for the conversation
        context_messages = [
            (
                "system",
                "Summarize the messages in this conversation. Only output the summary. To mention a user, use <@user_id>. If there's only one message in the conversation, just summarize that message.",
            ),
        ]
        for m in messages:            
            if m["user"] == bot_user_id:  
                continue
            print(f"{m['user']}: {m['text']}")
            context_messages.append(("user", f"<@{m['user']}>: {m['text']}"))

        prompt_template = ChatPromptTemplate.from_messages(context_messages)
    

        chain = prompt_template | self._llm | StrOutputParser()

        return chain.invoke({})
    
    def on_request(self, channel_id: str, message_ts: str, say: Say, client: WebClient):
        """
        Summarize a message, or thread, given a channel ID and message timestamp.
        If the message is in a thread, only the message will be summarized.
        If the message is a top-level message, the message and all replies will be summarized.

        The bot ignores its own messages when summarizing.
        """
        replies = client.conversations_replies(
            channel=channel_id,
            ts=message_ts,
        )
        # messages = []
        # for m in replies.data["messages"]:
            # print(f"{m['user']}: {m['text']}")
            # messages.append(f"<@{m['user']}>: {m['text']}")
        # say("Summary of the thread:\n" + "\n".join(messages), thread_ts=shortcut["message"]["ts"])
        
        
        # Get the bot username so it can be ignored in the summary
        bot_user_id = client.auth_test().data["user_id"]

        summary = self.summarize(messages=replies.data["messages"], bot_user_id=bot_user_id)
        print(f"Summary: {summary}")
        say(summary, thread_ts=message_ts)
