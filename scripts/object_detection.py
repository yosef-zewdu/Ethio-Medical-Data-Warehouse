# scripts/export_data.py

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import psycopg2
import logging
import torch


# Load environment variables from .env file
load_dotenv('../.env')

# Fetch database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")




def object_detect(model, image_dir):
    # Load the YOLOv5 model
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # 'yolov5s' is the small model

    # Directory containing your images
    # image_dir = '../ph'
    results = []

    a = 0
    # Loop through each image
    for img_name in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img_name)
        
        # Perform inference
        results = model(img_path)
    
        if a < 3:
            # Show results
            results.show()  # Displays the image with bounding boxes
            results.print()  # Prints detection results
        a+=1

# create table
def create_table(table_name: str):
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

         # Create detection table in the database
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                class_id INT,
                class_name VARCHAR(255),
                confidence FLOAT,
                x1 INT,
                y1 INT,
                x2 INT,
                y2 INT,
                image_name VARCHAR(255)
            )
        """)
       # Commit after each image
        connection.commit()

        # Close the database connection
        cursor.close()
        connection.close()
         
        logging.info('exporting to postgres finished.')
        print('finished')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def export_detection(table_name:str):
    '''
        export the detections to postgres
    '''
    # Load the YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Load the small YOLOv5 model

    # Establish a connection to the database
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = connection.cursor()

    # Directory containing your images
    image_dir = '../ph'

    # Loop through each image
    for img_name in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img_name)
        
        # Perform inference
        results = model(img_path)

        # Access results
        detections = results.xyxy[0]  # Get detections in the format [x1, y1, x2, y2, conf, class]

        # Insert detection results into the database
        for *box, conf, cls in detections.tolist():
            x1, y1, x2, y2 = map(int, box)
            class_id = int(cls)  # Class ID
            confidence = float(conf)  # Confidence score
            class_name = model.names[class_id]  # Get class name from model

            # Store detection data in the database
            cur.execute(
                f"INSERT INTO {table_name} (class_id,class_name, confidence, x1, y1, x2, y2, image_name) VALUES (%s,  %s, %s, %s, %s, %s, %s, %s)",
                (class_id, class_name, confidence, x1, y1, x2, y2, img_name)
            )

        # Commit after each image
        connection.commit()

    # Close the database connection
    cur.close()
    connection.close()