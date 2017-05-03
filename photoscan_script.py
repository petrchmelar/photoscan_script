from PhotoScan import *
import logging
import argparse
import glob
import os
import sys

from PhotoScanConfig import Configuration
from PhotoScanExporter import PhotoScanExporter

# loger initialization
# setup logger
logger = logging.getLogger("photoscan_script")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# file handler
file_handler = logging.FileHandler('{}/script.log'.format(os.path.dirname(os.path.abspath(__file__))))
file_handler.setFormatter(formatter)
# stdout handler
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

# Load config using python argparse if the config file is available
config_file_path = ""

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--config', help='Path to config file.')
args = arg_parser.parse_args()

if args.config:
    config_file_path = args.config
else:
    config_file_path = app.getOpenFileName("Select config file.")

# check if the config file exists
if os.path.exists(config_file_path):
    logger.info("Your config file path is {}".format(config_file_path))
else:
    app.messageBox("Invalid config file path: \"{}\"".format(config_file_path))
    logger.error("Invalid config file path: \"{}\"".format(config_file_path))

config = Configuration(config_file_path=config_file_path)

# create document and chunk
doc = Document()
chunk = doc.addChunk()
print("Document and chunk created.")

# mask
chunk.importMasks(config.mask_path)
print("Mask imported.")

# load photos and add them into the chunk
images = []
image_extensions = ['*.jpg', '*.png', '*.raw']
print("Loading images...")
for image_extension in image_extensions:
    for filename in glob.glob(os.path.join(config.images_directory, image_extension)):
        images.append(filename)
        print("Image {} loaded.".format(filename))

if len(images) == 0:
    app.messageBox("No images found.")
    print("No images found in directory {}".format(config.photos_directory))

chunk.addPhotos(images)

# load coordinates from the log file and add them into the chunk
print("Loading references...")
# check extension
if os.path.split(config.log_path)[1] in ['csv', 'txt']:
    raise IOError("Log file {} has bad format. (Required csv or txt)")
chunk.loadReference(config.log_path, columns='nyxz', delimiter='\t')

# set coordinates system
print("Setting coordinate system on EPSG::4326...")
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")

# set camera accuracy
print("Setting camera location accuracy on {}...".format([0.05, 0.05, 0.05]))
chunk.camera_location_accuracy = PhotoScan.Vector((0.05, 0.05, 0.05))

# update transformation
print("Updating transformation...")
chunk.updateTransform()

# photos alignment
print("Photos alignment...")
chunk.matchPhotos(accuracy=config.photos_alignment_accuracy,
                  preselection=config.photos_alignment_preselection,
                  generic_preselection=config.photos_alignment_generic_preselection,
                  keypoint_limit=config.photos_alignment_key_point_limit,
                  tiepoint_limit=config.photos_alignment_tie_point_limit)
chunk.alignCameras()

# build dense cloud
print("Building dense cloud...")
chunk.buildDenseCloud(quality=config.dense_cloud_quality,
                      filter=config.dense_cloud_filtering,
                      keep_depth = config.dense_cloud_keep_depth,
                      reuse_depth = config.dense_cloud_reuse_depth)

# build mesh
print("Building mesh...")
chunk.buildModel(surface = config.mesh_surface,
                 source = PhotoScan.DenseCloudData,
                 interpolation = config.mesh_interpolation,
                 face_count = config.mesh_face_count)

# build texture
print("Building texture...")
chunk.buildUV(mapping=config.texture_mapping,
              count=config.texture_count)
chunk.buildTexture(blending=config.texture_blending,
                   color_correction=config.texture_color_correction,
                   size=config.texture_size,
                   fill_holes=config.texture_fill_holes)

doc.save(path=os.path.join(config.project_directory, config.project_name + '.psx'))
doc.open(os.path.join(config.project_directory, config.project_name + '.psx'))
chunk = dock.chunk

# build dem
chunk.buildDem(source=config.dem_source,
              interpolation=config.dem_interpolation)

try:
  exporter = PhotoScanExporter(config, chunk)
  exporter.exportAll()
except ValueError as err:
  raise IOError("PhotoScanExporter: " + err.args)

doc.save(path=os.path.join(config.project_directory, config.project_name + '.psx'))
