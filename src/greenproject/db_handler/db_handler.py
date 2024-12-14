import psycopg2
from psycopg2 import sql
from datetime import datetime
import sys
from pathlib import Path
import os
import sys

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

class DBHandler:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                dbname=self.db_config['dbname'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            self.cursor = self.conn.cursor()
            print("Database connection established.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def close(self):
        """Close the database connection and cursor."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")
    
    def insert_model_run(self, start_time, end_time, data_size, run_duration, model_output_path):
        """Insert model run data into the Model_Runs table."""
        insert_query = """
        INSERT INTO Model_Runs (start_time, end_time, data_size, run_duration, model_output_path)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            self.cursor.execute(insert_query, (start_time, end_time, data_size, run_duration, model_output_path))
            self.conn.commit()
            print("Model run data inserted successfully.")
        except Exception as e:
            print(f"Error inserting model run data: {e}")
            self.conn.rollback()
            raise
