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
from oneview_module_loader import StoragePoolFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Storage Pools"
)


class StoragePoolFactsSpec(unittest.TestCase,
                           FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, StoragePoolFactsModule)
        self.storage_pools = self.mock_ov_client.storage_pools
        FactsParamsTestCase.configure_client_mock(self, self.storage_pools)

    def test_should_get_all_storage_pool(self):
        self.storage_pools.get_all.return_value = {"name": "Storage Pool Name"}
        self.mock_ansible_module.params = PARAMS_GET_ALL

        StoragePoolFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_pools=({"name": "Storage Pool Name"}))
        )

    def test_should_get_storage_pool_by_name(self):
        self.storage_pools.get_by.return_value = {"name": "Storage Pool Name"}
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        StoragePoolFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(storage_pools=({"name": "Storage Pool Name"}))
        )


if __name__ == '__main__':
    unittest.main()
