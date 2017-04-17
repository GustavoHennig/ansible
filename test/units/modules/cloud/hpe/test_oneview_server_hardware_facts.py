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
from oneview_module_loader import ServerHardwareFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Server Hardware"
)

PARAMS_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Server Hardware",
    options=[
        'bios', 'javaRemoteConsoleUrl', 'environmentalConfig', 'iloSsoUrl', 'remoteConsoleUrl', 'firmware',
        {"utilization": {"fields": 'AveragePower',
                         "filter": 'startDate=2016-05-30T03:29:42.000Z',
                         "view": 'day'}}]
)

PARAMS_WITH_ALL_FIRMWARES_WITHOUT_FILTER = dict(
    config='config.json',
    options=['firmwares']
)

FIRMWARE_FILTERS = [
    "components.componentName='HPE Synergy 3530C 16G Host Bus Adapter'",
    "components.componentVersion matches '1.2%'"
]

PARAMS_WITH_ALL_FIRMWARES_WITH_FILTERS = dict(
    config='config.json',
    options=[dict(firmwares=dict(filters=FIRMWARE_FILTERS))]
)


class ServerHardwareFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, ServerHardwareFactsModule)
        self.server_hardware = self.mock_ov_client.server_hardware

        FactsParamsTestCase.configure_client_mock(self, self.server_hardware)

    def test_should_get_all_server_hardware(self):
        self.server_hardware.get_all.return_value = {"name": "Server Hardware Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ServerHardwareFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardwares=({"name": "Server Hardware Name"}))
        )

    def test_should_get_server_hardware_by_name(self):
        self.server_hardware.get_by.return_value = {"name": "Server Hardware Name"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        ServerHardwareFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardwares=({"name": "Server Hardware Name"}))
        )

    def test_should_get_server_hardware_by_name_with_options(self):
        self.server_hardware.get_by.return_value = [{"name": "Server Hardware Name", "uri": "resuri"}]
        self.server_hardware.get_bios.return_value = {'subresource': 'value'}
        self.server_hardware.get_environmental_configuration.return_value = {'subresource': 'value'}
        self.server_hardware.get_java_remote_console_url.return_value = {'subresource': 'value'}
        self.server_hardware.get_ilo_sso_url.return_value = {'subresource': 'value'}
        self.server_hardware.get_remote_console_url.return_value = {'subresource': 'value'}
        self.server_hardware.get_utilization.return_value = {'subresource': 'value'}
        self.server_hardware.get_firmware.return_value = {'subresource': 'firmware'}
        self.mock_ansible_module.params = PARAMS_WITH_OPTIONS

        ServerHardwareFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={'server_hardwares': [{'name': 'Server Hardware Name', 'uri': 'resuri'}],
                           'server_hardware_remote_console_url': {'subresource': 'value'},
                           'server_hardware_utilization': {'subresource': 'value'},
                           'server_hardware_ilo_sso_url': {'subresource': 'value'},
                           'server_hardware_bios': {'subresource': 'value'},
                           'server_hardware_java_remote_console_url': {'subresource': 'value'},
                           'server_hardware_env_config': {'subresource': 'value'},
                           'server_hardware_firmware': {'subresource': 'firmware'}}
        )

    def test_should_get_all_firmwares_across_the_servers(self):
        self.server_hardware.get_all.return_value = []
        self.server_hardware.get_all_firmwares.return_value = [{'subresource': 'firmware'}]
        self.mock_ansible_module.params = PARAMS_WITH_ALL_FIRMWARES_WITHOUT_FILTER

        ServerHardwareFactsModule().run()

        self.server_hardware.get_all_firmwares.assert_called_once_with()
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={
                'server_hardwares': [],
                'server_hardware_firmwares': [{'subresource': 'firmware'}]
            }
        )

    def test_should_get_all_firmwares_with_filters(self):
        self.server_hardware.get_all.return_value = []
        self.server_hardware.get_all_firmwares.return_value = [{'subresource': 'firmware'}]
        self.mock_ansible_module.params = PARAMS_WITH_ALL_FIRMWARES_WITH_FILTERS

        ServerHardwareFactsModule().run()

        self.server_hardware.get_all_firmwares.assert_called_once_with(filters=FIRMWARE_FILTERS)
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts={
                'server_hardwares': [],
                'server_hardware_firmwares': [{'subresource': 'firmware'}]
            }
        )


if __name__ == '__main__':
    unittest.main()
