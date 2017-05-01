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

		export_matches_directory = os.path.join(config.exports_directory, "Matches")
		if not os.path.exists(export_matches_directory):
			print("Export matches directory {} doesn't exist. Creating new one...".format(export_matches_directory))
			os.mkdir(export_matches_directory)

		export_model_directory = os.path.join(config.exports_directory, "Model")
		if not os.path.exists(export_model_directory):
			print("Export model directory {} doesn't exist. Creating new one...".format(export_model_directory))
			os.mkdir(export_model_directory)

		export_orthomosaic_directory = os.path.join(config.exports_directory, "Orthomosaic")
		if not os.path.exists(export_orthomosaic_directory):
			print("Export orthomosaic directory {} doesn't exist. Creating new one...".format(export_orthomosaic_directory))
			os.mkdir(export_orthomosaic_directory)

		export_orthophotos_directory = os.path.join(config.exports_directory, "OrthoPhotos")
		if not os.path.exists(export_orthophotos_directory):
			print("Export orthoPhotos directory {} doesn't exist. Creating new one...".format(export_orthophotos_directory))
			os.mkdir(export_orthophotos_directory)

		export_points_directory = os.path.join(config.exports_directory, "Points")
		if not os.path.exists(export_points_directory):
			print("Export points directory {} doesn't exist. Creating new one...".format(export_points_directory))
			os.mkdir(export_points_directory)

		self.export_cameras_directory = export_cameras_directory
		self.export_dem_directory = export_dem_directory
		self.export_markers_directory = export_markers_directory
		self.export_matches_directory = export_matches_directory
		self.export_model_directory = export_model_directory
		self.export_orthomosaic_directory = export_orthomosaic_directory
		self.export_orthophotos_directory = export_orthophotos_directory
		self.export_points_directory = export_points_directory
	
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

		# export matches
		chunk.exportMatches(path=self.export_matches_directory, 
							format=self.config.matches_export_format, 
							precision=self.config.matches_export_precision, 
							export_points=True, 
							export_markers=False,
							use_labels=False)

		# export model
		chunk.exportModel(path=self.export_model_directory, 
						  binary=self.config.model_export_binary, 
						  precision=self.config.model_export_precision, 
						  texture_format=self.config.model_texture_format, 
						  texture=self.config.model_export_texture,
						  normals=self.config.model_export_normals, 
						  colors=self.config.model_export_colors, 
						  cameras=self.config.model_export_cameras, 
						  markers=self.config.model_export_markers, 
						  udim=self.config.model_export_udim,
						  strip_extensions=False)

		# export orthomosaic
		chunk.exportOrthomosaic(path=self.export_orthomosaic_directory, 
								raster_transform=self.config.raster_export_orthomosaic_transform,
								write_kml=self.config.orthomosaic_export_write_kml,
								write_world=self.config.orthomosaic_export_write_world,
								write_scheme=self.config.orthomosaic_export_write_scheme, 
								write_alpha=self.config.orthomosaic_export_write_alpha,
								tiff_compression=self.config.orthomosaic_export_tiff_compression, 
								tiff_big=self.config.orthomosaic_export_tiff_big, 
								jpeg_quality=self.config.orthomosaic_export_jpeg_quality,
								white_background=self.config.orthomosaic_export_white_background)

		# export orthophotos
		chunk.exportOrthophotos(path=self.export_orthophotos_directory, 
						  		raster_transform=self.config.raster_export_orthoPhotos_transform,
						  		write_kml=self.config.orthoPhotos_export_write_kml,
						  		write_world=self.config.orthoPhotos_export_write_world,
						  		write_scheme=self.config.orthoPhotos_export_write_scheme, 
						  		write_alpha=self.config.orthoPhotos_export_write_alpha,
						  		tiff_compression=self.config.orthoPhotos_export_tiff_compression, 
						  		tiff_big=self.config.orthoPhotos_export_tiff_big, 
						  		jpeg_quality=self.config.orthoPhotos_export_jpeg_quality,
						  		white_background=self.config.orthoPhotos_export_white_background)
		# export points
		chunk.exportPoints(path=self.export_points_directory, 
						   binary=self.config.points_export_binary, 
						   precision=self.config.points_export_precision, 
						   normals=self.config.points_export_normals, 
						   colors=self.config.points_export_colors)
