from PhotoScan import *
import argparse
import glob
import os

from configparser import ConfigParser, NoOptionError, NoSectionError

class PSConfigurator:
	def __init__(self, config_file_path):
		self.cfg_parser = ConfigParser()
		self.cfg_parser.read(config_file_path)

		Alignment_options = {
			"accuracy" : {
			"LowestAccuracy" 		: PhotoScan.LowestAccuracy,
			"LowAccuracy" 	 		: PhotoScan.LowAccuracy,
			"MediumAccuracy" 		: PhotoScan.MediumAccuracy,
			"HighAccuracy" 			: PhotoScan.HighAccuracy,
			"HighestAccuracy" 		: PhotoScan.HighestAccuracy,
			},
			"preselection" : {
			"NoPreselection" 		: PhotoScan.NoPreselection,
			"GenericPreselection"	: PhotoScan.GenericPreselection,
			"ReferencePreselection"	: PhotoScan.ReferencePreselection,
			}
		}

		Dense_Cloud_options = {
			"quality" : {
			"UltraHigh"				: PhotoScan.UltraQuality,
			"High"					: PhotoScan.HighQuality,
			"Medium"				: PhotoScan.MediumQuality,
			"Low"					: PhotoScan.LowQuality,
			"Lowest"				: PhotoScan.LowestQuality,
			},
			"depth_filtering": {
			"Disabled"				: PhotoScan.NoFiltering,
			"Mild"					: PhotoScan.MildFiltering,
			"Moderate"				: PhotoScan.moderateFiltering,
			"Aggressive"			: PhotoScan.AggressiveFiltering,
			}
		}

		#default configuration
		self.accuracy = Alignment_options["accuracy"]["MediumAccuracy"]
		self.photos_alignment_preselection = Alignment_options["preselection"]["NoPreselection"]
		self.photos_alignment_generic_preselection = True
		self.photos_alignment_key_point_limit = 40000
		self.photos_alignment_tie_point_limit = 4000

		self.dense_cloud_quality = Dense_Cloud_options["quality"]["Medium"]
		self.dense_cloud_filtering = Dense_Cloud_options["depth_filtering"]["Disabled"]

	def ConfigureGeneral(self):
		pass

	def ConfigureAlignment(self):
		pass

	def ConfigureDenseCloud(self):
		pass