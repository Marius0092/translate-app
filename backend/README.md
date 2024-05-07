# Translator backend

## Run the server
This project is managed with [pdm](https://pdm-project.org/latest/). Please, follow the instructions
to install pdm first (preferred method: pipx). Then, install all packages with `pdm install` inside
the backend folder.
Finally, run `pdm start` to start the server. The port listened by the server can be set with the 
argument flag `-p`, e.g.: `pdm start -p 8888`.

## Using Docker
Build a docker image with `docker build -f Dockerfile . -t translator-backend:dev-cpu`
and then run the container with `docker run -p 5000:5000 translator-backend:dev-cpu`.
It will start a server that listens to POST requests in `http://localhost:5000/translate`.
