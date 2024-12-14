from pathlib import Path
import os
import sys
import tqdm
import rasterio as rio
from appLogger import AppLogger

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))
appLogger = AppLogger()

from greenproject.processing.image_processor import ImageProcessor
from greenproject.processing.post_image_processor import PostImageProcessor
from greenproject.config import config
from greenproject.file_handler import local_file_handler
from greenproject.file_handler import s3_file_handler


if __name__ == '__main__':
    
    s3_file_handler.download_all_s3_files()
    appLogger.getLogger().debug(f"start processing")

    out_folder = 'output_folder'
    model_path = config.MODEL_NAME
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
    local_dir = os.path.join(parent_dir, config.local_dir)
    local_dir = os.path.join(local_dir, config.prefix)
    offsets = local_file_handler.load_file_offsets()
    parameters = local_file_handler.load_file_parameters()
    tif_file_list = local_file_handler.load_tif_file_list()
    for tif_file in tif_file_list:
   
      offset_per_pic = offsets[tif_file]
      parameters = parameters[tif_file]
  
      if parameters is None or offsets is None:
        print(f"Skipping {tif_file} due to missing parameters or offsets.")
        continue  # Skip this tif_file and move to the next one
      for root, dirs, files in os.walk(local_dir):
            adjusted_polygons = []  
            for png_image in tqdm.tqdm(files, desc=f"Processing images in {root}"):
               if png_image.endswith('.png'):
                  png_image_path = os.path.join(root, png_image)
                  print(f"Processing image: {png_image_path}")
                  model_path = os.path.join(config.SAVE_MODEL_PATH,config.MODEL_NAME)
                  print(model_path)
                  print(root)
                  processor = ImageProcessor(model_path, root, offset_per_pic)
                  polygons = processor.process_image(png_image_path, parameters['transform'])
                  adjusted_polygons.extend(polygons)  # Accumulate the polygons
                  postprocessor = PostImageProcessor(tif_file,adjusted_polygons,parameters['crs'])
                  postprocessor.save_shapefile()
   