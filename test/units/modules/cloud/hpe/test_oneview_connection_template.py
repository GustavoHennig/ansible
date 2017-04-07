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

from oneview_module_loader import ConnectionTemplateModule
from hpe_test_utils import OneViewBaseTestCase


class ConnectionTemplateModuleSpec(unittest.TestCase,
                                   OneViewBaseTestCase):

    FAKE_MSG_ERROR = 'Fake message error'

    YAML_CONNECTION_TEMPLATE = """
            config: "{{ config }}"
            state: present
            data:
                name: 'name1304244267-1467656930023'
                type : "connection-template"
                bandwidth :
                    maximumBandwidth : 10000
                    typicalBandwidth : 2000
              """

    YAML_CONNECTION_TEMPLATE_CHANGE = """
            config: "{{ config }}"
            state: present
            data:
                name: 'name1304244267-1467656930023'
                type : "connection-template"
                bandwidth :
                    maximumBandwidth : 10000
                    typicalBandwidth : 2000
                newName : "CT-23"
          """

    YAML_CONNECTION_TEMPLATE_MISSING_KEY = """
            config: "{{ config }}"
            state: present
            data:
                state: "Configured"
        """

    DICT_CONNECTION_TEMPLATE = yaml.load(YAML_CONNECTION_TEMPLATE)["data"]
    DICT_CONNECTION_TEMPLATE_CHANGED = yaml.load(YAML_CONNECTION_TEMPLATE_CHANGE)["data"]

    def setUp(self):
        self.configure_mocks(self, ConnectionTemplateModule)

    def test_should_update_the_connection_template(self):
        self.mock_ov_client.connection_templates.get_by.return_value = [self.DICT_CONNECTION_TEMPLATE]
        self.mock_ov_client.connection_templates.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(self.YAML_CONNECTION_TEMPLATE_CHANGE)

        ConnectionTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=ConnectionTemplateModule.MSG_UPDATED,
            ansible_facts=dict(connection_template={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.mock_ov_client.connection_templates.get_by.return_value = [self.DICT_CONNECTION_TEMPLATE]

        self.mock_ansible_module.params = yaml.load(self.YAML_CONNECTION_TEMPLATE)

        ConnectionTemplateModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=ConnectionTemplateModule.MSG_ALREADY_EXIST,
            ansible_facts=dict(connection_template=self.DICT_CONNECTION_TEMPLATE)
        )

    def test_should_fail_when_key_is_missing(self):
        self.mock_ov_client.connection_templates.get_by.return_value = [self.DICT_CONNECTION_TEMPLATE]

        self.mock_ansible_module.params = yaml.load(self.YAML_CONNECTION_TEMPLATE_MISSING_KEY)

        ConnectionTemplateModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ConnectionTemplateModule.MSG_MANDATORY_FIELD_MISSING
        )

    def test_should_fail_when_connection_template_was_not_found(self):
        self.mock_ov_client.connection_templates.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(self.YAML_CONNECTION_TEMPLATE)

        ConnectionTemplateModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=ConnectionTemplateModule.MSG_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
