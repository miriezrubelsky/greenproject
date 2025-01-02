from sklearn.metrics import jaccard_score
import pickle
import os
import sys
from pathlib import Path
import emails



PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))



from greenproject.processing.image_processor import ImageProcessor
from greenproject.config import config
from greenproject.config import db_config
from greenproject.file_handler import  s3_file_handler
from greenproject.mail_handler.mail_handler import  MailHandler
from greenproject.db_handler.db_handler import DBHandler
from greenproject.validation import validation_utils

MODEL_PATH  = os.path.join(config.SAVE_MODEL_PATH,config.MODEL_NAME)
PARENT_DIR = Path(os.path.abspath(os.path.join(os.getcwd(), '..')))
LOCAL_DIR = PARENT_DIR / config.local_dir / config.validation_prefix



def validate():

   db_handler = DBHandler(db_config.DB_CONFIG)
   db_handler.connect()
   validation_image, predict_image = validation_utils.categorize_files(LOCAL_DIR)
   png_image_path = Path(LOCAL_DIR) / predict_image
   validation_image_path = Path(LOCAL_DIR) / validation_image

   pred_metrix =validation_utils.process_prediction(png_image_path)
   if pred_metrix is None:
        return
   validation_metrix =validation_utils.load_validation_image(validation_image_path)
   if validation_metrix is None:
        return

   jac= validation_utils.calculate_jaccard_score(pred_metrix, validation_metrix)
   if jac is None:
        return
  
  # threshold = 0.8  # Set your threshold for the Jaccard score
   status, error_message = validation_utils.send_validation_results(jac, config.threshold)
   validation_utils.process_database_run( validation_image, predict_image, jac, config.threshold, status, error_message)

   
    

if __name__ == '__main__':
   s3_file_handler.download_all_s3_validation_files()
   validate()
   validation_utils.move_processed_folder_to_completed()