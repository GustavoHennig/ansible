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
import yaml

from oneview_module_loader import ServerHardwareTypeModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

YAML_SERVER_HARDWARE_TYPE = """
        config: "{{ config }}"
        state: present
        data:
          name: 'My Server Hardware Type'
          description: "New Description"
          """

YAML_SERVER_HARDWARE_TYPE_CHANGE = """
        config: "{{ config }}"
        state: present
        data:
          name: 'My Server Hardware Type'
          newName: 'My New Server Hardware Type'
          description: "Another Description"
          """

YAML_SERVER_HARDWARE_TYPE_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name: 'MyServerHardwareType'
        """

DICT_DEFAULT_SERVER_HARDWARE_TYPE = yaml.load(YAML_SERVER_HARDWARE_TYPE)["data"]
DICT_DEFAULT_SERVER_HARDWARE_TYPE_CHANGED = yaml.load(YAML_SERVER_HARDWARE_TYPE_CHANGE)["data"]


class ServerHardwareTypeSpec(unittest.TestCase, OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, ServerHardwareTypeModule)
        self.resource = self.mock_ov_client.server_hardware_types

    def test_should_update_the_server_hardware_type(self):
        srv_hw_type = DICT_DEFAULT_SERVER_HARDWARE_TYPE.copy()
        srv_hw_type['uri'] = '/rest/id'

        self.resource.get_by.return_value = [srv_hw_type]
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_CHANGE)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareTypeModule.MSG_UPDATED,
            ansible_facts=dict(server_hardware_type={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_SERVER_HARDWARE_TYPE]

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareTypeModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(server_hardware_type=DICT_DEFAULT_SERVER_HARDWARE_TYPE)
        )

    def test_should_remove_server_hardware_type(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_SERVER_HARDWARE_TYPE]

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_ABSENT)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ServerHardwareTypeModule.MSG_DELETED
        )

    def test_should_do_nothing_when_server_hardware_type_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE_ABSENT)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ServerHardwareTypeModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_server_hardware_type_was_not_found(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_SERVER_HARDWARE_TYPE)

        ServerHardwareTypeModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ServerHardwareTypeModule.MSG_RESOURCE_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
