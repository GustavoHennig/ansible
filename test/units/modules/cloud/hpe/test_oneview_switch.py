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

from ansible.modules.cloud.hpe.oneview_switch import SwitchModule
from hpe_test_utils import OneViewBaseTestCase

SWITCH_NAME = "172.18.16.2"

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    name=SWITCH_NAME
)

PARAMS_PORTS_UPDATED = dict(
    config='config.json',
    state='ports_updated',
    name=SWITCH_NAME,
    data=[
        dict(
            portId="ca520119-1329-496b-8e44-43092e937eae:1.21",
            portName="1.21",
            enabled=True
        )
    ]
)

SWITCH = dict(
    name=SWITCH_NAME,
    uri="/rest/switches/ca520119-1329-496b-8e44-43092e937eae"
)


class SwitchModuleSpec(unittest.TestCase,
                       OneViewBaseTestCase):

    def setUp(self):
        self.configure_mocks(self, SwitchModule)
        self.resource = self.mock_ov_client.switches

    def test_should_remove_switch(self):
        self.resource.get_by.return_value = [SWITCH]
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        SwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SwitchModule.MSG_DELETED
        )

    def test_should_do_nothing_when_switch_not_exist(self):
        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        SwitchModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SwitchModule.MSG_NOT_FOUND
        )

    def test_should_update_switch_ports(self):
        self.resource.get_by.return_value = [SWITCH]
        self.mock_ansible_module.params = PARAMS_PORTS_UPDATED

        SwitchModule().run()

        self.resource.update_ports.assert_called_once_with(
            id_or_uri=SWITCH["uri"],
            ports=PARAMS_PORTS_UPDATED["data"]
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SwitchModule.MSG_PORTS_UPDATED
        )


if __name__ == '__main__':
    unittest.main()
