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

from ansible.modules.cloud.hpe.oneview_logical_enclosure_facts import LogicalEnclosureFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

LOGICAL_ENCLOSURE = {"uri": "/rest/logical-enclosures/a0a5d4a1-c4a7-4c9b-b05d-feb0a9d8190d",
                     "name": "Logical Enclosure Name"}

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Logical Enclosures",
    options=None
)

PARAMS_GET_BY_NAME_WITH_OPTIONS = dict(
    config='config.json',
    name="Test Logical Enclosures",
    options=['script']
)


class LogicalEnclosureFactsSpec(unittest.TestCase,
                                FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, LogicalEnclosureFactsModule)
        self.logical_enclosures = self.mock_ov_client.logical_enclosures
        FactsParamsTestCase.configure_client_mock(self, self.logical_enclosures)

    def test_should_get_all_logical_enclosure(self):
        self.logical_enclosures.get_all.return_value = [LOGICAL_ENCLOSURE]

        self.mock_ansible_module.params = PARAMS_GET_ALL

        LogicalEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_enclosures=([LOGICAL_ENCLOSURE]))
        )

    def test_should_get_logical_enclosure_by_name(self):
        self.logical_enclosures.get_by.return_value = [LOGICAL_ENCLOSURE]

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        LogicalEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_enclosures=[LOGICAL_ENCLOSURE])
        )

    def test_should_get_logical_enclosure_by_name_with_options(self):
        self.logical_enclosures.get_by.return_value = [LOGICAL_ENCLOSURE]
        self.logical_enclosures.get_script.return_value = "# script code"

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME_WITH_OPTIONS

        LogicalEnclosureFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(logical_enclosures=[LOGICAL_ENCLOSURE],
                               logical_enclosure_script="# script code")
        )


if __name__ == '__main__':
    unittest.main()
