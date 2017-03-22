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
# GENERAL section
print("Loading config file...")
project_name = cfg_parser.get('general', 'project_name')
print("Project name configuration successfully loaded: {}".format(project_name))
try:
    working_directory = cfg_parser.get('general', 'working_directory')
    if not os.path.exists(working_directory):
        raise IOError("Path {} does not exist".format(working_directory))
    print("Working directory configuration successfully loaded: {}".format(working_directory))
except NoOptionError as ex:
    app.messageBox("working_directory option is missing in the configuration file.")
    raise ex
except NoSectionError as ex:
    app.messageBox("General section is missing in the configuration file.")
    raise ex

try:
    project_directory = os.path.join(working_directory, cfg_parser.get('general', 'project_directory'))
    if not os.path.exists(project_directory):
        print("Project directory {} doesn't exist. Creating new one...". format(project_directory))
        os.mkdir(project_directory)
    print("Project directory configuration successfully loaded: {}".format(project_directory))
except NoOptionError as ex:
    app.messageBox("project_directory option is missing in the configuration file.")
    raise ex
except NoSectionError as ex:
    app.messageBox("General section is missing in the configuration file.")
    raise ex

try:
    log_path = os.path.join(working_directory, cfg_parser.get('general', 'log_path'))
    if not os.path.exists(log_path):
        raise IOError("Path {} does not exist".format(log_path))
    print("Logs path configuration successfully loaded: {}".format(log_path))
except NoOptionError as ex:
    app.messageBox("log_path option is missing in the configuration file.")
    raise ex
except NoSectionError as ex:
    app.messageBox("General section is missing in the configuration file.")
    raise ex

try:
    images_directory = os.path.join(working_directory, cfg_parser.get('general', 'images_directory'))
    if not os.path.exists(images_directory):
        raise IOError("Path {} does not exist".format(images_directory))
    print("Photos directory configuration successfully loaded: {}".format(images_directory))
except NoOptionError as ex:
    app.messageBox("images_directory option is missing in the configuration file.")
    raise ex
except NoSectionError as ex:
    app.messageBox("General section is missing in the configuration file.")
    raise ex

try:
    mask_path = os.path.join(working_directory, cfg_parser.get('general', 'mask_path'))
    if not os.path.exists(mask_path):
        raise IOError("Path {} does not exist".format(mask_path))
    print("Mask path configuration successfully loaded: {}".format(mask_path))
    if not os.path.exists(images_directory):
        raise IOError("Path {} does not exist".format(images_directory))
    print("Photos directory configuration successfully loaded: {}".format(images_directory))
except NoOptionError as ex:
    app.messageBox("mask_path option is missing in the configuration file.")
    raise ex
except NoSectionError as ex:
    app.messageBox("General section is missing in the configuration file.")
    raise ex

# photos alignment section
try:
    accuracy = cfg_parser.get('photos_alignment', 'accuracy')
    if accuracy == "LowestAccuracy":
        photos_alignment_accuracy = PhotoScan.LowestAccuracy
    elif accuracy == "LowAccuracy":
        photos_alignment_accuracy = PhotoScan.LowAccuracy
    elif accuracy == "MediumAccuracy":
        photos_alignment_accuracy = PhotoScan.MediumAccuracy
    elif accuracy == "HighAccuracy":
        photos_alignment_accuracy = PhotoScan.HighAccuracy
    elif accuracy == "HighestAccuracy":
        photos_alignment_accuracy = PhotoScan.HighestAccuracy
    else:
        photos_alignment_accuracy = PhotoScan.MediumAccuracy
        print("Photos alignment accuracy option doesn't found in config file. Default setting will be used (MediumAccuracy).")
except NoOptionError:
    photos_alignment_accuracy = PhotoScan.MediumAccuracy
    print("Photos alignment accuracy option doesn't found in config file. Default setting will be used (MediumAccuracy).")

except NoSectionError:
    photos_alignment_accuracy = PhotoScan.MediumAccuracy
    print(
        "Photos alignment section doesn't found in config file.")
    app.messageBox("Config file loading error. photos_alignment section is missing.")
    raise IOError("Config file error.")
finally:
    print("Photos alignment accuracy loaded: {}".format(str(photos_alignment_accuracy)))

try:
    preselection = cfg_parser.get('photos_alignment', 'preselection')
    if preselection == "NoPreselection":
        photos_alignment_preselection = PhotoScan.NoPreselection
    elif preselection == "GenericPreselection":
        photos_alignment_preselection = PhotoScan.GenericPreselection
    elif preselection == "ReferencePreselection":
        photos_alignment_preselection = PhotoScan.ReferencePreselection
    else:
        photos_alignment_preselection = PhotoScan.NoPreselection
        print("Photos alignment preselection option doesn't found in config file. Default setting will be used (NoPreselection).")
except NoOptionError:
    photos_alignment_preselection = PhotoScan.NoPreselection
    print("Photos alignment preselection option doesn't found in config file. Default setting will be used (NoPreselection).")

except NoSectionError:
    photos_alignment_accuracy = PhotoScan.MediumAccuracy
    print(
        "Photos alignment section doesn't found in config file.")
    app.messageBox("Config file loading error. photos_alignment section is missing.")
    raise IOError("Config file error.")
finally:
    print("Photos alignment accuracy loaded: {}".format(str(photos_alignment_accuracy)))

print("Configuration file successfully loaded.")

# create document and chunk
doc = Document()
chunk = doc.addChunk()
print("Document and chunk created.")

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
chunk.matchPhotos(accuracy=photos_alignment_accuracy, preselection=photos_alignment_preselection)
chunk.alignCameras()

print("Building dense cloud...")
chunk.buildDenseCloud(quality=PhotoScan.MediumQuality)

print("Building mesh...")
chunk.buildModel(surface = PhotoScan.Arbitrary, source = PhotoScan.DenseCloudData, interpolation = PhotoScan.DisabledInterpolation, face_count = PhotoScan.MediumFaceCount)

print("Building texture...")
chunk.buildUV(mapping=PhotoScan.GenericMapping)
chunk.buildTexture(blending = PhotoScan.MosaicBlending, size = 4096)

doc.save(path=os.path.join(project_directory, project_name + '.psz'))
