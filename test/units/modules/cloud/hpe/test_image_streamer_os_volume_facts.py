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

from oneview_module_loader import OsVolumeFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'


class OsVolumeFactsSpec(unittest.TestCase,
                        FactsParamsTestCase):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """

    def setUp(self):
        self.configure_mocks(self, OsVolumeFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        FactsParamsTestCase.configure_client_mock(self, self.i3s.os_volumes)

        # Load scenarios from module examples
        self.PLAY_GET_ALL = self.EXAMPLES[0]['image_streamer_os_volume_facts']
        self.PLAY_GET_BY_NAME = self.EXAMPLES[4]['image_streamer_os_volume_facts']

        self.OS_VOLUME = dict(
            name="OS Volume Name",
            uri="/rest/os-volumes/a3b3c234-2ei0-b99o-jh778jsdkl2n5")

    def test_get_all_os_volumes(self):
        self.i3s.os_volumes.get_all.return_value = [self.OS_VOLUME]
        self.mock_ansible_module.params = self.PLAY_GET_ALL

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME])
        )

    def test_get_os_volume_by_name(self):
        self.i3s.os_volumes.get_by.return_value = [self.OS_VOLUME]
        self.mock_ansible_module.params = self.PLAY_GET_BY_NAME

        OsVolumeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_volumes=[self.OS_VOLUME])
        )


if __name__ == '__main__':
    unittest.main()
