#  Drakkar-Software OctoBot-Tentacles-Manager
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

import os.path as path

import octobot_tentacles_manager.exporters.artifact_exporter as artifact_exporter
import octobot_tentacles_manager.models as models
import octobot_tentacles_manager.constants as constants
import octobot_tentacles_manager.util as util


class TentaclePackageExporter(artifact_exporter.ArtifactExporter):
    def __init__(self,
                 artifact: models.TentaclePackage,
                 exported_tentacles_package: str,
                 tentacles_folder: str,
                 should_cythonize: bool = False,
                 should_zip: bool = False,
                 with_dev_mode: bool = False):
        super().__init__(artifact,
                         tentacles_folder=tentacles_folder,
                         should_cythonize=should_cythonize,
                         should_zip=should_zip,
                         with_dev_mode=with_dev_mode)
        self.exported_tentacles_package: str = exported_tentacles_package

        self.tentacles_filter: util.TentacleFilter = None
        self.tentacles_white_list: list = []
        self.tentacles = []

        # create working folder
        self.working_folder = path.join(constants.TENTACLES_PACKAGE_CREATOR_TEMP_FOLDER,
                                        constants.TENTACLES_ARCHIVE_ROOT) if self.should_zip else self.artifact.name

    async def prepare_export(self):
        if not self.with_dev_mode or self.exported_tentacles_package is not None:
            self.tentacles = util.load_tentacle_with_metadata(self.tentacles_folder)
            # remove dev-mode or non exported package tentacles if necessary
            self.tentacles_white_list = util.filter_tentacles_by_dev_mode_and_package(
                tentacles=self.tentacles,
                with_dev_mode=self.with_dev_mode,
                package_filter=self.exported_tentacles_package
            )

        self.tentacles_filter = util.TentacleFilter(self.tentacles, self.tentacles_white_list)
        if self.should_zip:
            self.copy_directory_content_to_temporary_dir(self.tentacles_folder,
                                                         ignore=self.tentacles_filter.should_ignore)
        else:
            self.copy_directory_content_to_working_dir(self.tentacles_folder,
                                                       ignore=self.tentacles_filter.should_ignore)
