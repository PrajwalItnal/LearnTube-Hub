FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv gunicorn dj-database-url psycopg2-binary

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# production ready server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "E_Learning.wsgi:application"]
