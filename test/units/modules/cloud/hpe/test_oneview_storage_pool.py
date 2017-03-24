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

from ansible.modules.cloud.hpe.oneview_storage_pool import StoragePoolModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

YAML_STORAGE_POOL = """
        config: "{{ config }}"
        state: present
        data:
           storageSystemUri: "/rest/storage-systems/TXQ1010307"
           poolName: "FST_CPG2"
          """

YAML_STORAGE_POOL_MISSING_KEY = """
    config: "{{ config }}"
    state: present
    data:
       storageSystemUri: "/rest/storage-systems/TXQ1010307"
      """

YAML_STORAGE_POOL_ABSENT = """
        config: "{{ config }}"
        state: absent
        data:
           poolName: "FST_CPG2"
        """

DICT_DEFAULT_STORAGE_POOL = yaml.load(YAML_STORAGE_POOL)["data"]


class StoragePoolModuleSpec(unittest.TestCase,
                            OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, StoragePoolModule)

    def test_should_create_new_storage_pool(self):
        self.mock_ov_client.storage_pools.get_by.return_value = []
        self.mock_ov_client.storage_pools.add.return_value = {"name": "name"}
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StoragePoolModule.MSG_ADDED,
            ansible_facts=dict(storage_pool={"name": "name"})
        )

    def test_should_do_nothing_when_storage_pool_already_exist(self):
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StoragePoolModule.MSG_ALREADY_ADDED,
            ansible_facts=dict(storage_pool=DICT_DEFAULT_STORAGE_POOL)
        )

    def test_should_remove_storage_pool(self):
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_ABSENT)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StoragePoolModule.MSG_DELETED
        )

    def test_should_do_nothing_when_storage_pool_not_exist(self):
        self.mock_ov_client.storage_pools.get_by.return_value = []
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_ABSENT)

        StoragePoolModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=StoragePoolModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_key_is_missing(self):
        self.mock_ov_client.storage_pools.get_by.return_value = [DICT_DEFAULT_STORAGE_POOL]
        self.mock_ansible_module.params = yaml.load(YAML_STORAGE_POOL_MISSING_KEY)

        StoragePoolModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=StoragePoolModule.MSG_MANDATORY_FIELD_MISSING
        )


if __name__ == '__main__':
    unittest.main()
