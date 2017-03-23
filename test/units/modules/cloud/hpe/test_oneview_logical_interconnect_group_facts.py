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

from hpe_test_utils import FactsParamsTestCase

from ansible.modules.cloud.hpe.oneview_logical_interconnect_group_facts import LogicalInterconnectGroupFactsModule

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Logical Interconnect Group"
)

PRESENT_LIGS = [{
    "name": "Test Logical Interconnect Group",
    "uri": "/rest/logical-interconnect-groups/ebb4ada8-08df-400e-8fac-9ff987ac5140"
}]


class LogicalInterconnectGroupFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalInterconnectGroupFactsModule)
        self.logical_interconnect_groups = self.mock_ov_client.logical_interconnect_groups
        FactsParamsTestCase.configure_client_mock(self, self.logical_interconnect_groups)

    def test_should_get_all_ligs(self):
        self.logical_interconnect_groups.get_all.return_value = PRESENT_LIGS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        LogicalInterconnectGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnect_groups=(PRESENT_LIGS))
        )

    def test_should_get_lig_by_name(self):
        self.logical_interconnect_groups.get_by.return_value = PRESENT_LIGS
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        LogicalInterconnectGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_interconnect_groups=(PRESENT_LIGS))
        )


if __name__ == '__main__':
    unittest.main()
