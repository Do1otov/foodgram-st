FROM python:3.10.0-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN mkdir -p /app/static /app/media

ENTRYPOINT ["/entrypoint.sh"]
