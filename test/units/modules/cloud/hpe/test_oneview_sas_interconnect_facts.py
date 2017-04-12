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

from oneview_module_loader import SasInterconnectFactsModule
from hpe_test_utils import FactsParamsTestCase

SAS_INTERCONNECT_1_NAME = '0000A66103, interconnect 1'

SAS_INTERCONNECT_1 = dict(
    name=SAS_INTERCONNECT_1_NAME,
    uri='/rest/sas-interconnects/2M220104SL'
)

SAS_INTERCONNECT_4 = dict(
    name='0000A66102, interconnect 4',
    uri='/rest/sas-interconnects/2M220103SL'
)

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name=SAS_INTERCONNECT_1_NAME
)


class SasInterconnectFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, SasInterconnectFactsModule)
        self.resource = self.mock_ov_client.sas_interconnects
        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_get_all_sas_interconnects(self):
        all_sas_interconnects = [SAS_INTERCONNECT_1, SAS_INTERCONNECT_4]

        self.resource.get_all.return_value = all_sas_interconnects

        self.mock_ansible_module.params = PARAMS_GET_ALL

        SasInterconnectFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnects=all_sas_interconnects)
        )

    def test_get_sas_interconnects_by_name(self):
        self.resource.get_by.return_value = [SAS_INTERCONNECT_1]

        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        SasInterconnectFactsModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_1_NAME)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_interconnects=[SAS_INTERCONNECT_1])
        )


if __name__ == '__main__':
    unittest.main()
