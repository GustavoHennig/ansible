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

from ansible.modules.cloud.hpe.oneview_os_deployment_server_facts import (OsDeploymentServerFactsModule,
                                                                          EXAMPLES)
from hpe_test_utils import FactsParamsTestCase

SERVERS = [
    {
        "name": 'Test Deployment Server',
        "description": "OS Deployment Server"
    }
]


class OsDeploymentServerFactsSpec(unittest.TestCase,
                                  FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, OsDeploymentServerFactsModule)
        self.os_deployment_servers = self.mock_ov_client.os_deployment_servers
        FactsParamsTestCase.configure_client_mock(self, self.os_deployment_servers)

        # Load scenarios from module examples
        self.EXAMPLES = yaml.load(EXAMPLES)
        self.PARAMS_GET_ALL = self.EXAMPLES[0]['oneview_os_deployment_server_facts']
        self.PARAMS_GET_BY_NAME = self.EXAMPLES[2]['oneview_os_deployment_server_facts']
        self.PARAMS_GET_BY_NAME_WITH_OPTIONS = self.EXAMPLES[4]['oneview_os_deployment_server_facts']

    def test_should_get_all_os_deployment_server(self):
        self.os_deployment_servers.get_all.return_value = SERVERS

        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        OsDeploymentServerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_deployment_servers=SERVERS)
        )

    def test_should_get_os_deployment_server_by_name(self):
        self.os_deployment_servers.get_by.return_value = SERVERS

        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        OsDeploymentServerFactsModule().run()

        self.os_deployment_servers.get_by.assert_called_once_with('name', "OS Deployment Server-Name")

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(os_deployment_servers=SERVERS)
        )

    def test_should_get_os_deployment_servers_with_options(self):
        networks = [{"name": "net"}]
        appliances = [{"name": "appl1"}, {"name": "appl2"}]
        appliance = {"name": "appl1"}
        self.os_deployment_servers.get_by.return_value = SERVERS
        self.os_deployment_servers.get_networks.return_value = networks
        self.os_deployment_servers.get_appliances.return_value = appliances
        self.os_deployment_servers.get_appliance_by_name.return_value = appliance

        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME_WITH_OPTIONS

        OsDeploymentServerFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(
                os_deployment_servers=SERVERS,
                os_deployment_server_networks=networks,
                os_deployment_server_appliances=appliances,
                os_deployment_server_appliance=appliance
            )
        )


if __name__ == '__main__':
    unittest.main()
