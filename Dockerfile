FROM python:3.11

WORKDIR /app

# 1️⃣ Dépendances système (1 fois)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2️⃣ requirements SEUL (clé du cache)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 3️⃣ Copier le code APRÈS
COPY . .

EXPOSE 8080

# Lancer Flask
CMD ["python", "app.py"]
