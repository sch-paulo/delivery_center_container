# Imagem da versão do Python a ser instalada dentro do container
FROM python:3.12-slim

# Definir o diretório de trabalho
# Todos os comandos subsequentes serão executados aqui
WORKDIR /app

# Instalar bibliotecas
RUN pip install pandas sqlalchemy psycopg2-binary

# Copiar script Python
COPY etl.py .

# Executar script
CMD ["python", "etl.py"]