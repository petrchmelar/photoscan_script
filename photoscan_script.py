from PhotoScan import *
import argparse
import glob
import os

from configparser import ConfigParser, NoOptionError, NoSectionError

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
    print("Your config file path is {}".format(config_file_path))
else:
    app.messageBox("Invalid config file path: \"{}\"".format(config_file_path))
    print("Invalid config file path: \"{}\"".format(config_file_path))

# try parse config file
cfg_parser = ConfigParser()
cfg_parser.read(config_file_path)

# load config file section
try:
    # GENERAL section
    print("Loading config file...")
    project_name = cfg_parser.get('general', 'project_name')
    print("Project name configuration successfully loaded: {}".format(project_name))

    working_directory = cfg_parser.get('general', 'working_directory')
    if not os.path.exists(working_directory):
        raise IOError("Path {} does not exist".format(working_directory))
    print("Working directory configuration successfully loaded: {}".format(working_directory))

    project_directory = os.path.join(working_directory, cfg_parser.get('general', 'project_directory'))
    if not os.path.exists(project_directory):
        print("Project directory {} doesn't exist. Creating new one...". format(project_directory))
        os.mkdir(project_directory)
    print("Project directory configuration successfully loaded: {}".format(project_directory))

    log_path = os.path.join(working_directory, cfg_parser.get('general', 'log_path'))
    if not os.path.exists(log_path):
        raise IOError("Path {} does not exist".format(log_path))
    print("Logs path configuration successfully loaded: {}".format(log_path))

    images_directory = os.path.join(working_directory, cfg_parser.get('general', 'images_directory'))
    if not os.path.exists(images_directory):
        raise IOError("Path {} does not exist".format(images_directory))
    print("Photos directory configuration successfully loaded: {}".format(images_directory))

    mask_path = os.path.join(working_directory, cfg_parser.get('general', 'mask_path'))
    if not os.path.exists(mask_path):
        raise IOError("Path {} does not exist".format(mask_path))
    print("Mask path configuration successfully loaded: {}".format(mask_path))
    print("Configuration file successfully loaded.")

except Exception as ex:
    app.messageBox("Config file loading error.")
    raise ex

# create document and chunk
doc = Document()
chunk = doc.addChunk()
print("Document and chunk created.")

# load mask
if len(mask_path):
    chunk.importMasks(mask_path)
    print("Mask imported")

# load photos and add them into the chunk
images = []
image_extensions = ['*.jpg', '*.png', '*.raw']
print("Loading images...")
for image_extension in image_extensions:
    for filename in glob.glob(os.path.join(images_directory, image_extension)):
        images.append(filename)
        print("Image {} loaded.".format(filename))

if len(images) == 0:
    app.messageBox("No images found.")
    print("No images found in directory {}".format(photos_directory))

chunk.addPhotos(images)

# load coordinates from the log file and add them into the chunk
print("Loading references...")
# check extension
if os.path.split(log_path)[1] in ['csv', 'txt']:
    raise IOError("Log file {} has bad format. (Required csv or txt)")
chunk.loadReference(log_path, columns='nyxz', delimiter='\t')

# set coordinates system
print("Setting coordinate system on EPSG::4326...")
chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")

# set camera accuracy
print("Setting camera location accuracy on {}...".format([0.05, 0.05, 0.05]))
chunk.camera_location_accuracy = PhotoScan.Vector((0.05, 0.05, 0.05))

# update transformation
print("Updating transformation...")
chunk.updateTransform()

print("Photos alignment...")
chunk.matchPhotos(accuracy=PhotoScan.LowestAccuracy, preselection=PhotoScan.ReferencePreselection)
chunk.alignCameras()

print("Building dense cloud...")
chunk.buildDenseCloud(quality=PhotoScan.MediumQuality)

print("Building mesh...")
chunk.buildModel(surface = PhotoScan.Arbitrary, source = PhotoScan.DenseCloudData, interpolation = PhotoScan.DisabledInterpolation, face_count = PhotoScan.MediumFaceCount)

print("Building texture...")
chunk.buildUV(mapping=PhotoScan.GenericMapping)
chunk.buildTexture(blending = PhotoScan.MosaicBlending, size = 4096)


doc.save(path=os.path.join(project_directory, project_name + '.psz'))


"""
doc = PhotoScan.app.document
chunk = doc.addChunk()

working_path = "D:\\photoscan_test"

# Load photos
photo_path = working_path + "\\photos"
photo_list = os.listdir(photo_path)
for photo_name in photo_list:
        chunk.addPhotos([photo_path + "\\" + photo_name])

# Import coordinates of cameras
cameralog_path = working_path + "\\logs\\log.txt"
chunk.loadReference(cameralog_path, format='csv', columns='nyxz', delimiter='\t')

chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")
chunk.accuracy_cameras = [0.05, 0.05, 0.05]
chunk.updateTransform()

# Align photos
chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.ReferencePreselection)
chunk.buildPoints()
#chunk.alignCameras()
"""
