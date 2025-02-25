FROM python:3.12

WORKDIR /app

# Instalar dependências
RUN apt-get update && \
    apt-get install -y unzip && \
    rm -rf /var/lib/apt/lists/*

# Instalar bibliotecas
RUN pip install pandas sqlalchemy psycopg2-binary kaggle

# Copiar script Python
COPY etl.py .

# Configurar credenciais do Kaggle
RUN mkdir -p /root/.kaggle
COPY kaggle/kaggle.json /root/.kaggle/
RUN chmod 600 /root/.kaggle/kaggle.json

# Executar script
CMD ["python", "etl.py"]