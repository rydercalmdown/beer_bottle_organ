FROM python:3.9-slim
WORKDIR /app
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./src /app
EXPOSE 5000
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "app.py"]
