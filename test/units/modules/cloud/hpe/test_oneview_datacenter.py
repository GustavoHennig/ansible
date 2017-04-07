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

from oneview_module_loader import DatacenterModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

RACK_URI = '/rest/racks/rackid'

YAML_DATACENTER = """
        config: "{{ config }}"
        state: present
        data:
            name: "MyDatacenter"
            width: 5000
            depth: 6000
            contents:
                - resourceName: "Rack-221"
                  resourceUri: '/rest/racks/rackid'
                  x: 1000
                  y: 1000
          """

YAML_DATACENTER_CHANGE = """
        config: "{{ config }}"
        state: present
        data:
            name: "MyDatacenter"
            newName: "MyDatacenter1"
            width: 5000
            depth: 5000
            contents:
                - resourceUri: '/rest/racks/rackid'
                  x: 1000
                  y: 1000
      """

YAML_DATACENTER_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
            name: 'MyDatacenter'
        """

DICT_DEFAULT_DATACENTER = yaml.load(YAML_DATACENTER)["data"]
DICT_DEFAULT_DATACENTER_CHANGED = yaml.load(YAML_DATACENTER_CHANGE)["data"]


class DatacenterModuleSpec(unittest.TestCase,
                           OneViewBaseTestCase):
    """
    OneViewBaseTestCase has tests for the main function and provides the mocks used in this test case.
    """

    def setUp(self):
        self.configure_mocks(self, DatacenterModule)
        self.resource = self.mock_ov_client.datacenters

    def test_should_create_new_datacenter(self):
        self.resource.get_by.return_value = []
        self.resource.add.return_value = {"name": "name"}
        self.mock_ov_client.racks.get_by.return_value = [{'uri': RACK_URI}]

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DatacenterModule.MSG_CREATED,
            ansible_facts=dict(datacenter={"name": "name"})
        )

    def test_should_update_the_datacenter(self):
        self.resource.get_by.side_effect = [[DICT_DEFAULT_DATACENTER], []]
        self.resource.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER_CHANGE)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DatacenterModule.MSG_UPDATED,
            ansible_facts=dict(datacenter={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        datacenter_replaced = DICT_DEFAULT_DATACENTER.copy()
        del datacenter_replaced['contents'][0]['resourceName']

        self.resource.get_by.return_value = [DICT_DEFAULT_DATACENTER]
        self.mock_ov_client.racks.get_by.return_value = [{'uri': RACK_URI}]

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=DatacenterModule.MSG_ALREADY_EXIST,
            ansible_facts=dict(datacenter=DICT_DEFAULT_DATACENTER)
        )

    def test_should_remove_datacenter(self):
        self.resource.get_by.return_value = [DICT_DEFAULT_DATACENTER]

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER_ABSENT)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=DatacenterModule.MSG_DELETED
        )

    def test_should_do_nothing_when_datacenter_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER_ABSENT)

        DatacenterModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=DatacenterModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_switch_type_was_not_found(self):
        self.resource.get_by.return_value = []
        self.mock_ov_client.racks.get_by.return_value = []

        self.mock_ansible_module.params = yaml.load(YAML_DATACENTER)

        DatacenterModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=DatacenterModule.MSG_RACK_NOT_FOUND
        )


if __name__ == '__main__':
    unittest.main()
