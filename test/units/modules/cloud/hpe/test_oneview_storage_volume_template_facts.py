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
from ansible.modules.cloud.hpe.oneview_storage_volume_template_facts import StorageVolumeTemplateFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_MANDATORY_MISSING = dict(
    config='config.json',
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="FusionTemplateExample"
)

PARAMS_GET_ALL = dict(
    config='config.json',
)

PARAMS_GET_CONNECTED = dict(
    config='config.json',
    options=['connectableVolumeTemplates']
)


class StorageVolumeTemplatesFactsSpec(unittest.TestCase,
                                      FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, StorageVolumeTemplateFactsModule)
        self.storage_volume_templates = self.mock_ov_client.storage_volume_templates
        FactsParamsTestCase.configure_client_mock(self, self.storage_volume_templates)

    def test_should_get_all_storage_volume_templates(self):
        self.storage_volume_templates.get_all.return_value = {"name": "Storage System Name"}

        self.mock_ansible_module.params = PARAMS_GET_ALL

        StorageVolumeTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_templates=({"name": "Storage System Name"}))
        )

    def test_should_get_storage_volume_template_by_name(self):
        self.storage_volume_templates.get_by.return_value = {"name": "Storage System Name"}

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        StorageVolumeTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_volume_templates=({"name": "Storage System Name"}))
        )

    def test_should_get_connectable_storage_volume_templates(self):
        self.storage_volume_templates.get_all.return_value = {"name": "Storage System Name"}
        self.storage_volume_templates.get_connectable_volume_templates.return_value = {
            "name": "Storage System Name"}

        self.mock_ansible_module.params = PARAMS_GET_CONNECTED

        StorageVolumeTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'connectable_volume_templates': {'name': 'Storage System Name'},
                           'storage_volume_templates': {'name': 'Storage System Name'}}
        )


if __name__ == '__main__':
    unittest.main()
