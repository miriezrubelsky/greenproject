import os
from pathlib import Path
import sys
import geopandas as gpd


PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

from greenproject.config import config

class PostImageProcessor:
    def __init__(self, tif_file, polygons_info, crs, image_size=1600):
        self.tif_file = tif_file
        self.polygons_info = polygons_info
        self.crs = crs
        self.image_size = image_size
        self.folder_name = tif_file.split("/")[-1].replace('.tif', '')
        self.png_tif_file = f"{self.folder_name}_png_file.png"
        self.output_png_split = 'images_split'
        self.output_dsm_split = 'dsm_split'
        self.image_name_prefix = "img"
        self.output_folder = self._create_output_folder()
        self.output_shp_path = f'{self.output_folder}/{self.folder_name}_shapefile.shp'
        self.output_png_path = f'{self.output_folder}/{self.png_tif_file}'
        self.out_folder = f'result_{self.tif_file}'
        

    def _get_folder_name(self):
         return self.tif_file.split("/")[-1].replace('.tif', '')
    
    def _create_output_folder(self):
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..','..'))
       # output_folder = os.path.join(parent_dir, config.output_dir)
        output_folder = os.path.join(parent_dir, config.output_local_dir, self.folder_name)
        # Ensure the folder exists
        if not Path(output_folder).exists():
            Path(output_folder).mkdir(parents=True, exist_ok=True)
        return output_folder    

     

    def save_shapefile(self):
        gdf = gpd.GeoDataFrame({'geometry': self.polygons_info}, crs=self.crs)
        gdf.to_file(self.output_shp_path)
        print(f"Shapefile saved to {self.output_shp_path}")   
        return  self.output_shp_path    

    def get_output_paths(self):
   
        return self.output_folder

    def print_paths(self):
        """
        Prints the paths for the output folder and shapefile.
        """
        print(f"Output folder: {self.output_folder}")
        print(f"Shapefile path: {self.output_shp_path}")

# Usage example:

