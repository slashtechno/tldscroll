FROM python:3.12

LABEL org.opencontainers.image.title "Too long; didn't scroll"
LABEL org.opencontainers.image.description "Docker image for Too long, didn't scroll (TL;DS), a tool for summarizing Slack messages and threads."
# LABEL org.opencontainers.image.source ""


RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "tlds"]