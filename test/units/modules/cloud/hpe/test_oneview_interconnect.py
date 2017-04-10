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

from oneview_module_loader import InterconnectModule
from hpe_test_utils import OneViewBaseTestCase


def create_params_for(power_state):
    return dict(
        config='config.json',
        state=power_state,
        name='Encl1, interconnect 1',
        ip=None
    )


class InterconnectModuleSpec(unittest.TestCase,
                             OneViewBaseTestCase):

    FAKE_URI = "/rest/interconnects/748d4699-62ff-454e-8ec8-773815c4aa2f"

    INTERCONNECT_IP = '172.18.1.114'

    INTERCONNECT_ID = "748d4699-62ff-454e-8ec8-773815c4aa2f"

    PORT_D1 = {
        "type": "port",
        "portName": "d1",
        "bayNumber": 1,
        "enabled": False,
        "portId": "{0}:d1".format(INTERCONNECT_ID)
    }

    PORT_D2 = {
        "portName": "d2",
        "enabled": False,
        "portId": "{0}:d2".format(INTERCONNECT_ID)
    }

    PORTS_FOR_UPDATE = [PORT_D1, PORT_D2]

    PARAMS_FOR_RESET_DEVICE_BY_IP = dict(
        config='config.json',
        state='device_reset',
        name=None,
        ip=INTERCONNECT_IP
    )

    PARAMS_FOR_UPDATE_PORTS = dict(
        config='config.json',
        state='update_ports',
        name=None,
        ip=INTERCONNECT_IP,
        ports=PORTS_FOR_UPDATE
    )

    PARAMS_FOR_RESET_PORT_PROTECTION = dict(
        config='config.json',
        state='reset_port_protection',
        name=None,
        ip=INTERCONNECT_IP
    )

    def setUp(self):
        self.configure_mocks(self, InterconnectModule)

    def test_should_ensure_powered_on_state(self):
        ansible_arguments = create_params_for('powered_on')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = [dict(powerState='Off', uri=self.FAKE_URI)]

        fake_interconnect_updated = dict(powerState='On')
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect_updated

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=self.FAKE_URI,
            operation='replace',
            path='/powerState',
            value='On'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect_updated)
        )

    def test_should_return_changed_false_when_interconnect_is_already_powered_on(self):
        ansible_arguments = create_params_for('powered_on')
        self.mock_ansible_module.params = ansible_arguments

        fake_interconnect = dict(powerState='On')
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]

        InterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_ensure_powered_off_state(self):
        ansible_arguments = create_params_for('powered_off')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = [dict(powerState='On', uri=self.FAKE_URI)]

        fake_interconnect_updated = dict(powerState='Off')
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect_updated

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=self.FAKE_URI,
            operation='replace',
            path='/powerState',
            value='Off'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect_updated)
        )

    def test_should_ensure_uid_on_state(self):
        ansible_arguments = create_params_for('uid_on')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = [dict(uidState='Off', uri=self.FAKE_URI)]

        fake_interconnect_updated = dict(uidState='On')
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect_updated

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=self.FAKE_URI,
            operation='replace',
            path='/uidState',
            value='On'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect_updated)
        )

    def test_should_return_changed_false_when_uid_is_already_on(self):
        ansible_arguments = create_params_for('uid_on')
        self.mock_ansible_module.params = ansible_arguments

        fake_interconnect = dict(uidState='On')
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]

        InterconnectModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_ensure_uid_off_state(self):
        ansible_arguments = create_params_for('uid_off')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = [dict(uidState='On', uri=self.FAKE_URI)]

        fake_interconnect_updated = dict(uidState='Off')
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect_updated

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=self.FAKE_URI,
            operation='replace',
            path='/uidState',
            value='Off'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect_updated)
        )

    def test_should_ensure_device_reset(self):
        ansible_arguments = create_params_for('device_reset')
        self.mock_ansible_module.params = ansible_arguments

        fake_interconnect = dict(uri=self.FAKE_URI)

        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect

        InterconnectModule().run()

        self.mock_ov_client.interconnects.patch.assert_called_with(
            id_or_uri=self.FAKE_URI,
            operation='replace',
            path='/deviceResetState',
            value='Reset'
        )
        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_fail_when_interconnect_was_not_found(self):
        ansible_arguments = create_params_for('device_reset')
        self.mock_ansible_module.params = ansible_arguments

        self.mock_ov_client.interconnects.get_by.return_value = []

        InterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=InterconnectModule.MSG_INTERCONNECT_NOT_FOUND
        )

    def test_should_ensure_device_reset_by_ip_address(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_RESET_DEVICE_BY_IP

        fake_interconnect = dict(uri=self.FAKE_URI)
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]
        self.mock_ov_client.interconnects.patch.return_value = fake_interconnect

        InterconnectModule().run()

        self.mock_ov_client.interconnects.get_by.assert_called_with('interconnectIP', self.INTERCONNECT_IP)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_fail_when_no_key_is_provided(self):
        params = self.PARAMS_FOR_RESET_DEVICE_BY_IP.copy()
        params['ip'] = None

        self.mock_ansible_module.params = params

        InterconnectModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=InterconnectModule.MSG_MISSING_KEY)

    def test_should_update_the_interconnect_ports(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_UPDATE_PORTS

        fake_interconnect = dict(uri=self.FAKE_URI)
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]
        self.mock_ov_client.interconnects.update_ports.return_value = fake_interconnect

        InterconnectModule().run()

        self.mock_ov_client.interconnects.get_by.assert_called_with('interconnectIP', self.INTERCONNECT_IP)
        self.mock_ov_client.interconnects.update_ports.assert_called_with(ports=self.PORTS_FOR_UPDATE,
                                                                          id_or_uri=self.FAKE_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect)
        )

    def test_should_reset_port_protection(self):
        self.mock_ansible_module.params = self.PARAMS_FOR_RESET_PORT_PROTECTION

        fake_interconnect = dict(uri=self.FAKE_URI)
        self.mock_ov_client.interconnects.get_by.return_value = [fake_interconnect]
        self.mock_ov_client.interconnects.reset_port_protection.return_value = fake_interconnect

        InterconnectModule().run()

        self.mock_ov_client.interconnects.get_by.assert_called_with('interconnectIP', self.INTERCONNECT_IP)
        self.mock_ov_client.interconnects.reset_port_protection.assert_called_with(id_or_uri=self.FAKE_URI)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(interconnect=fake_interconnect)
        )


if __name__ == '__main__':
    unittest.main()
