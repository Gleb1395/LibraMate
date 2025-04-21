FROM python:3.10.11-slim

RUN apt update

RUN mkdir "/libra"

WORKDIR /libra

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

COPY ./commands ./commands

RUN python -m pip install --upgrade & pip install -r ./requirements.txt

CMD ["bash"]