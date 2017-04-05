from PhotoScan import *
import argparse
import glob
import os

from PhotoScanConfig import Configuration

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

config = Configuration(config_file_path=config_file_path)

# create document and chunk
doc = Document()
chunk = doc.addChunk()
print("Document and chunk created.")

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

print("Photos alignment...")
chunk.matchPhotos(accuracy=config.photos_alignment_accuracy,
                  preselection=photos_alignment_preselection,
                  generic_preselection=photos_alignment_generic_preselection,
                  keypoint_limit=photos_alignment_key_point_limit,
                  tiepoint_limit=photos_alignment_tie_point_limit)
chunk.alignCameras()

print("Building dense cloud...")
chunk.buildDenseCloud(quality=dense_cloud_quality, filter=dense_cloud_filtering)

print("Building mesh...")
chunk.buildModel(surface = PhotoScan.Arbitrary, source = PhotoScan.DenseCloudData, interpolation = PhotoScan.DisabledInterpolation, face_count = PhotoScan.MediumFaceCount)

print("Building texture...")
chunk.buildUV(mapping=PhotoScan.GenericMapping)
chunk.buildTexture(blending = PhotoScan.MosaicBlending, size = 4096)

doc.save(path=os.path.join(project_directory, project_name + '.psz'))
