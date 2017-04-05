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

from ansible.modules.cloud.hpe.oneview_connection_template_facts import ConnectionTemplateFactsModule
from hpe_test_utils import FactsParamsTestCase


class ConnectionTemplatesFactsSpec(unittest.TestCase,
                                   FactsParamsTestCase):

    ERROR_MSG = 'Fake message error'

    PARAMS_MANDATORY_MISSING = dict(
        config='config.json',
    )

    PARAMS_GET_BY_NAME = dict(
        config='config.json',
        name="name1304244267-1467656930023"
    )

    PARAMS_GET_ALL = dict(
        config='config.json',
    )

    PARAMS_GET_DEFAULT = dict(
        config='config.json',
        options=['defaultConnectionTemplate']
    )

    def setUp(self):
        self.configure_mocks(self, ConnectionTemplateFactsModule)
        self.connection_templates = self.mock_ov_client.connection_templates
        FactsParamsTestCase.configure_client_mock(self, self.connection_templates)

    def test_should_get_all_connection_templates(self):
        self.connection_templates.get_all.return_value = {"name": "Storage System Name"}
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        ConnectionTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(connection_templates=({"name": "Storage System Name"}))
        )

    def test_should_get_connection_template_by_name(self):
        self.connection_templates.get_by.return_value = {"name": "Storage System Name"}

        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        ConnectionTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(connection_templates=({"name": "Storage System Name"}))
        )

    def test_should_get_default_connection_template(self):
        self.connection_templates.get_default.return_value = {
            "name": "default_connection_template"}

        self.mock_ansible_module.params = self.PARAMS_GET_DEFAULT

        ConnectionTemplateFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'default_connection_template': {'name': 'default_connection_template'}}
        )


if __name__ == '__main__':
    unittest.main()
