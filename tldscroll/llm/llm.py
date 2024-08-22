from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class Summarizer:
    def __init__(self, model_name: str = "llama3.1:8b"):
        # self.model = Ollama(model_name=model_name)
        self._llm = ChatOllama(model=model_name)

    def summarize(self, messages: list) -> str:
        # https://python.langchain.com/v0.1/docs/modules/model_io/prompts/quick_start/#lcel

        context_messages = [
            (
                "system",
                "Summarize the messages in this conversation. Only output the summary. To mention a user, use <@user_id>. If there's only one message, just summarize it.",
            ),
        ]
        for m in messages:
            context_messages.append(("user", f"<@{m['user']}>: {m['text']}"))

        prompt_template = ChatPromptTemplate.from_messages(context_messages)
    

        chain = prompt_template | self._llm | StrOutputParser()

        return chain.invoke({})