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
from oneview_module_loader import InterconnectTypeFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="HP VC Flex-10 Enet Module"
)

PRESENT_TYPES = [{
    "name": "HP VC Flex-10 Enet Module",
    "uri": "/rest/interconnect-types/e6d938ac-0588-44c9-95f2-610f3da4a941"
}]


class InterconnectTypeFactsSpec(unittest.TestCase,
                                FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, InterconnectTypeFactsModule)
        self.interconnect_types = self.mock_ov_client.interconnect_types
        FactsParamsTestCase.configure_client_mock(self, self.interconnect_types)

    def test_should_get_all_interconnect_types(self):
        self.interconnect_types.get_all.return_value = PRESENT_TYPES

        self.mock_ansible_module.params = PARAMS_GET_ALL

        InterconnectTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_types=(PRESENT_TYPES))
        )

    def test_should_get_interconnect_type_by_name(self):
        self.interconnect_types.get_by.return_value = PRESENT_TYPES

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        InterconnectTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_types=(PRESENT_TYPES))
        )


if __name__ == '__main__':
    unittest.main()
