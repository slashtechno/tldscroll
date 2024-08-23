from dynaconf import Dynaconf, Validator, ValidationError


def ollama_validator(value):
    if value is not None and settings.get("llm.openai") is None:
        return True
    return False

def openai_validator(value):
    if value is not None and settings.get("llm.ollama") is None:
        return True
    return False

settings = Dynaconf(
    envvar_prefix="TLDS",
    load_dotenv=True,
    settings_files=["settings.toml", ".secrets.toml"],
    merge_enabled=True,
)
settings.validators.register(
        validators=[
        Validator(
            "slack_bot_token",
            must_exist=True,
            condition=lambda x: x.startswith("xoxb-"),
            messages={"condition": "Must start with 'xoxb-'"},
        ),
        Validator(
            "slack_app_token",
            must_exist=True,
            condition=lambda x: x.startswith("xapp-"),
            messages={"condition": "Must start with 'xapp-'"},
        ),
        Validator("llm.ollama", condition=ollama_validator, messages={"condition": "Either llm.ollama or llm.openai must be set. Only one can be set."}),
        Validator("llm.openai", condition=openai_validator, messages={"condition": "Either llm.ollama or llm.openai must be set. Only one can be set."}),
    ],
)

settings.validators.validate()
