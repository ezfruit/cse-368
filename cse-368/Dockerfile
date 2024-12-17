FROM python:3.12.6

ENV HOME /app
WORKDIR /app

COPY campus_living_info.csv ub_campus_paragraphs.csv ub_events.csv  ./
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8080

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
RUN pip install spacy
RUN python -m spacy download en_core_web_sm
CMD /wait && python -u server.py