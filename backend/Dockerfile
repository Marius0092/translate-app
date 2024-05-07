FROM python:3.10-slim-buster

RUN apt-get update
RUN apt-get install -y curl unzip

RUN useradd -m -s /bin/bash translator
USER translator

COPY --chown=translator:translator . /opt/backend
WORKDIR /opt/backend
RUN chmod +x download_models.sh

RUN mkdir $HOME/models
WORKDIR /home/translator/models
RUN /opt/backend/download_models.sh

RUN pip install pipx
RUN python -m pipx install pdm

WORKDIR /opt/backend
RUN $HOME/.local/bin/pdm use 3.10
RUN $HOME/.local/bin/pdm install --venv in-project
RUN .venv/bin/python3.10 -c "import nltk; nltk.download('punkt')"

RUN mkdir src/translator/models
RUN .venv/bin/ct2-opus-mt-converter --model_dir $HOME/models/enit --output_dir src/translator/models/enit/enit_ctranslate2
RUN .venv/bin/ct2-opus-mt-converter --model_dir $HOME/models/iten --output_dir src/translator/models/iten/iten_ctranslate2
RUN cp /home/translator/models/enit/*spm src/translator/models/enit/
RUN cp /home/translator/models/iten/*spm src/translator/models/iten/
RUN rm -fr /home/translator/models/*

EXPOSE 5000
CMD $HOME/.local/bin/pdm start --host 172.17.0.2