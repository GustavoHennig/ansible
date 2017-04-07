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
from oneview_module_loader import FirmwareDriverModule
from hpe_test_utils import OneViewBaseTestCase

FIRMWARE_DRIVER_NAME = "Service Pack for ProLiant.iso"

PARAMS_ABSENT = dict(
    config='config.json',
    state='absent',
    name=FIRMWARE_DRIVER_NAME
)

FIRMWARE_DRIVER = dict(name=FIRMWARE_DRIVER_NAME)


class FirmwareDriverModuleSpec(unittest.TestCase,
                               OneViewBaseTestCase):

    def setUp(self):
        self.configure_mocks(self, FirmwareDriverModule)

    def test_should_remove_firmware_driver(self):
        firmwares = [FIRMWARE_DRIVER]
        self.mock_ov_client.firmware_drivers.get_by.return_value = firmwares
        self.mock_ansible_module.params = PARAMS_ABSENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FirmwareDriverModule.MSG_DELETED
        )

    def test_should_do_nothing_when_firmware_driver_not_exist(self):
        self.mock_ov_client.firmware_drivers.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_ABSENT

        FirmwareDriverModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FirmwareDriverModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
