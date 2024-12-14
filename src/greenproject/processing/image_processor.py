import os
import pickle
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
import detectree as dtr
import numpy as np
from shapely.geometry import JOIN_STYLE
from shapely.ops import unary_union
from skimage.measure import find_contours
from appLogger import AppLogger
import sys
from pathlib import Path
appLogger = AppLogger()

PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

class ImageProcessor:
    def __init__(self, model_path, output_png_split, offsets):
        
        self.model_path = model_path
        self.output_png_split = output_png_split
        self.offsets = offsets
        self.clf = pickle.load(open(self.model_path, 'rb'))
        self.clf_v1 = dtr.Classifier(clf=self.clf)

    def process_image(self, png_name, transform):
        appLogger.getLogger().debug("Start process image")
        file_name = os.path.basename(png_name)
        if file_name not in self.offsets:
            appLogger.getLogger().debug(f"Warning: No offset found for {file_name} . Skipping processing.")
            return []
        offset = self.offsets[file_name]
        # Predict models
        #appLogger.getLogger().debug(png_name)
        
        y_pred = self.clf_v1.predict_img(png_name)
        # Process results
        vegetation_mask = np.where(y_pred == 0, 0, 255)
        polygons = self.create_polygons(vegetation_mask)
        adjusted_polygons = []
        for polygon in polygons:
            exterior_coords = [(x + offset[0], y + offset[1]) for x, y in polygon.exterior.coords]
            interiors = []
            for interior in polygon.interiors:
                interior_coords = [(x + offset[0], y + offset[1]) for x, y in interior.coords]
                interiors.append(interior_coords)

            exterior_coords = [transform * (x, y) for x, y in exterior_coords]
            interiors = [[transform * (x, y) for x, y in interior] for interior in interiors]
            adjusted_polygon = Polygon(exterior_coords, interiors)
            adjusted_polygons.append(adjusted_polygon)

        return adjusted_polygons 

    def create_polygons(self, mask):

        simplification_tolerance = 1.0
        min_polygon_points = 3
        min_contour_points = 3
        join_mitre_leange = 1
        contours_level = 0.5
        min_area = 20.0
        contours = find_contours(mask, level=contours_level)
        polygons = []
        for contour in contours:
            if len(contour) >= min_contour_points:
                polygon = Polygon(contour[:, ::-1])
                if polygon.is_valid:
                    polygons.append(polygon)

        buffered_polygons = [polygon.buffer(join_mitre_leange, join_style=JOIN_STYLE.mitre) for polygon in polygons]
        combined_polygons = unary_union(buffered_polygons)
        if isinstance(combined_polygons, MultiPolygon):
            combined_polygons = list(combined_polygons.geoms)
        elif isinstance(combined_polygons, Polygon):
            combined_polygons = [combined_polygons]
        else:
            combined_polygons = list(combined_polygons.geoms) if isinstance(combined_polygons, GeometryCollection) else []

        filtered_polygons = [polygon for polygon in combined_polygons
                             if len(polygon.exterior.coords) >= min_polygon_points and polygon.area >= min_area]
        simplified_polygons = [polygon.simplify(simplification_tolerance, preserve_topology=True) for polygon in filtered_polygons]
        final_polygons = []
        for polygon in simplified_polygons:
            if not polygon.is_empty and polygon.is_valid:
                final_polygons.append(polygon)

        return final_polygons
    


