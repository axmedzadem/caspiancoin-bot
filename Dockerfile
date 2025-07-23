FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
ENV API_TOKEN=your_bot_token_here

CMD ["python", "webhook.py"]
