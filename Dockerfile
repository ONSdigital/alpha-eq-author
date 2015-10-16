FROM python:2.7.10

RUN mkdir /opt/eq-author
ADD . /opt/eq-author
RUN pip install -r /opt/eq-author/requirements.txt
WORKDIR /opt/eq-author

ENV SURVEY_RUNNER_URL=http://127.0.0.1:8080/
ENV USERNAME=author
ENV PASSWORD=password
ENV DB_HOST=127.0.0.1
ENV DB_PORT=5432
ENV DB_NAME=author
ENV DATABASE_URL=postgres://$USERNAME:$PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME

EXPOSE 8000

ENTRYPOINT sleep 10 && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
