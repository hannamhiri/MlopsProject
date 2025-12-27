FROM python:3.11

WORKDIR /app

# Dépendances système 
RUN apt-get update && apt-get install -y \
    libgomp1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier TOUT le projet (inclut setup.py)
COPY . .

# Installer les dépendances
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Lancer Flask
CMD ["python", "app.py"]
