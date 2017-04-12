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

from oneview_module_loader import DriveEnclosureFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

DICT_DEFAULT_DRIVE_ENCLOSURE = {
    'name': '/rest/drive-enclosures/SN123101',
    'powerState': 'On',
    'status': 'OK',
    'type': 'drive-enclosure',
    'uidState': 'Off',
    'uri': '0000A66102, bay 1'
}

MOCK_DRIVE_ENCLOSURES = [
    DICT_DEFAULT_DRIVE_ENCLOSURE,
    DICT_DEFAULT_DRIVE_ENCLOSURE
]

MOCK_PORT_MAP = {
    "type": "DriveEnclosurePortMap"
}

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test-Enclosure",
    options=[]
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test-Enclosure",
    options=['portMap']
)


class DriveEnclosureFactsSpec(unittest.TestCase,
                              FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, DriveEnclosureFactsModule)
        self.drive_enclosures = self.mock_ov_client.drive_enclosures

        FactsParamsTestCase.configure_client_mock(self, self.drive_enclosures)

    def test_should_get_all(self):
        self.drive_enclosures.get_all.return_value = MOCK_DRIVE_ENCLOSURES

        self.mock_ansible_module.params = PARAMS_GET_ALL

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=MOCK_DRIVE_ENCLOSURES)
        )

    def test_should_get_by_name(self):
        self.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=[DICT_DEFAULT_DRIVE_ENCLOSURE])
        )

    def test_should_get_by_name_with_options(self):
        self.drive_enclosures.get_by.return_value = [DICT_DEFAULT_DRIVE_ENCLOSURE]
        self.drive_enclosures.get_port_map.return_value = MOCK_PORT_MAP

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        DriveEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(drive_enclosures=[DICT_DEFAULT_DRIVE_ENCLOSURE],
                               drive_enclosure_port_map=MOCK_PORT_MAP)
        )


if __name__ == '__main__':
    unittest.main()
