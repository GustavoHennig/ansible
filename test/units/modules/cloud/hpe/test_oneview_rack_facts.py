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

from ansible.modules.cloud.hpe.oneview_rack_facts import RackFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_MANDATORY_MISSING = dict(
    config='config.json',
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="RackName01"
)

PARAMS_GET_ALL = dict(
    config='config.json',
)

PARAMS_GET_TOPOLOGY = dict(
    config='config.json',
    name="RackName01",
    options=['deviceTopology']
)


class RackFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, RackFactsModule)
        self.resource = self.mock_ov_client.racks
        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_should_get_all(self):
        self.resource.get_all.return_value = {"name": "Rack Name"}

        self.mock_ansible_module.params = PARAMS_GET_ALL

        RackFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(racks=({"name": "Rack Name"}))
        )

    def test_should_get_by_name(self):
        self.resource.get_by.return_value = {"name": "Rack Name"}

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        RackFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(racks=({"name": "Rack Name"}))
        )

    def test_should_get_rack_device_topology(self):
        rack = [{"name": "Rack Name", "uri": "/rest/uri/123"}]
        self.resource.get_by.return_value = rack
        self.resource.get_device_topology.return_value = {"name": "Rack Name"}

        self.mock_ansible_module.params = PARAMS_GET_TOPOLOGY

        RackFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'rack_device_topology': {'name': 'Rack Name'},
                           'racks': rack}
        )


if __name__ == '__main__':
    unittest.main()
