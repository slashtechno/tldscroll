# Too Long; Didn't Scroll (TL;DS)  
A Slack bot that helps you to summarize long messages and threads.  

[![Demo](tlds-demo_2024-08-22_19-24-01.gif)](tlds-demo_2024-08-22_19-24-01.mp4)


### Features  
* Summarize messages and threads
    * Running on a top-level message will summarize the message along with its replies, if any exist  
    * Running on a reply will summarize the reply  
* Summarize messages and threads with a single click (well, two clicks)
    * Use the `Generate Summary` message action to summarize
* Customizable visibility
    * When using the `/tlds` command, you can choose whether the summary is visible to everyone or is ephemeral and only visible to you  
    * When using the `Generate summary` message action, the summary is ephemeral and only visible to you
    * When using the `Generate public summary` message action, the summary is visible to everyone
* Customizable LLM model and provider  
    * Supports [Ollama](https://ollama.com/) for local/on-premises summarization  
    * Supports OpenAI-compatible APIs for cloud-based summarization
        * Examples include [OpenAI](https://openai.com/) and [OpenRouter](https://openrouter.ai/)  
* A help command (`/tlds-help`) to show the available commands and options


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
If you have Ollama running on the host, the host can be accessed by the container by using `host.docker.internal` as the host name. For example, if Ollama is running on port `11434` (the default), setting the `base_url` to `http://host.docker.internal:11434` will allow the container to access Ollama.  
The `docker-compose.yml` file also has a commented-out section for Ollama that can be used. However, setting it up on the host or by itself can offer more flexibility. To use the Ollama section in the `docker-compose.yml` file, uncomment the section. The `base_url` should be `http://ollama:11434` in this case.  

##### Poetry  
If you want to run the server without Docker, you can use [Poetry](https://python-poetry.org/):    
```sh
poetry install
poetry run python -m tlds
```


### Usage  
1. Add the app to channel(s) where you want it to be able to summarize messages from   
2. Use the `/tlds` command or the `Generate Summary`/`Generate public summary` message actions to summarize messages and threads