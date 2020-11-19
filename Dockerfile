FROM python:3.8.3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN chmod -x /usr/src/app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]