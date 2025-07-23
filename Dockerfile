# Python 3.10 bazası
FROM python:3.10-slim

# İş qovluğu
WORKDIR /app

# Asılılıqlar faylını kopyala
COPY requirements.txt .

# Asılılıqları quraşdır
RUN pip install --no-cache-dir -r requirements.txt

# Layihəni kopyala
COPY . .

# PORT mühit dəyişəni üçün default təyin et
ENV PORT=8000

# Botu gunicorn ilə işə sal (webhook.py faylındakı Flask app = app)
CMD ["gunicorn", "webhook:app", "--bind", "0.0.0.0:8000"]
