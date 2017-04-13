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

from ansible.modules.cloud.hpe.oneview_server_hardware_type_facts import ServerHardwareTypeFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="MyServerHardwareType"
)

PARAMS_GET_ALL = dict(
    config='config.json',
)


class ServerHardwareTypeFactsSpec(unittest.TestCase,
                                  FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, ServerHardwareTypeFactsModule)
        self.server_hardware_types = self.mock_ov_client.server_hardware_types
        FactsParamsTestCase.configure_client_mock(self, self.server_hardware_types)

    def test_should_get_all(self):
        self.server_hardware_types.get_all.return_value = {"name": "Server Hardware Type Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        ServerHardwareTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardware_types=({"name": "Server Hardware Type Name"}))
        )

    def test_should_get_server_hardware_type_by_name(self):
        self.server_hardware_types.get_by.return_value = [{"name": "Server Hardware Type Name"}]
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        ServerHardwareTypeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(server_hardware_types=([{"name": "Server Hardware Type Name"}]))
        )


if __name__ == '__main__':
    unittest.main()
