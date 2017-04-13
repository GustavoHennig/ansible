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
import yaml

from oneview_module_loader import LogicalSwitchGroupModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

SWITCH_TYPE_URI = '/rest/switch-types/2f36bc8f-65d8-4ea2-9300-750180402a5e'

YAML_LOGICAL_SWITCH_GROUP = """
        config: "{{ config }}"
        state: present
        data:
            type: "logical-switch-group"
            name: "OneView Test Logical Switch Group"
            switchMapTemplate:
                switchMapEntryTemplates:
                    - logicalLocation:
                        locationEntries:
                           - relativeValue: 1
                             type: "StackingMemberId"
                      permittedSwitchTypeName: 'Switch Type Name'
                      permittedSwitchTypeUri: '/rest/switch-types/2f36bc8f-65d8-4ea2-9300-750180402a5e'
          """

YAML_LOGICAL_SWITCH_GROUP_CHANGE = """
        config: "{{ config }}"
        state: present
        data:
            type: "logical-switch-group"
            name: "OneView Test Logical Switch Group"
            newName: "OneView Test Logical Switch Group (Changed)"
            switchMapTemplate:
                switchMapEntryTemplates:
                    - logicalLocation:
                        locationEntries:
                           - relativeValue: 1
                             type: "StackingMemberId"
                      permittedSwitchTypeUri: '/rest/switch-types/2f36bc8f-65d8-4ea2-9300-750180402a5e'
      """

YAML_LOGICAL_SWITCH_GROUP_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name: '{{storage_vol_templ_name}}'
        """

DICT_DEFAULT_LOGICAL_SWITCH_GROUP = yaml.load(YAML_LOGICAL_SWITCH_GROUP)["data"]
DICT_DEFAULT_LOGICAL_SWITCH_GROUP_CHANGED = yaml.load(YAML_LOGICAL_SWITCH_GROUP_CHANGE)["data"]


class LogicalSwitchModuleSpec(unittest.TestCase,
                              OneViewBaseTestCase):
    """
    OneViewBaseTestCase has a common test for the main function,
    also provides the mocks used in this test case.
    """

    def setUp(self):
        self.configure_mocks(self, LogicalSwitchGroupModule)
        self.resource = self.mock_ov_client.logical_switch_groups

    def test_should_create_new_logical_switch_group(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = {"name": "name"}
        self.mock_ov_client.switch_types.get_by.return_value = [{'uri': SWITCH_TYPE_URI}]

        self.mock_ansible_module.params = yaml.load(YAML_LOGICAL_SWITCH_GROUP)

        LogicalSwitchGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalSwitchGroupModule.MSG_CREATED,
            ansible_facts=dict(logical_switch_group={"name": "name"})
        )

    def test_should_update_the_logical_switch_group(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_LOGICAL_SWITCH_GROUP]
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_LOGICAL_SWITCH_GROUP_CHANGE)

        LogicalSwitchGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalSwitchGroupModule.MSG_UPDATED,
            ansible_facts=dict(logical_switch_group={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        switch_type_replaced = DICT_DEFAULT_LOGICAL_SWITCH_GROUP.copy()
        del switch_type_replaced['switchMapTemplate']['switchMapEntryTemplates'][0]['permittedSwitchTypeName']

        self.resource.get_by.return_value = [DICT_DEFAULT_LOGICAL_SWITCH_GROUP]
        self.mock_ov_client.switch_types.get_by.return_value = [{'uri': SWITCH_TYPE_URI}]

        self.mock_ansible_module.params = yaml.load(YAML_LOGICAL_SWITCH_GROUP)

        LogicalSwitchGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalSwitchGroupModule.MSG_ALREADY_EXIST,
            ansible_facts=dict(logical_switch_group=DICT_DEFAULT_LOGICAL_SWITCH_GROUP)
        )

    def test_should_remove_logical_switch_group(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_LOGICAL_SWITCH_GROUP]

        self.mock_ansible_module.params = yaml.load(YAML_LOGICAL_SWITCH_GROUP_ABSENT)

        LogicalSwitchGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=LogicalSwitchGroupModule.MSG_DELETED
        )

    def test_should_do_nothing_when_logical_switch_group_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_LOGICAL_SWITCH_GROUP_ABSENT)

        LogicalSwitchGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=LogicalSwitchGroupModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_switch_type_was_not_found(self):
        self.resource.get_by.return_value = []
        self.mock_ov_client.switch_types.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_LOGICAL_SWITCH_GROUP)

        LogicalSwitchGroupModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=LogicalSwitchGroupModule.MSG_SWITCH_TYPE_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
