# Fuller Temperature vs Worker Efficiency App
This app is to be used as an interative tool in order to determine construction worker efficiency as it realtes to temperature.  From time to time it may be down due to development but serves a s ainstrument for constuction companies to help plan their best use for labourers for outdoor construction in teh Ottawa are. 







## For those of you who want to use the repo as a streamlit template

Example on how to run and develop a [streamlit](https://github.com/streamlit/streamlit) application inside docker.

<p align="center">
<img src="/img/screenshot.png" alt="streamlit in docker">
</p>

## Installation

```bash
git clone https://github.com/iwpnd/streamlit-docker-example.git
cd steamlit-docker-example

docker-compose up -d --build
```

The container will start in detached mode and can now be accessed via [localhost:8501](http://localhost:8501). Whenever you change the app/main.py the steamlit application will update too. If you want to build upon that example, just add your dependencies to the Dockerfile and rebuild the image using docker-compose.

After you are done, and you want to tear down the application, either

```bash
docker-compose stop
```

to stop the application, or use 

```bash
docker-compose down --rmi all
```

to stop the application, remove the stopped containers and optionally `--rmi all` / remove all images associated in the docker-compose.yml file.