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

from ansible.modules.cloud.hpe.oneview_fc_network import FcNetworkModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_FC_NETWORK_TEMPLATE = dict(
    name='New FC Network 2',
    autoLoginRedistribution=True,
    fabricType='FabricAttach'
)

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'])
)

PARAMS_WITH_CHANGES = dict(
    config='config.json',
    state='present',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'],
              newName="New Name",
              fabricType='DirectAttach')
)

PARAMS_FOR_ABSENT = dict(
    config='config.json',
    state='absent',
    data=dict(name=DEFAULT_FC_NETWORK_TEMPLATE['name'])
)


class FcNetworkModuleSpec(unittest.TestCase,
                          OneViewBaseTestCase):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, FcNetworkModule)
        self.resource = self.mock_ov_client.fc_networks

    def test_should_create_new_fc_network(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = DEFAULT_FC_NETWORK_TEMPLATE

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_CREATED,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by.return_value = [DEFAULT_FC_NETWORK_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FcNetworkModule.MSG_ALREADY_EXIST,
            ansible_facts=dict(fc_network=DEFAULT_FC_NETWORK_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_FC_NETWORK_TEMPLATE.copy()

        data_merged['fabricType'] = 'DirectAttach'

        self.resource.get_by.return_value = [DEFAULT_FC_NETWORK_TEMPLATE]
        self.resource.update.return_value = data_merged

        self.mock_ansible_module.params = PARAMS_WITH_CHANGES

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_UPDATED,
            ansible_facts=dict(fc_network=data_merged)
        )

    def test_should_remove_fc_network(self):
        self.resource.get_by.return_value = [DEFAULT_FC_NETWORK_TEMPLATE]

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=FcNetworkModule.MSG_DELETED
        )

    def test_should_do_nothing_when_fc_network_not_exist(self):
        self.resource.get_by.return_value = []

        self.mock_ansible_module.params = PARAMS_FOR_ABSENT

        FcNetworkModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=FcNetworkModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()