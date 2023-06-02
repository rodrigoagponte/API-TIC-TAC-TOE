FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ ./

CMD ["/usr/local/bin/python", "manage.py", "runserver", "0.0.0.0:8080"]
