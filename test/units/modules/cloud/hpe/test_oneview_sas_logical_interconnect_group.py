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

from oneview_module_loader import (SasLogicalInterconnectGroupModule)
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'
DEFAULT_SAS_LIG_NAME = 'Test SAS Logical Interconnect Group'
RENAMED_SAS_LIG = 'Renamed SAS Logical Interconnect Group'

DEFAULT_SAS_LIG_TEMPLATE = dict(
    type='sas-logical-interconnect-group',
    name=DEFAULT_SAS_LIG_NAME,
    state='Active',
    enclosureType='SY12000',
    interconnectBaySet="1"
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SAS_LIG_NAME)
)

PARAMS_TO_RENAME = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SAS_LIG_NAME,
              newName=RENAMED_SAS_LIG)
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_SAS_LIG_NAME,
              interconnectBaySet='2')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_SAS_LIG_NAME)
)


class SasLogicalInterconnectGroupSpec(unittest.TestCase,
                                      OneViewBaseTestCase):
    """
    OneViewBaseTestCase has common tests for the main function attribute, also provides the mocks used in this test
    case.
    """

    def setUp(self):
        self.configure_mocks(self, SasLogicalInterconnectGroupModule)
        self.resource = self.mock_ov_client.sas_logical_interconnect_groups

    def test_should_create(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = DEFAULT_SAS_LIG_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectGroupModule.MSG_CREATED,
            ansible_facts=dict(sas_logical_interconnect_group=DEFAULT_SAS_LIG_TEMPLATE)
        )

    def test_create_with_newName_when_resource_not_exists(self):
        data_merged = DEFAULT_SAS_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_SAS_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        self.resource.get_by.return_value = []
        self.resource.create.return_value = DEFAULT_SAS_LIG_TEMPLATE

        self.mock_ansible_module.params = params_to_rename

        SasLogicalInterconnectGroupModule().run()

        self.resource.create.assert_called_once_with(PARAMS_TO_RENAME['data'])

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasLogicalInterconnectGroupModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(sas_logical_interconnect_group=DEFAULT_SAS_LIG_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_SAS_LIG_TEMPLATE.copy()
        data_merged['description'] = 'New description'

        self.resource.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectGroupModule.MSG_UPDATED,
            ansible_facts=dict(sas_logical_interconnect_group=data_merged)
        )

    def test_rename_when_resource_exists(self):
        data_merged = DEFAULT_SAS_LIG_TEMPLATE.copy()
        data_merged['name'] = RENAMED_SAS_LIG
        params_to_rename = PARAMS_TO_RENAME.copy()

        self.resource.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = params_to_rename

        SasLogicalInterconnectGroupModule().run()

        self.resource.update.assert_called_once_with(data_merged)

    def test_should_remove(self):
        self.resource.get_by.return_value = [DEFAULT_SAS_LIG_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SasLogicalInterconnectGroupModule.MSG_DELETED
        )

    def test_should_do_nothing_when_resource_not_exist(self):
        self.resource.get_by.return_value = []
        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        SasLogicalInterconnectGroupModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SasLogicalInterconnectGroupModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
