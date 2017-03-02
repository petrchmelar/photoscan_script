import PhotoScan
import os

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
