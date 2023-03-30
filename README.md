# Flask URL Shortener
This is an URL Shortener Web made with Python 3 and Flask.

## Setup

The easiest way to setup this project is with Docker. Just run the following commands:

```bash
git clone https://github.com/ToniIvars/flask-url-shortener
docker build -t flask-shortener .
```

After building the docker image, you must change the **SECRET_KEY** environment variable in the **docker-compose.yml** file.
You can generate one running `python -c 'import uuid; print(uuid.uuid4().hex)'` in a terminal.

Now, to build the container, you just have to run `docker compose up -d`.

At this point, you will have the web app running, and you just have to visit [http://localhost:8000/](http://localhost:8000) to see it.

## Manual setup

You can also install this project manually. For the installation of the necessary modules, run `pip install -r requirements.txt`.

> Using a virtual environment is highly recommended

Now, you can run `gunicorn app:app -b :8000 -w 2` to launch the application, and you can visit it at [http://localhost:8000/](http://localhost:8000)
