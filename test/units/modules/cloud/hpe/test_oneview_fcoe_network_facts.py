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

from ansible.modules.cloud.hpe.oneview_fcoe_network_facts import FcoeNetworkFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test FCoE Networks"
)

PRESENT_NETWORKS = [{
    "name": "Test FCoE Networks",
    "uri": "/rest/fcoe-networks/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]


class FcoeNetworkFactsSpec(unittest.TestCase,
                           FactsParamsTestCase
                           ):
    def setUp(self):
        self.configure_mocks(self, FcoeNetworkFactsModule)
        self.fcoe_networks = self.mock_ov_client.fcoe_networks
        FactsParamsTestCase.configure_client_mock(self, self.fcoe_networks)

    def test_should_get_all_fcoe_network(self):
        self.fcoe_networks.get_all.return_value = PRESENT_NETWORKS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        FcoeNetworkFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fcoe_networks=PRESENT_NETWORKS)
        )

    def test_should_get_fcoe_network_by_name(self):
        self.fcoe_networks.get_by.return_value = PRESENT_NETWORKS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        FcoeNetworkFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(fcoe_networks=PRESENT_NETWORKS)
        )


if __name__ == '__main__':
    unittest.main()
