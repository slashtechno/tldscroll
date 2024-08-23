# Too Long; Didn't Scroll (TL;DS)  
A Slack bot that helps you to summarize long messages and threads.  

[![Demo](tlds-demo_2024-08-22_19-24-01.gif)](tlds-demo_2024-08-22_19-24-01.mp4)


### Some more details  
TL;DS uses an Llama 3.1 to summarize long messages and threads. It can be used as a [message action](https://api.slack.com/interactivity/shortcuts#message) or as a [command](https://slack.com/help/articles/360057554553-Use-shortcuts-to-take-actions-in-Slack).  

### Setup   
1. Create a new Slack app at [api.slack.com/apps](https://api.slack.com/apps)
2. Use the `manifest.yml` file to create it  
3. Install the app to your workspace  
4. Clone the repository  
<!-- Even though .secrets.toml may be better, .env can easily be loaded by Docker Compose -->
5. Copy the `example.env` file to `.env` and fill in the values
    * Alternatively, you can use `.secrets.toml` and `settings.toml`  
    * For more information, check the `example.*.toml` files  

#### Running the server  
##### Docker 
Run the following command to build and run the Docker container:  
```sh
docker-compose up
```  
If you want to run the container in the background, use the `-d` flag:  
```sh
docker-compose up -d
```
##### Poetry  
If you want to run the server without Docker, you can use [Poetry](https://python-poetry.org/):    
```sh
poetry install
poetry run python -m tlds
```


### Usage  
1. Add the app to channel(s) where you want it to be able to summarize messages from   
2. Use the `/tlds` command or the "Summarize" message action to summarize messages  