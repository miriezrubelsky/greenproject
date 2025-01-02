import os
import sys
from pathlib import Path
import tqdm
import rasterio as rio
from appLogger import AppLogger
from datetime import datetime


# Setup logger
appLogger = AppLogger()

# Constants and paths
PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from greenproject.processing.image_processor import ImageProcessor
from greenproject.processing.post_image_processor import PostImageProcessor
from greenproject.db_handler.db_handler import DBHandler
from greenproject.config import config
from greenproject.file_handler import local_file_handler, s3_file_handler

MODEL_PATH  = os.path.join(config.SAVE_MODEL_PATH,config.MODEL_NAME)
OUTPUT_FOLDER = 'output_folder'
PARENT_DIR = Path(os.path.abspath(os.path.join(os.getcwd(), '..')))
LOCAL_DIR = PARENT_DIR / config.local_dir / config.prefix

DB_CONFIG = {
    'host': 'postgres',
    'port': '5432',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '1234'
}

def download_files():
    """Download necessary files from S3."""
    s3_file_handler.download_all_s3_files()

def upload_files():
    """Download necessary files from S3."""
    s3_file_handler.upload_folder_to_s3()

def move_processed_folder_to_completed():
    
    s3_file_handler.move_processed_folder_to_completed(config.bucket_name,config.prefix,config.prefix_completed)
    s3_file_handler.move_processed_folder_to_completed(config.bucket_name,config.offset_prefix,config.offset_prefix_completed)
    s3_file_handler.move_processed_folder_to_completed(config.bucket_name,config.metadata_prefix,config.metadata_prefix_completed)

def load_data():
    """Load all necessary data for processing."""
    offsets = local_file_handler.load_file_offsets()
    metadata = local_file_handler.load_file_metadata()
    tif_files = local_file_handler.load_tif_file_list()
    return offsets, metadata, tif_files

def process_image_file(tif_file, offsets, metadata):
    """Process each TIFF file."""
    offset_per_pic = offsets.get(tif_file)
    file_metadata = metadata.get(tif_file)

    if file_metadata is None or offset_per_pic is None:
        appLogger.getLogger().debug(f"Skipping {tif_file} due to missing metadata or offsets.")
        return  # Skip if data is missing
    
    adjusted_polygons = []
    
    # Walk through directories to find PNG images
    for root, _, files in os.walk(LOCAL_DIR):
        for png_image in tqdm.tqdm([f for f in files if f.endswith('.png')], desc=f"Processing images in {root}"):
            png_image_path = Path(root) / png_image
            appLogger.getLogger().debug(f"Processing image: {png_image_path}")
            processor = ImageProcessor(MODEL_PATH, root, offset_per_pic)
            polygons = processor.process_image(png_image_path, file_metadata['transform'])
            adjusted_polygons.extend(polygons)
    
    # Post-process and save shapefile
    postprocessor = PostImageProcessor(tif_file, adjusted_polygons, file_metadata['crs'])
    postprocessor.save_shapefile()
    return postprocessor.get_output_paths()
    
def process_database_run(db_handler, start_time, end_time, total_data_size, run_duration,output_path):
        db_handler.insert_model_run(start_time, end_time, total_data_size, run_duration, output_path)

def main():
    if(s3_file_handler.is_folder_empty(config.bucket_name,config.prefix)):
         appLogger.getLogger().debug(f"The folder {config.prefix} is empty")
         print(f"The folder {config.prefix} is empty")
    db_handler = DBHandler(DB_CONFIG)
    db_handler.connect()
    start_time = datetime.now() 
    download_files()
    appLogger.getLogger().debug("Start processing")
    offsets, metadata, tif_files = load_data()
    total_data_size =0
    for tif_file in tif_files:
        data_size = len(tif_file)
        start_time = datetime.now()
        output_path = process_image_file(tif_file, offsets, metadata)
        end_time = datetime.now()
        run_duration = end_time - start_time
        process_database_run(db_handler, start_time, end_time, data_size, run_duration,output_path)
    
    db_handler.close()  
    upload_files()
    move_processed_folder_to_completed()

if __name__ == '__main__':
    main()
