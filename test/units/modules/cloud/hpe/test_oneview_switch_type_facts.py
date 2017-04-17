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

from oneview_module_loader import SwitchTypeFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Switch Type 2"
)

SWITCH_TYPES = [{"name": "Test Switch Type 1"}, {"name": "Test Switch Type 2"}, {"name": "Test Switch Type 3"}]


class SwitchTypeFactsSpec(unittest.TestCase,
                          FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, SwitchTypeFactsModule)
        self.switch_types = self.mock_ov_client.switch_types
        FactsParamsTestCase.configure_client_mock(self, self.switch_types)

    def test_should_get_all_switch_types(self):
        self.switch_types.get_all.return_value = SWITCH_TYPES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SwitchTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switch_types=(SWITCH_TYPES))
        )

    def test_should_get_switch_type_by_name(self):
        self.switch_types.get_by.return_value = [SWITCH_TYPES[1]]
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SwitchTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switch_types=([SWITCH_TYPES[1]]))
        )


if __name__ == '__main__':
    unittest.main()
