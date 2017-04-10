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

from oneview_module_loader import FirmwareDriverFactsModule
from hpe_test_utils import FactsParamsTestCase

FIRMWARE_DRIVER_NAME = "Service Pack for ProLiant.iso"

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=FIRMWARE_DRIVER_NAME
)

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

FIRMWARE_DRIVER = dict(
    category='firmware-drivers',
    name=FIRMWARE_DRIVER_NAME,
    uri='/rest/firmware-drivers/Service_0Pack_0for_0ProLiant',
)


class FirmwareDriverFactsSpec(unittest.TestCase,
                              FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, FirmwareDriverFactsModule)
        self.firmware_drivers = self.mock_ov_client.firmware_drivers
        FactsParamsTestCase.configure_client_mock(self, self.firmware_drivers)

    def test_should_get_all_firmware_drivers(self):
        firmwares = [FIRMWARE_DRIVER]
        self.firmware_drivers.get_all.return_value = firmwares

        self.mock_ansible_module.params = PARAMS_GET_ALL

        FirmwareDriverFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(firmware_drivers=firmwares)
        )

    def test_should_get_by_name(self):
        firmwares = [FIRMWARE_DRIVER]
        self.firmware_drivers.get_by.return_value = firmwares

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        FirmwareDriverFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(firmware_drivers=firmwares)
        )


if __name__ == '__main__':
    unittest.main()
