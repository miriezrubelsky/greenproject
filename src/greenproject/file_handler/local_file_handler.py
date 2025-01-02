import os
import sys
from pathlib import Path
import json

from affine import Affine
from rasterio.crs import CRS
import rasterio as rio

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from greenproject.config import config

  

# Dictionary to store folder names and their respective offsets
def load_tif_file_list():
    tif_file_list =[]
    source_dir = get_source_dir()
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        if os.path.isdir(folder_path):
            tif_file_list.append(folder_name)  # A
    return   tif_file_list      

def load_file_metadata():
    metadata_dict = {}
    source_dir = get_source_dir()
    metadata_dir = get_metadata_dir()
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        if os.path.isdir(folder_path):
            metadata_file_name = folder_name + '_metadata.txt'
            metadata_file_path = os.path.join(metadata_dir, metadata_file_name)
            print(f"Checking file: '{metadata_file_path}'")
            metadata_file_path = Path(metadata_file_path)
            if metadata_file_path.exists():
                metadata ={}
                print(f"Metadata file found for {folder_name}: {metadata_file_path}")
                with open(metadata_file_path, 'r') as f:
                    data = json.load(f)
                    transform_data = data['transform']
                    transform = Affine(
                       transform_data['a'], transform_data['b'], transform_data['xoff'],
                       transform_data['d'], transform_data['e'], transform_data['yoff']
                    )
                    crs = CRS.from_string(data['crs'])
                    image_size = data['image_size']
                    metadata['image_size']=image_size
                    metadata['crs']=crs
                    metadata['transform']=transform
                    print("Reconstructed Affine Transform:", transform)
                    print("Reconstructed CRS:", crs)
                    print("Reconstructed Image Size:", image_size)
                    metadata_dict[folder_name] = metadata
                    print(folder_name)
                    print(metadata)
    return   metadata_dict   


def load_file_offsets():
    offsets_dict = {}
    source_dir = get_source_dir()
    offsets_dir = get_offsets_dir()
    #print("source_dir"+source_dir)
    #print("offset"+offsets_dir)
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        
        if os.path.isdir(folder_path):
            offsets_file_name = folder_name + '_offsets.txt'
            offsets_file_path = os.path.join(offsets_dir, offsets_file_name)
            print(f"Checking file: '{offsets_file_path}'")
            offsets_file_path = Path(offsets_file_path)
            if offsets_file_path.exists():
                print(f"Offsets file found for {folder_name}: {offsets_file_path}")
      
                with open(offsets_file_path, 'r') as offsets_file:
                    offsets_content = offsets_file.read()  # Assuming the content is text
                    offsets_dict[folder_name] = json.loads(offsets_content)   # Store it in the dictionary
            else:
                print(f"Offsets file NOT found for {folder_name}")
    print( offsets_dict)            
    return  offsets_dict   

def get_source_dir():
   parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..','..'))
   local_dir = os.path.join(parent_dir, config.local_dir)
   source_dir = os.path.join(local_dir, config.prefix)
   print(source_dir)
   return source_dir

def get_offsets_dir():
   parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..','..'))
   local_dir = os.path.join(parent_dir, config.local_dir)
   offset_dir = os.path.join(local_dir, config.offset_prefix)
   return offset_dir

def get_metadata_dir():
   parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..','..'))
   local_dir = os.path.join(parent_dir, config.local_dir)
   metadata_dir = os.path.join(local_dir, config.metadata_prefix)
   return metadata_dir

def load_png_file(png_file):
    """Load and return the PNG file using rasterio."""
    with rio.open(png_file) as src:
        image = src.read(1)  # Reads the first band of the image
    return image 

       

if __name__ == '__main__':                
  offsets_dict=load_file_metadata()
  print(offsets_dict)