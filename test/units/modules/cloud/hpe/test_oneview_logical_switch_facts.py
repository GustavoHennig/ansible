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

from oneview_module_loader import LogicalSwitchFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Logical Switch"
)

PRESENT_LOGICAL_SWITCHES = [{
    "name": "Test Logical Switch",
    "uri": "/rest/logical-switches/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]


class LogicalSwitchFactsSpec(unittest.TestCase,
                             FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalSwitchFactsModule)
        self.logical_switches = self.mock_ov_client.logical_switches
        FactsParamsTestCase.configure_client_mock(self, self.logical_switches)

    def test_should_get_all_logical_switches(self):
        self.logical_switches.get_all.return_value = PRESENT_LOGICAL_SWITCHES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        LogicalSwitchFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switches=(PRESENT_LOGICAL_SWITCHES))
        )

    def test_should_get_logical_switch_by_name(self):
        self.logical_switches.get_by.return_value = PRESENT_LOGICAL_SWITCHES
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        LogicalSwitchFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switches=(PRESENT_LOGICAL_SWITCHES))
        )


if __name__ == '__main__':
    unittest.main()
