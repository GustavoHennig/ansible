#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see <http://www.gnu.org/licenses/>.

import unittest

from oneview_module_loader import ArtifactBundleFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'


class ArtifactBundleFactsSpec(unittest.TestCase,
                              FactsParamsTestCase):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """

    def setUp(self):
        self.configure_mocks(self, ArtifactBundleFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        FactsParamsTestCase.configure_client_mock(self, self.i3s.artifact_bundles)

        self.TASK_GET_ALL = self.EXAMPLES[0]['image_streamer_artifact_bundle_facts']
        self.TASK_GET_BY_NAME = self.EXAMPLES[4]['image_streamer_artifact_bundle_facts']
        self.TASK_GET_ALL_BACKUPS = self.EXAMPLES[6]['image_streamer_artifact_bundle_facts']
        self.TASK_GET_BACKUP = self.EXAMPLES[9]['image_streamer_artifact_bundle_facts']

        self.ARTIFACT_BUNDLE = dict(
            name="HPE-ImageStreamer-Developer-2016-09-12",
            uri="/rest/artifact-bundles/a2f97f20-160c-4c78-8185-1f31f86efaf7")

    def test_get_all_artifact_bundles(self):
        self.i3s.artifact_bundles.get_all.return_value = [self.ARTIFACT_BUNDLE]
        self.mock_ansible_module.params = self.TASK_GET_ALL

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE])
        )

    def test_get_an_artifact_bundle_by_name(self):
        self.i3s.artifact_bundles.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.mock_ansible_module.params = self.TASK_GET_BY_NAME

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE])
        )

    def test_get_all_backups(self):
        self.i3s.artifact_bundles.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.i3s.artifact_bundles.get_all_backups.return_value = [self.ARTIFACT_BUNDLE]

        self.mock_ansible_module.params = self.TASK_GET_ALL_BACKUPS

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE], artifact_bundle_backups=[self.ARTIFACT_BUNDLE])
        )

    def test_get_backup_for_an_artifact_bundle(self):
        self.i3s.artifact_bundles.get_by.return_value = [self.ARTIFACT_BUNDLE]
        self.i3s.artifact_bundles.get_backup.return_value = [self.ARTIFACT_BUNDLE]

        self.mock_ansible_module.params = self.TASK_GET_BACKUP

        ArtifactBundleFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(artifact_bundles=[self.ARTIFACT_BUNDLE],
                               backup_for_artifact_bundle=[self.ARTIFACT_BUNDLE])
        )


if __name__ == '__main__':
    unittest.main()
