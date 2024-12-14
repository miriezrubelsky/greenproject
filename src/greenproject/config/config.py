import pathlib
import os
import greenproject


PACKAGE_ROOT = pathlib.Path(greenproject.__file__).resolve().parent

IMAGE_NAME_PREFIX = "tile"


MODEL_NAME = 'tree_model_new'
SAVE_MODEL_PATH = os.path.join(PACKAGE_ROOT,'trained_model')



# AWS credentials
AWS_ACCESS_KEY_ID ='AKIAS7IX5HS445262XN3'
AWS_SECRET_ACCESS_KEY = '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'
REGION_NAME = 'us-east-1'


bucket_name = 'miri-bucket'  
prefix = 'output-splitted-png'  
output_prefix = 'output_files' 
offset_prefix = 'output-splitted-png_offsets'
parameters_prefix = 'output-splitted-png_parameters'
local_dir = 'downloaded_files' 
output_local_dir = 'output_files' 





