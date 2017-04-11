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

from oneview_module_loader import SasInterconnectModule
from hpe_test_utils import OneViewBaseTestCase

SAS_INTERCONNECT_NAME = "0000A66103, interconnect 4"
SAS_INTERCONNECT_URI = '/rest/sas-interconnects/3518be0e-17c1-4189-8f81-83f3724f6155'

REFRESH_CONFIGURATION = dict(refreshState="RefreshPending")

SAS_INTERCONNECT = dict(
    name=SAS_INTERCONNECT_NAME,
    uri=SAS_INTERCONNECT_URI
)


class StateCheck(object):
    def __init__(self, state_name):
        self.msg = SasInterconnectModule.states_success_message[state_name]
        self.state = SasInterconnectModule.states[state_name]
        self.params = dict(
            config='config.json',
            state=state_name,
            name=SAS_INTERCONNECT_NAME
        )


class SasInterconnectModuleSpec(unittest.TestCase,
                                OneViewBaseTestCase):
    """
    ModuleContructorTestCase has common tests for class constructor and main function,
    also provides the mocks used in this test case

    ErrorHandlingTestCase has common tests for the module error handling.
    """

    def setUp(self):
        self.configure_mocks(self, SasInterconnectModule)
        self.resource = self.mock_ov_client.sas_interconnects

    def test_should_refresh_the_sas_interconnect(self):
        state_check = StateCheck('refreshed')

        self.resource.get_by.return_value = [SAS_INTERCONNECT]
        self.resource.refresh_state.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)

        self.resource.refresh_state.assert_called_once_with(
            id_or_uri=SAS_INTERCONNECT_URI,
            configuration=REFRESH_CONFIGURATION
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_turn_on_the_uid_when_uid_is_off(self):
        sas_interconnect = dict(uidState='Off', **SAS_INTERCONNECT)

        state_check = StateCheck('uid_on')

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_uid_is_already_on(self):
        sas_interconnect = dict(uidState='On', **SAS_INTERCONNECT)
        state_check = StateCheck('uid_on')

        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasInterconnectModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_fail_when_interconnect_not_found(self):
        state_check = StateCheck('uid_on')

        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=SasInterconnectModule.MSG_NOT_FOUND,
        )

    def test_should_turn_off_the_uid_when_uid_is_on(self):
        sas_interconnect = dict(uidState='On', **SAS_INTERCONNECT)
        state_check = StateCheck('uid_off')

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_uid_is_already_off(self):
        sas_interconnect = dict(uidState='Off', **SAS_INTERCONNECT)
        state_check = StateCheck('uid_off')

        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasInterconnectModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_turn_the_power_off_when_the_sas_interconnect_is_powered_on(self):
        sas_interconnect = dict(powerState='On', **SAS_INTERCONNECT)
        state_check = StateCheck('powered_off')

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_the_sas_interconnect_is_already_powered_off(self):
        sas_interconnect = dict(powerState='Off', **SAS_INTERCONNECT)
        state_check = StateCheck('powered_off')

        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasInterconnectModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_turn_the_power_on_when_the_sas_interconnect_is_powered_off(self):
        state_check = StateCheck('powered_on')

        sas_interconnect = dict(powerState='Off', **SAS_INTERCONNECT)

        self.resource.get_by.return_value = [sas_interconnect]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_do_nothing_when_the_sas_interconnect_is_already_powered_on(self):
        sas_interconnect = dict(powerState='On', **SAS_INTERCONNECT)
        state_check = StateCheck('powered_on')

        self.resource.get_by.return_value = [sas_interconnect]
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_not_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasInterconnectModule.MSG_NOTHING_TO_DO,
            ansible_facts=dict(sas_interconnect=sas_interconnect)
        )

    def test_should_perform_soft_reset(self):
        state_check = StateCheck('soft_reset')

        self.resource.get_by.return_value = [SAS_INTERCONNECT]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )

    def test_should_perform_hard_reset(self):
        state_check = StateCheck('hard_reset')

        self.resource.get_by.return_value = [SAS_INTERCONNECT]
        self.resource.patch.return_value = SAS_INTERCONNECT
        self.mock_ansible_module.params = state_check.params

        SasInterconnectModule().run()

        self.resource.get_by.assert_called_once_with('name', SAS_INTERCONNECT_NAME)
        self.resource.patch.assert_called_once_with(id_or_uri=SAS_INTERCONNECT_URI, **state_check.state)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=state_check.msg,
            ansible_facts=dict(sas_interconnect=SAS_INTERCONNECT)
        )


if __name__ == '__main__':
    unittest.main()
