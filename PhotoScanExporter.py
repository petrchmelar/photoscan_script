from PhotoScan import *
import os
import sys
import logging

# logger initialization
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[SCRIPT] %(asctime)s:%(name)s:%(levelname)s: %(message)s')
# file handler
file_handler = logging.FileHandler('{}/script.log'.format(os.path.dirname(os.path.abspath(__file__))),
'w')
file_handler.setFormatter(formatter)
# stdout handler
stdout_handler = logging.StreamHandler(sys.stdout)

stdout_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

class PhotoScanExporter:
	def __init__(self, config, chunk):
		if chunk is None:
			message = "Chunk does not exist!"
			logger.error(message)
			raise ValueError(message)
		else:
			self.chunk = chunk

		if config is None:
			message = "Configuration does not exist!"
			logger.error(message)
			raise ValueError(message)
		# create export directories
		export_cameras_directory = os.path.join(config.exports_directory, "Cameras")
		if not os.path.exists(export_cameras_directory):
			logger.warning("Export cameras directory {} doesn't exist. Creating new one...".format(export_cameras_directory))
			os.mkdir(export_cameras_directory)

		export_dem_directory = os.path.join(config.exports_directory, "Dem")
		if not os.path.exists(export_dem_directory):
			logger.warning("Export dem directory {} doesn't exist. Creating new one...".format(export_dem_directory))
			os.mkdir(export_dem_directory)

		export_markers_directory = os.path.join(config.exports_directory, "Markers")
		if not os.path.exists(export_markers_directory):
			logger.warning("Export markers directory {} doesn't exist. Creating new one...".format(export_markers_directory))
			os.mkdir(export_markers_directory)

		export_matches_directory = os.path.join(config.exports_directory, "Matches")
		if not os.path.exists(export_matches_directory):
			logger.warning("Export matches directory {} doesn't exist. Creating new one...".format(export_matches_directory))
			os.mkdir(export_matches_directory)

		export_model_directory = os.path.join(config.exports_directory, "Model")
		if not os.path.exists(export_model_directory):
			logger.warning("Export model directory {} doesn't exist. Creating new one...".format(export_model_directory))
			os.mkdir(export_model_directory)

		export_orthomosaic_directory = os.path.join(config.exports_directory, "Orthomosaic")
		if not os.path.exists(export_orthomosaic_directory):
			logger.warning("Export orthomosaic directory {} doesn't exist. Creating new one...".format(export_orthomosaic_directory))
			os.mkdir(export_orthomosaic_directory)

		export_orthophotos_directory = os.path.join(config.exports_directory, "OrthoPhotos")
		if not os.path.exists(export_orthophotos_directory):
			logger.warning("Export orthoPhotos directory {} doesn't exist. Creating new one...".format(export_orthophotos_directory))
			os.mkdir(export_orthophotos_directory)

		export_points_directory = os.path.join(config.exports_directory, "Points")
		if not os.path.exists(export_points_directory):
			logger.warning("Export points directory {} doesn't exist. Creating new one...".format(export_points_directory))
			os.mkdir(export_points_directory)

		export_report_directory = os.path.join(config.exports_directory, "Report")
		if not os.path.exists(export_report_directory):
			logger.warning("Export report directory {} doesn't exist. Creating new one...".format(export_report_directory))
			os.mkdir(export_report_directory)

		export_shapes_directory = os.path.join(config.exports_directory, "Shapes")
		if not os.path.exists(export_shapes_directory):
			logger.warning("Export shapes directory {} doesn't exist. Creating new one...".format(export_shapes_directory))
			os.mkdir(export_shapes_directory)

		export_tiledModel_directory = os.path.join(config.exports_directory, "TiledModel")
		if not os.path.exists(export_tiledModel_directory):
			logger.warning("Export Tiled model directory {} doesn't exist. Creating new one...".format(export_tiledModel_directory))
			os.mkdir(export_tiledModel_directory)

		self.export_cameras_directory = export_cameras_directory
		self.export_dem_directory = export_dem_directory
		self.export_markers_directory = export_markers_directory
		self.export_matches_directory = export_matches_directory
		self.export_model_directory = export_model_directory
		self.export_orthomosaic_directory = export_orthomosaic_directory
		self.export_orthophotos_directory = export_orthophotos_directory
		self.export_points_directory = export_points_directory
		self.export_report_directory = export_report_directory
		self.export_shapes_directory = export_shapes_directory
		self.export_tiledModel_directory = export_tiledModel_directory

	def exportAll(self):
		# export cameras
		self.chunk.exportCameras(path=self.export_cameras_directory,
			                     format=self.config.cameras_export_format,
			                     rotation_order=self.config.cameras_rotation_order)

		# export dem
		self.chunk.exportDem(path=self.export_dem_directory,
			                 raster_transform=self.config.raster_export_transform,
			                 nodata=self.config.no_export_data,
			                 write_kml=False,
			                 write_world=False,
			                 write_scheme=False,
			                 tiff_big=False)

		# export markers
		self.chunk.exportMarkers(path=self.export_markers_directory)

		# export matches
		self.chunk.exportMatches(path=self.export_matches_directory,
								 format=self.config.matches_export_format,
								 precision=self.config.matches_export_precision,
								 export_points=True,
								 export_markers=False,
								 use_labels=False)

		# export model
		self.chunk.exportModel(path=self.export_model_directory,
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
		self.chunk.exportOrthomosaic(path=self.export_orthomosaic_directory,
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
		self.chunk.exportOrthophotos(path=self.export_orthophotos_directory,
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
		self.chunk.exportPoints(path=self.export_points_directory,
							    binary=self.config.points_export_binary,
							    precision=self.config.points_export_precision,
							    normals=self.config.points_export_normals,
							    colors=self.config.points_export_colors)

		# export report
		self.chunk.exportReport(path=self.export_report_directory)

		# export shapes
		self.chunk.exportShapes(path=self.export_shapes_directory,
						   		items=self.config.export_shapes_items)

		# exoirt tiled model
		self.chunk.exportTiledModel(path=self.export_tiledModel_directory,
								    format=self.config.tiled_model_export_format,
								    mesh_format=self.config.tiled_model_export_mesh_format)
