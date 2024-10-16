# scripts/export_data.py

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import psycopg2
import logging


# Load environment variables from .env file
load_dotenv('../.env')

# Fetch database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

logging.info('exporting')
def  export_to_postgres(df: pd.DataFrame, table_name: str):
    """
    Connects to the PostgreSQL database and loads data.

    :param df: data
    :param table_name: Name of the table to be created
    """


    logging.info('exporting to postgres')
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()

        # Create the table if it doesn't exist
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                Channel_Title	 VARCHAR(255),
                Channel_Username  VARCHAR(255),
                ID      INT,
                Message TEXT, 
                Date  TIMESTAMP,
                Media_Path VARCHAR(255)
            )
        """)
        
        # Insert the data into the table
        for i, row in df.iterrows():
            sql = f"INSERT INTO {table_name} (Channel_Title, Channel_Username, ID, Message, Date, Media_Path) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (row['Channel Title'], row['Channel Username'], row['ID'], row['Message'], row['Date'], row['Media Path'])
            cursor.execute(sql, values)
            
        connection.commit()
        connection.close()
        logging.info('exporting to postgres finished.')
        print('finished')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

print('end')