FROM python:3.11

# Dépendances système (OBLIGATOIRE pour LightGBM)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installer les deps Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

EXPOSE 8080

# Lancer Flask
CMD ["python", "app.py"]
