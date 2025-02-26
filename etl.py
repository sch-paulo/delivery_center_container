import pandas as pd
import os
import glob
from sqlalchemy import create_engine
import time

def main():
    # Setup para conexão com o banco de dados
    user = "postgres"
    password = "postgrespass"
    dbname = "delivery_center"
    host = "db"
    port = 5432

    # Esperar devida configuração do Postgres para conectar
    while True:
        try:
            engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')
            engine.connect()
            break
        except Exception as e:
            print("Waiting for database...")
            time.sleep(5)

    # Processar arquivos
    base_path = '/app/dataset'
    csv_files = glob.glob(f'{base_path}/*.csv')
    
    for file in csv_files:
        df_name = os.path.basename(file).split('.')[0]
        df = pd.read_csv(file, encoding='latin1')
        
        # Converter colunas de tipo data
        if df_name == 'orders':
            date_columns = [
                'order_moment_created', 'order_moment_accepted',
                'order_moment_ready', 'order_moment_collected',
                'order_moment_in_expedition', 'order_moment_delivering',
                'order_moment_delivered', 'order_moment_finished'
            ]
            for col in date_columns:
                df[col] = pd.to_datetime(
                    df[col],
                    format='%m/%d/%Y %I:%M:%S %p',
                    errors='coerce'
                )
        
        # Inserir dados no banco
        df.to_sql(
            df_name,
            engine,
            if_exists='replace',
            index=False,
            method='multi',
            chunksize=1000
        )
        print(f'{df_name} inserido')

if __name__ == '__main__':
    main()