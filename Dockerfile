FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    python3-pip \
    unzip \
    curl \
    gnupg \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libu2f-udev \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Establecer variables de entorno para que Selenium sepa dónde está Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY filters.json .

# Copiar el resto del código
COPY . .

CMD ["python", "main.py"]