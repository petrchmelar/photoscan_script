from PhotoScan import *
import os

class PhotoScanExporter:
	def __init__(self, config, chunk):
		if chunk is None:
			raise ValueError("chunk does not exist !")

		if config is None:
			raise ValueError("configuration does not exist !")

		# create export directories
		export_cameras_directory = os.path.join(config.exports_directory, "Cameras")
		if not os.path.exists(export_cameras_directory):
			print("Export cameras directory {} doesn't exist. Creating new one...".format(export_cameras_directory))
			os.mkdir(export_cameras_directory)

		export_dem_directory = os.path.join(config.exports_directory, "Dem")
		if not os.path.exists(export_dem_directory):
			print("Export dem directory {} doesn't exist. Creating new one...".format(export_dem_directory))
			os.mkdir(export_dem_directory)

		export_markers_directory = os.path.join(config.exports_directory, "Markers")
		if not os.path.exists(export_markers_directory):
			print("Export markers directory {} doesn't exist. Creating new one...".format(export_markers_directory))
			os.mkdir(export_markers_directory)

		self.export_cameras_directory = export_cameras_directory
		self.export_dem_directory = export_dem_directory
		self.export_markers_directory = export_markers_directory

	def exportAll(self):
		# export cameras
		chunk.exportCameras(path=self.export_cameras_directory, 
		                    format=self.config.cameras_export_format, 
		                    rotation_order=self.config.cameras_rotation_order)

		# export dem
		chunk.exportDem(path=self.export_dem_directory, 
		                raster_transform=self.config.raster_export_transform,
		                nodata=self.config.no_export_data,
		                write_kml=False,
		                write_world=False, 
		                write_scheme=False, 
		                tiff_big=False)

		# export markers
		chunk.exportMarkers(path=self.export_markers_directory)