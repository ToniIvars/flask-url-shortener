FROM python:slim

WORKDIR /app
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["gunicorn", "-b", ":8000", "-w", "2","app:app"]