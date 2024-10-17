# Ethio Medical Data Warehouse

## Project Overview

This project involves building a complete data pipwarehouseeline to scrape, clean, and store data on Ethiopian medical businesses. The final product includes an integrated data warehouse and a FastAPI backend to expose the data. Object detection using YOLO is implemented to enhance the data analysis by processing images collected from various Telegram channels.

### Key Features:

1. **Telegram Data Scraping**: Scrape relevant business data from public Telegram channels using `telethon` and Python scripts.
2. **ETL/ELT Data Transformation**: Clean and transform the data using **DBT (Data Build Tool)** for structured data in the warehouse.
3. **Object Detection with YOLO**: Use the YOLO framework to detect objects in business-related images.
4. **Data Warehouse Implementation**: Design and implement a PostgreSQL-based data warehouse for structured storage and retrieval.
5. **API with FastAPI**: Expose the collected and processed data through FastAPI, enabling easy access for other services or teams.


notebooks structure

```
export_to_postgres.ipynb                                # exporting scrapped data to postgres
yollo.ipynb                                             # notebook for object detection
