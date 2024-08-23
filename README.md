# Too Long; Didn't Scroll (TL;DS)  
A Slack bot that helps you to summarize long messages and threads.  

[![Demo](tldscroll-demo_2024-08-22_19-24-01.gif)](tldscroll-demo_2024-08-22_19-24-01.mp4)


### Some more details  
TL;DS uses an Llama 3.1 to summarize long messages and threads. It can be used as a [message action](https://api.slack.com/interactivity/shortcuts#message) or as a [command](https://slack.com/help/articles/360057554553-Use-shortcuts-to-take-actions-in-Slack).  

### Installation and Setup  
1. Create a new Slack app at [api.slack.com/apps](https://api.slack.com/apps)
2. Use the `manifest.yml` file to create it  
3. Install the app to your workspace  
4. Clone the repository  
5. Ensuring you have [Poetry](https://python-poetry.org/) installed, run `poetry install`  
6. Copy the `example.env` file to `.env` and fill in the values
7. Run `poetry run python -m tldscroll`  

### Usage  
1. Add the app to channel(s) where you want it to be able to summarize messages from   
2. Use the `/tldscroll` command or the "Summarize" message action to summarize messages  