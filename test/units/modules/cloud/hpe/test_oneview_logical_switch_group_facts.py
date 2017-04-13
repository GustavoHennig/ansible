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
from oneview_module_loader import LogicalSwitchGroupFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'


class LogicalSwitchGroupFactsSpec(unittest.TestCase,
                                  FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalSwitchGroupFactsModule)
        self.logical_switch_groups = self.mock_ov_client.logical_switch_groups
        FactsParamsTestCase.configure_client_mock(self, self.logical_switch_groups)

        self.PARAMS_GET_ALL = self.EXAMPLES[0]['oneview_logical_switch_group_facts']
        self.PARAMS_GET_BY_NAME = self.EXAMPLES[4]['oneview_logical_switch_group_facts']

    def test_should_get_logical_switch_group_by_name(self):
        self.logical_switch_groups.get_by.return_value = {"name": "Logical Switch Group"}
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switch_groups=({"name": "Logical Switch Group"}))
        )

    def test_should_get_all_logical_switch_groups(self):
        self.logical_switch_groups.get_all.return_value = {"name": "Logical Switch Group"}
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        LogicalSwitchGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_switch_groups=({"name": "Logical Switch Group"}))
        )


if __name__ == '__main__':
    unittest.main()
