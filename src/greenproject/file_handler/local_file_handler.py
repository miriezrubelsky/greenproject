import os
import sys
from pathlib import Path
import json

from affine import Affine
from rasterio.crs import CRS

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

def load_file_parameters():
    parameters_dict = {}
    source_dir = get_source_dir()
    parameters_dir = get_parameters_dir()
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        if os.path.isdir(folder_path):
            parameters_file_name = folder_name + '_parameters.txt'
            parameters_file_path = os.path.join(parameters_dir, parameters_file_name)
            print(f"Checking file: '{parameters_file_path}'")
            parameters_file_path = Path(parameters_file_path)
            if parameters_file_path.exists():
                parameters ={}
                print(f"Parameters file found for {folder_name}: {parameters_file_path}")
                with open(parameters_file_path, 'r') as f:
                    data = json.load(f)
                    transform_data = data['transform']
                    transform = Affine(
                       transform_data['a'], transform_data['b'], transform_data['xoff'],
                       transform_data['d'], transform_data['e'], transform_data['yoff']
                    )
                    crs = CRS.from_string(data['crs'])
                    image_size = data['image_size']
                    parameters['image_size']=image_size
                    parameters['crs']=crs
                    parameters['transform']=transform
                    print("Reconstructed Affine Transform:", transform)
                    print("Reconstructed CRS:", crs)
                    print("Reconstructed Image Size:", image_size)
                    parameters_dict[folder_name] = parameters
                    print(folder_name)
                    print(parameters)
    return   parameters_dict   


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

def get_parameters_dir():
   parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..','..'))
   local_dir = os.path.join(parent_dir, config.local_dir)
   parameters_dir = os.path.join(local_dir, config.parameters_prefix)
   return parameters_dir
        

if __name__ == '__main__':                
  offsets_dict=load_file_parameters()
  print(offsets_dict)