FROM python:3.12-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app.py ./
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
