import pathlib
import os
import greenproject


PACKAGE_ROOT = pathlib.Path(greenproject.__file__).resolve().parent

IMAGE_NAME_PREFIX = "tile"


MODEL_NAME = 'tree_model_new'
SAVE_MODEL_PATH = os.path.join(PACKAGE_ROOT,'trained_model')



# AWS credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = 'us-east-1'

SMTP_HOST ="smtp.mail.yahoo.com"
SMTP_USER ="miriperelman@yahoo.com"
SMTP_PASSWORD ="nassnhryvoccuuac"


bucket_name = 'miri-bucket'  
prefix = 'output-splitted-png-in-process' 
prefix_completed = 'output-splitted-png-completed'  
validation_prefix = 'validation-processed'
validation_prefix_completed = 'validation-completed'
output_prefix = 'output_files' 
offset_prefix = 'output-splitted-png-in-process-offsets'
offset_prefix_completed = 'output-splitted-png_offsets-completed'
metadata_prefix = 'output-splitted-png-in-process-metadata'
metadata_prefix_completed = 'output-splitted-png-metadata-completed'
local_dir = 'downloaded_files' 
output_local_dir = 'output_files' 


threshold = 0.8





