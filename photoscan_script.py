from PhotoScan import app
import argparse

from configparser import ConfigParser

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
    raise IOError("File \"{}\" does not exist".format(config_file_path))

# try parse config file
cfg_parser = ConfigParser()
cfg_parser.read(config_file_path)

# load configuration





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
