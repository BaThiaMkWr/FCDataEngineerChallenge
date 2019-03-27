FROM python:2.7

MAINTAINER BaSamMaDi "bathia.mkwr@gmail.com"

COPY .  /app
WORKDIR /app

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["runserver.py"]
