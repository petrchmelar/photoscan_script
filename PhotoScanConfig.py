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
                print("Photos alignment accuracy option doesn't found in config file. Default setting will be used (MediumAccuracy).")
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
                    "Photos alignment preselection option doesn't found in config file. Default setting will be used (NoPreselection).")
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
                    "Photos alignment generic_preselection option doesn't found in config file. Default setting will be used (True).")
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
        print("Dense cloud quality loaded: {}".format(str(dense_cloud_filtering)))

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

        # GENERAL section (this values should be loaded from the config file...)
        self.project_name = project_name
        self.working_directory = working_directory
        self.project_directory = project_directory
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