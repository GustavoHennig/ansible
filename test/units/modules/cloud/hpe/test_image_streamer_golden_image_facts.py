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

from oneview_module_loader import GoldenImageFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'


class GoldenImageFactsSpec(unittest.TestCase,
                           FactsParamsTestCase):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """

    def setUp(self):
        self.configure_mocks(self, GoldenImageFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        FactsParamsTestCase.configure_client_mock(self, self.i3s.golden_images)

        # Load scenarios from module examples
        self.TASK_GET_ALL = self.EXAMPLES[0]['image_streamer_golden_image_facts']
        self.TASK_GET_BY_NAME = self.EXAMPLES[4]['image_streamer_golden_image_facts']

        self.GOLDEN_IMAGE = dict(
            name="Golden Image name",
            uri="/rest/golden-image/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_get_all_golden_images(self):
        self.i3s.golden_images.get_all.return_value = [self.GOLDEN_IMAGE]
        self.mock_ansible_module.params = self.TASK_GET_ALL

        GoldenImageFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(golden_images=[self.GOLDEN_IMAGE])
        )

    def test_get_a_golden_image_by_name(self):
        self.i3s.golden_images.get_by.return_value = [self.GOLDEN_IMAGE]
        self.mock_ansible_module.params = self.TASK_GET_BY_NAME

        GoldenImageFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(golden_images=[self.GOLDEN_IMAGE])
        )


if __name__ == '__main__':
    unittest.main()
