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

from oneview_module_loader import SwitchFactsModule
from hpe_test_utils import FactsParamsTestCase


ERROR_MSG = 'Fake message error'

SWITCH_NAME = '172.18.20.1'

SWITCH_URI = '/rest/switches/028e81d0-831b-4211-931c-8ac63d687ebd'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=SWITCH_NAME,
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name=SWITCH_NAME,
    options=['environmentalConfiguration']
)

SWITCH = dict(name=SWITCH_NAME, uri=SWITCH_URI)

ALL_SWITCHES = [SWITCH, dict(name='172.18.20.2')]


class SwitchFactsSpec(unittest.TestCase,
                      FactsParamsTestCase):

    def setUp(self):
        self.configure_mocks(self, SwitchFactsModule)
        self.switches = self.mock_ov_client.switches
        FactsParamsTestCase.configure_client_mock(self, self.switches)

    def test_should_get_all(self):
        self.switches.get_all.return_value = ALL_SWITCHES
        self.mock_ansible_module.params = PARAMS_GET_ALL

        SwitchFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switches=ALL_SWITCHES)
        )

    def test_should_get_by_name(self):
        switches = [SWITCH]
        self.switches.get_by.return_value = switches
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SwitchFactsModule().run()

        self.switches.get_by.assert_called_once_with('name', SWITCH_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switches=switches)
        )

    def test_should_get_by_name_with_options(self):
        switches = [SWITCH]
        environmental_configuration = dict(calibratedMaxPower=0, capHistorySupported=False)

        self.switches.get_by.return_value = switches
        self.switches.get_environmental_configuration.return_value = environmental_configuration
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        SwitchFactsModule().run()

        self.switches.get_by.assert_called_once_with('name', SWITCH_NAME)
        self.switches.get_environmental_configuration.assert_called_once_with(id_or_uri=SWITCH_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(switches=switches, switch_environmental_configuration=environmental_configuration)
        )


if __name__ == '__main__':
    unittest.main()
