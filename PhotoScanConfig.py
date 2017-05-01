from PhotoScan import *
import os

from configparser import ConfigParser, NoOptionError


class Configuration:
    def __init__(self, config_file_path=None):

        # default configuration
        # GENERAL section (this values  need to be loaded from the config file...)
        self.project_name = ""
        self.working_directory = ""
        self.project_directory = ""
        self.log_path = ""
        self.images_directory = ""
        self.mask_path = ""

        # photos alignment section (this configurations are optional)
        # default values could be set by calling LoadDefaultConfig method
        self.photos_alignment_accuracy = None
        self.photos_alignment_preselection = None
        self.photos_alignment_generic_preselection = None
        self.photos_alignment_key_point_limit = None
        self.photos_alignment_tie_point_limit = None

        # dense cloud section (this configurations are optional)
        # default values could be set by calling LoadDefaultConfig method
        self.dense_cloud_quality = None
        self.dense_cloud_filtering = None
        self.dense_cloud_keep_depth = None
        self.dense_cloud_reuse_depth = None

        # texture section (this configurations are optional)
        # default values could be set by calling LoadDefaultConfig method
        self.texture_count = None
        self.texture_mapping = None

        # build texture section (this configurations are optional)
        # default values could be set by calling LoadDefaultConfig method
        self.texture_blending = None
        self.texture_color_correction = None
        self.texture_size = None
        self.texture_fill_holes = None

        # dem section (this configurations are optional)
        # default values could be set by calling LoadDefaultConfig method
        self.dem_source = None
        self.dem_interpolation = None

        self.LoadDefaultConfig()
        # load config file if path is available
        if config_file_path is not None:
            self.LoadConfigFile(config_file_path)

    def ConfigureGeneral(self):
        pass

    def ConfigureAlignment(self):
        pass

    def ConfigureDenseCloud(self):
        pass

    def LoadConfigFile(self, config_file_path):
        # load config file section
        # GENERAL section
        cfg_parser = ConfigParser()
        cfg_parser.read(config_file_path)
        print("Loading config file...")
        project_name = cfg_parser.get('general', 'project_name')
        print("Project name configuration successfully loaded: {}".format(project_name))

        working_directory = cfg_parser.get('general', 'working_directory')
        if not os.path.exists(working_directory):
            raise IOError("Path {} does not exist".format(working_directory))
        print("Working directory configuration successfully loaded: {}".format(working_directory))

        project_directory = os.path.join(working_directory, cfg_parser.get('general', 'project_directory'))
        if not os.path.exists(project_directory):
            print("Project directory {} doesn't exist. Creating new one...".format(project_directory))
            os.mkdir(project_directory)
        print("Project directory configuration successfully loaded: {}".format(project_directory))

        exports_directory = os.path.join(working_directory, cfg_parser.get('general', 'exports_directory'))
        if not os.path.exists(exports_directory):
            raise IOError("Path {} does not exist".format(exports_directory))
        print("exports_directory directory configuration successfully loaded: {}".format(exports_directory))
        log_path = os.path.join(working_directory, cfg_parser.get('general', 'log_path'))
        if not os.path.exists(log_path):
            raise IOError("Path {} does not exist".format(log_path))
        print("Logs path configuration successfully loaded: {}".format(log_path))

        export_cameras_directory = os.path.join(exports_directory, "Cameras")
        if not os.path.exists(export_cameras_directory):
            print("Export cameras directory {} doesn't exist. Creating new one...".format(export_cameras_directory))
            os.mkdir(export_cameras_directory)

        export_dem_directory = os.path.join(exports_directory, "Dem")
        if not os.path.exists(export_dem_directory):
            print("Export dem directory {} doesn't exist. Creating new one...".format(export_dem_directory))
            os.mkdir(export_dem_directory)

        export_markers_directory = os.path.join(exports_directory, "Markers")
        if not os.path.exists(export_markers_directory):
            print("Export markers directory {} doesn't exist. Creating new one...".format(export_markers_directory))
            os.mkdir(export_markers_directory)

        images_directory = os.path.join(working_directory, cfg_parser.get('general', 'images_directory'))
        if not os.path.exists(images_directory):
            raise IOError("Path {} does not exist".format(images_directory))
        print("Photos directory configuration successfully loaded: {}".format(images_directory))

        mask_path = os.path.join(working_directory, cfg_parser.get('general', 'mask_path'))
        if not os.path.exists(mask_path):
            raise IOError("Path {} does not exist".format(mask_path))
        print("Mask path configuration successfully loaded: {}".format(mask_path))


        # photos alignment section
        try:
            accuracy = cfg_parser.get('photos_alignment', 'accuracy')
            if accuracy == "LowestAccuracy":
                photos_alignment_accuracy = LowestAccuracy
            elif accuracy == "LowAccuracy":
                photos_alignment_accuracy = LowAccuracy
            elif accuracy == "MediumAccuracy":
                photos_alignment_accuracy = MediumAccuracy
            elif accuracy == "HighAccuracy":
                photos_alignment_accuracy = HighAccuracy
            elif accuracy == "HighestAccuracy":
                photos_alignment_accuracy = HighestAccuracy
            else:
                photos_alignment_accuracy = MediumAccuracy
                print("Photos alignment accuracy option bad format. Default setting will be used (MediumAccuracy).")
        except NoOptionError:
            photos_alignment_accuracy = MediumAccuracy
            print("Photos alignment accuracy option doesn't found in config file. Default setting will be used (MediumAccuracy).")
        print("Photos alignment accuracy loaded: {}".format(str(photos_alignment_accuracy)))

        try:
            preselection = cfg_parser.get('photos_alignment', 'preselection')
            if preselection == "NoPreselection":
                photos_alignment_preselection = NoPreselection
            elif preselection == "GenericPreselection":
                photos_alignment_preselection = GenericPreselection
            elif preselection == "ReferencePreselection":
                photos_alignment_preselection = ReferencePreselection
            else:
                photos_alignment_preselection = NoPreselection
                print(
                    "Photos alignment preselection option bad format. Default setting will be used (NoPreselection).")
        except NoOptionError:
            photos_alignment_preselection = NoPreselection
            print("Photos alignment preselection option doesn't found in config file. Default setting will be used (NoPreselection).")
        print("Photos alignment preselection loaded: {}".format(str(photos_alignment_preselection)))

        try:
            generic_preselection = cfg_parser.get('photos_alignment', 'generic_preselection')
            if generic_preselection == "True":
                photos_alignment_generic_preselection = True
            elif generic_preselection == "False":
                photos_alignment_generic_preselection = False
            else:
                photos_alignment_generic_preselection = True
                print(
                    "Photos alignment generic_preselection option bad format. Default setting will be used (True).")
        except NoOptionError:
            photos_alignment_generic_preselection = True
            print("Photos alignment generic_preselection option doesn't found in config file. Default setting will be used (True).")

        print("Photos alignment generic_preselection loaded: {}".format(str(photos_alignment_generic_preselection)))

        try:
            photos_alignment_key_point_limit = int(cfg_parser.get('photos_alignment', 'key_point_limit'))
        except NoOptionError:
            photos_alignment_key_point_limit = 40000
            print("Photos alignment key_point_limit option doesn't found in config file. Default setting will be used (40000).")
        except ValueError:
            photos_alignment_key_point_limit = 40000
            print("Photos alignment key_point_limit bad format. Default setting will be used (40000).")
        print("Photos alignment key_point_limit loaded: {}".format(str(photos_alignment_key_point_limit)))

        try:
            photos_alignment_tie_point_limit = int(cfg_parser.get('photos_alignment', 'tie_point_limit'))
        except NoOptionError:
            photos_alignment_tie_point_limit = 4000
            print("Photos alignment tie_point_limit option doesn't found in config file. Default setting will be used (4000).")
        except ValueError:
            photos_alignment_tie_point_limit = 4000
        print("Photos alignment tie_point_limit loaded: {}".format(str(photos_alignment_tie_point_limit)))

        # dense cloud section
        try:
            quality = cfg_parser.get('dense_cloud', 'quality')
            if quality == "LowestQuality":
                dense_cloud_quality = LowestQuality
            elif quality == "LowQuality":
                dense_cloud_quality = LowQuality
            elif quality == "MediumQuality":
                dense_cloud_quality = MediumQuality
            elif quality == "HighQuality":
                dense_cloud_quality = HighQuality
            elif quality == "UltraHighQuality":
                dense_cloud_quality = UltraHighQuality
            else:
                dense_cloud_quality = MediumQuality
                print("Dense cloud quality option format error. Default setting will be used (Medium).")
        except NoOptionError:
            dense_cloud_quality = MediumQuality
            print("Dense cloud quality option doesn't found in config file. Default setting will be used (Medium).")
        print("Dense cloud quality loaded: {}".format(str(dense_cloud_quality)))

        try:
            filter = cfg_parser.get('dense_cloud', 'depth_filtering')
            if filter == "NoFiltering":
                dense_cloud_filtering = NoFiltering
            elif filter == "MildFiltering":
                dense_cloud_filtering = MildFiltering
            elif filter == "ModerateFiltering":
                dense_cloud_filtering = ModerateFiltering
            elif filter == "AggressiveFiltering":
                dense_cloud_filtering = AggressiveFiltering
            else:
                dense_cloud_filtering = AggressiveFiltering
                print("Dense cloud filtering option format error. Default setting will be used (Aggressive).")
        except NoOptionError:
            dense_cloud_filtering = AggressiveFiltering
            print("Dense cloud filtering option doesn't found in config file. Default setting will be used (Aggressive).")
        print("Dense cloud depth_filtering loaded: {}".format(str(dense_cloud_filtering)))

        try:
            keep_depth = cfg_parser.get('dense_cloud', 'keep_depth')
            if keep_depth == "True":
                dense_cloud_keep_depth = True
            elif keep_depth == "False":
                dense_cloud_keep_depth = False
            else:
                dense_cloud_keep_depth = False
                print(
                    "Dense cloud keep_dept option bad format. Default setting will be used (False).")
        except NoOptionError:
            dense_cloud_keep_depth = False
            print("Dense cloud keep_dept option doesn't found in config file. Default setting will be used (False).")
        print("Dense cloud keep_depth loaded: {}".format(str(dense_cloud_keep_depth)))

        try:
            reuse_depth = cfg_parser.get('dense_cloud', 'reuse_depth')
            if reuse_depth == "True":
                dense_cloud_reuse_depth = True
            elif reuse_depth == "False":
                dense_cloud_reuse_depth = False
            else:
                dense_cloud_reuse_depth = False
                print(
                    "Dense cloud reuse_depth option bad format. Default setting will be used (False).")
        except NoOptionError:
            dense_cloud_reuse_depth = False
            print("Dense cloud reuse_depth option doesn't found in config file. Default setting will be used (False).")
        print("Dense cloud reuse_depth loaded: {}".format(str(dense_cloud_reuse_depth)))

        # mesh section
        try:
            surface = cfg_parser.get('mesh', 'surface')
            if surface == "Arbitrary":
                mesh_surface = Arbitrary
            elif surface == "HeightFiled":
                mesh_surface = HeightFiled
            else:
                mesh_surface = Arbitrary
                print("Mesh surface option format error. Default setting will be used (Arbitrary).")
        except NoOptionError:
            mesh_surface = Arbitrary
            print("Mesh surface option doesn't found in config file. Default setting will be used (Arbitrary).")
        print("Mesh surface loaded: {}".format(str(mesh_surface)))

        try:
            interpolation = cfg_parser.get('mesh', 'interpolation')
            if interpolation == "DisabledInterpolation":
                mesh_interpolation = DisabledInterpolation
            elif interpolation == "EnabledInterpolation":
                mesh_interpolation = EnabledInterpolation
            elif interpolation == "Extrapolated":
                mesh_interpolation = Extrapolated
            else:
                mesh_interpolation = EnabledInterpolation
                print("Mesh interpolation option format error. Default setting will be used (EnabledInterpolation).")
        except NoOptionError:
            mesh_interpolation = EnabledInterpolation
            print("Mesh interpolation option doesn't found in config file. Default setting will be used (EnabledInterpolation).")
        print("Mesh interpolation loaded: {}".format(str(mesh_interpolation)))


        try:
            face_count = cfg_parser.get('mesh', 'face_count')
            if face_count == "LowFaceCount":
                mesh_face_count = LowFaceCount
            elif face_count == "MediumFaceCount":
                mesh_face_count = MediumFaceCount
            elif face_count == "HighFaceCount":
                mesh_face_count = HighFaceCount
            else:
                mesh_face_count = MediumFaceCount
                print("Mesh face_count option format error. Default setting will be used (MediumFaceCount).")
        except NoOptionError:
            mesh_face_count = EnabledInterpolation
            print("Mesh face_count option doesn't found in config file. Default setting will be used (MediumFaceCount).")
        print("Mesh face_count loaded: {}".format(str(mesh_face_count)))

        # texture section
        try:
            mapping = cfg_parser.get('texture', 'mapping')
            if mapping == "GenericMapping":
                texture_mapping = GenericMapping
            elif mapping == "OrthophotoMapping":
                texture_mapping = OrthophotoMapping
            elif mapping == "AdaptiveOrthophotoMapping":
                texture_mapping = AdaptiveOrthophotoMapping
            elif mapping == "SphericalMapping":
                texture_mapping = SphericalMapping
            elif mapping == "CameraMapping":
                texture_mapping = CameraMapping
            else:
                texture_mapping = GenericMapping
                print("Texture mapping option format error. Default setting will be used (GenericMapping).")
        except NoOptionError:
            mesh_face_count = EnabledInterpolation
            print("Texture mapping option doesn't found in config file. Default setting will be used (GenericMapping).")
        print("Texture mapping loaded: {}".format(str(GenericMapping)))

        try:
            texture_count = int(cfg_parser.get('texture', 'count'))
        except NoOptionError:
            texture_count = 1
            print("texture count option doesn't found in config file. Default setting will be used (4000).")
        except ValueError:
            texture_count = 1
        print("Photos alignment tie_point_limit loaded: {}".format(str(texture_count)))

        # build texture section
        try:
            blending = cfg_parser.get('build_texture', 'blending')
            if blending == "AverageBlending":
                texture_blending = AverageBlending
            elif blending == "MosaicBlending":
                texture_blending = MosaicBlending
            elif blending == "MinBlending":
                texture_blending = MinBlending
            elif blending == "MaxBlending":
                texture_blending = MaxBlending
            elif blending == "DisabledBlending":
                texture_blending = DisabledBlending
            else:
                texture_blending = MosaicBlending
                print("Texture blending option format error. Default setting will be used (MosaicBlending).")
        except NoOptionError:
            texture_blending = MosaicBlending
            print("Texture blending option doesn't found in config file. Default setting will be used (MosaicBlending).")
        print("Texture blending loaded: {}".format(str(texture_blending)))

        try:
            color_correction = cfg_parser.get('build_texture', 'color_correction')
            if color_correction == "True":
                texture_color_correction = True
            elif color_correction == "False":
                texture_color_correction = False
            else:
                texture_color_correction = False
                print(
                    "Dense cloud color_correction option bad format. Default setting will be used (False).")
        except NoOptionError:
            texture_color_correction = False
            print("Dense cloud color_correction option doesn't found in config file. Default setting will be used (False).")
        print("Dense cloud color_correction loaded: {}".format(str(texture_color_correction)))

        try:
            texture_size = int(cfg_parser.get('build_texture', 'size'))
        except NoOptionError:
            texture_size = 2048
            print("texture count option doesn't found in config file. Default setting will be used (4000).")
        except ValueError:
            texture_size = 2048
        print("Photos alignment tie_point_limit loaded: {}".format(str(texture_size)))

        try:
            fill_holes = cfg_parser.get('build_texture', 'fill_holes')
            if fill_holes == "True":
                texture_fill_holes = True
            elif fill_holes == "False":
                texture_fill_holes = False
            else:
                texture_fill_holes = True
                print(
                    "Dense cloud fill_holes option bad format. Default setting will be used (True).")
        except NoOptionError:
            texture_fill_holes = True
            print("Dense cloud fill_holes option doesn't found in config file. Default setting will be used (True).")
        print("Dense cloud fill_holes loaded: {}".format(str(texture_fill_holes)))

        # build dem section
        try:
            source = cfg_parser.get('dem', 'source')
            if source == "PointCloudData":
                dem_source = PointCloudData
            elif source == "DenseCloudData":
                dem_source = DenseCloudData
            elif source == "DepthMapsData":
                dem_source = DepthMapsData
            elif source == "ModelData":
                dem_source = ModelData
            elif source == "TiledModelData":
                dem_source = TiledModelData
            elif source == "ElevationData":
                dem_source = ElevationData
            elif source == "OrthomosaicData":
                dem_source = OrthomosaicData
            else:
                dem_source = DenseCloudData
                print("dem source option format error. Default setting will be used (DenseCloudData).")
        except NoOptionError:
            dem_source = DenseCloudData
            print(
                "dem source option doesn't found in config file. Default setting will be used (DenseCloudData).")
        print("DEM source loaded: {}".format(str(dem_source)))

        try:
            interpolation = cfg_parser.get('dem', 'interpolation')
            if interpolation == "DisabledInterpolation":
                dem_interpolation = DisabledInterpolation
            elif interpolation == "EnabledInterpolation":
                dem_interpolation = EnabledInterpolation
            elif interpolation == "Extrapolated":
                dem_interpolation = Extrapolated
            else:
                dem_interpolation = EnabledInterpolation
                print("DEM interpolation option format error. Default setting will be used (EnabledInterpolation).")
        except NoOptionError:
            dem_interpolation = EnabledInterpolation
            print(
                "DEM interpolation option doesn't found in config file. Default setting will be used (EnabledInterpolation).")
        print("DEM interpolation loaded: {}".format(str(dem_interpolation)))

		# cameras export format
        try:
            cameras_format = cfg_parser.get('export', 'cameras_format')
            if cameras_format == "CamerasFormatXML":
                cameras_export_format = CamerasFormatXML
            elif cameras_format == "CamerasFormatCHAN":
                cameras_export_format = CamerasFormatCHAN
            elif cameras_format == "CamerasFormatBoujou":
                cameras_export_format = CamerasFormatBoujou
            elif cameras_format == "CamerasFormatBundler":
                cameras_export_format = CamerasFormatBundler
            elif cameras_format == "CamerasFormatOPK":
                cameras_export_format = CamerasFormatOPK
            elif cameras_format == "CamerasFormatPATB":
                cameras_export_format = CamerasFormatPATB
            elif cameras_format == "CamerasFormatBINGO":
                cameras_export_format = CamerasFormatBINGO
            elif cameras_format == "CamerasFormatAeroSys":
                cameras_export_format = CamerasFormatAeroSys
            elif cameras_format == "CamerasFormatInpho":
                cameras_export_format = CamerasFormatInpho
            elif cameras_format == "CamerasFormatRZML":
                cameras_export_format = CamerasFormatRZML
            elif cameras_format == "CamerasFormatVisionMap":
                cameras_export_format = CamerasFormatVisionMap
            else:
                cameras_export_format = CamerasFormatXML
                print("Cameras export option format error. Default setting will be used (CamerasFormatXML).")
        except NoOptionError:
            cameras_export_format = CamerasFormatXML
            print(
                "Cameras export format option doesn't found in config file. Default setting will be used (CamerasFormatXML).")
        print("Cameras export format loaded: {}".format(str(cameras_export_format)))

        #cameras rotation
        try:
            rotation_order = cfg_parser.get('export', 'cameras_rotation')
            if rotation_order == "RotationOrderXYZ":
                cameras_rotation_order = RotationOrderXYZ
            elif rotation_order == "RotationOrderXZY":
                cameras_rotation_order = RotationOrderXZY
            elif rotation_order == "RotationOrderYXZ":
                cameras_rotation_order = RotationOrderYXZ
            elif rotation_order == "RotationOrderYZX":
                cameras_rotation_order = RotationOrderYZX
            elif rotation_order == "RotationOrderZXY":
                cameras_rotation_order = RotationOrderZXY
            elif rotation_order == "RotationOrderZYX":
                cameras_rotation_order = RotationOrderZYX
            else:
                cameras_rotation_order = RotationOrderXYZ
                print("Cameras rotation order option format error. Default setting will be used (RotationOrderXYZ).")
        except NoOptionError:
            cameras_rotation_order = RotationOrderXYZ
            print(
                "Cameras rotation order option doesn't found in config file. Default setting will be used (RotationOrderXYZ).")
        print("Cameras rotation order loaded: {}".format(str(cameras_rotation_order)))

        # export dem raster transformation 
        try:
            transform = cfg_parser.get('export', 'raster_transform')
            if transform == "RasterTransformNone":
                raster_export_transform = RasterTransformNone
            elif transform == "RasterTransformValue":
                raster_export_transform = RasterTransformValue
            elif transform == "RasterTransformPalette":
                raster_export_transform = RasterTransformPalette
            else:
                raster_export_transform = RasterTransformNone
                print("Raster transformation export order option format error. Default setting will be used (RasterTransformNone).")
        except NoOptionError:
            raster_export_transform = RasterTransformNone
            print(
                "Raster transformation export order option doesn't found in config file. Default setting will be used (RasterTransformNone).")
        print("aster transformation export order loaded: {}".format(str(raster_export_transform)))

        # export dem no data 
        no_export_data = int(cfg_parser.get('export', 'no_data'))

        # GENERAL section (this values should be loaded from the config file...)
        self.project_name = project_name
        self.working_directory = working_directory
        self.project_directory = project_directory
        self.exports_directory = exports_directory
        self.export_cameras_directory = export_cameras_directory
        self.export_dem_directory = export_dem_directory
        self.export_markers_directory = export_markers_directory
        self.log_path = log_path
        self.images_directory = images_directory
        self.mask_path = mask_path

        # photos alignment section
        self.photos_alignment_accuracy = photos_alignment_accuracy
        self.photos_alignment_preselection = photos_alignment_preselection
        self.photos_alignment_generic_preselection = photos_alignment_generic_preselection
        self.photos_alignment_key_point_limit = photos_alignment_key_point_limit
        self.photos_alignment_tie_point_limit = photos_alignment_tie_point_limit

        # dense cloud section
        self.dense_cloud_quality = dense_cloud_quality
        self.dense_cloud_filtering = dense_cloud_filtering
        self.dense_cloud_keep_depth = dense_cloud_keep_depth
        self.dense_cloud_reuse_depth = dense_cloud_reuse_depth

        # mesh
        self.mesh_surface = mesh_surface
        self.mesh_interpolation = mesh_interpolation
        self.mesh_face_count = mesh_face_count

        # texture
        self.texture_mapping = texture_mapping
        self.texture_count = texture_count

        # build texture
        self.texture_blending = texture_blending
        self.texture_color_correction = texture_color_correction
        self.texture_size = texture_size
        self.texture_fill_holes = texture_fill_holes

        # dem
        self.dem_source = dem_source
        self.dem_interpolation = dem_interpolation

		# cameras export
        self.cameras_export_format = cameras_export_format 
        self.cameras_rotation_order = cameras_rotation_order
        # dem export 
        self.raster_export_transform = raster_export_transform
        self.no_export_data = no_export_data

    def LoadDefaultConfig(self):
        # GENERAL section (this values  need to be loaded from the config file...)
        self.project_name = ""
        self.working_directory = ""
        self.project_directory = ""
        self.log_path = ""
        self.images_directory = ""
        self.mask_path = ""

        # photos alignment section
        self.photos_alignment_accuracy = MediumAccuracy
        self.photos_alignment_preselection = NoPreselection
        self.photos_alignment_generic_preselection = True
        self.photos_alignment_key_point_limit = 40000
        self.photos_alignment_tie_point_limit = 4000

        # dense cloud section
        self.dense_cloud_quality = MediumQuality
        self.dense_cloud_filtering = AggressiveFiltering
        self.dense_cloud_keep_depth = False
        self.dense_cloud_reuse_depth = False

        # mesh
        self.mesh_surface = Arbitrary
        self.mesh_interpolation = EnabledInterpolation
        self.mesh_face_count = MediumFaceCount

        # texture
        self.texture_mapping = GenericMapping
        self.texture_count = 1

        # build texture
        self.texture_blending = MosaicBlending
        self.texture_color_correction = False
        self.texture_size = 2048
        self.texture_fill_holes = True

        # dem
        self.dem_source = DenseCloudData
        self.dem_interpolation = EnabledInterpolation