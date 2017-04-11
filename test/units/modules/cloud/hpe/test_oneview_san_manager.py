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

from oneview_module_loader import SanManagerModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_SAN_MANAGER_TEMPLATE = dict(
    providerDisplayName='Brocade Network Advisor',
    uri='/rest/fc-sans/device-managers/UUU-AAA-BBB',
    connectionInfo=[
        {
            'valueFormat': 'IPAddressOrHostname',
            'displayName': 'Host',
            'name': 'Host',
            'valueType': 'String',
            'required': False,
            'value': '172.18.15.1'
        }]
)


class SanManagerModuleSpec(unittest.TestCase,
                           OneViewBaseTestCase):
    PARAMS_FOR_PRESENT = dict(
        config='config.json',
        state='present',
        data=dict(providerDisplayName=DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName'])
    )

    PARAMS_WITH_CHANGES = dict(
        config='config.json',
        state='present',
        data=dict(providerDisplayName=DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName'],
                  refreshState='RefreshPending')
    )

    PARAMS_FOR_ABSENT = dict(
        config='config.json',
        state='absent',
        data=dict(providerDisplayName=DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName'])
    )

    def setUp(self):
        self.configure_mocks(self, SanManagerModule)
        self.resource = self.mock_ov_client.san_managers

    def test_should_add_new_san_manager(self):
        self.resource.get_by_provider_display_name.return_value = None
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'
        self.resource.add.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_CREATED,
            ansible_facts=dict(san_manager=DEFAULT_SAN_MANAGER_TEMPLATE)
        )

    def test_should_find_provider_uri_to_add(self):
        self.resource.get_by_provider_display_name.return_value = None
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'
        self.resource.add.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        provider_display_name = DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName']
        self.resource.get_provider_uri.assert_called_once_with(provider_display_name)

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SanManagerModule.MSG_ALREADY_EXIST,
            ansible_facts=dict(san_manager=DEFAULT_SAN_MANAGER_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_SAN_MANAGER_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        self.resource.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.resource.update.return_value = data_merged
        self.mock_ansible_module.params = self.PARAMS_WITH_CHANGES

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_UPDATED,
            ansible_facts=dict(san_manager=data_merged)
        )

    def test_update_when_should_not_send_connection_info_when_not_informed_on_data(self):
        merged_data = dict(providerDisplayName='Brocade Network Advisor',
                           uri='/rest/fc-sans/device-managers/UUU-AAA-BBB',
                           refreshState='RefreshPending')

        self.resource.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE
        self.resource.update.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_WITH_CHANGES

        SanManagerModule().run()

        self.resource.update.assert_called_once_with(resource=merged_data, id_or_uri=merged_data['uri'])

    def test_should_remove_san_manager(self):
        self.resource.get_by_provider_display_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_ABSENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_DELETED
        )

    def test_should_do_nothing_when_san_manager_not_exist(self):
        self.resource.get_by_provider_display_name.return_value = None

        self.mock_ansible_module.params = self.PARAMS_FOR_ABSENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SanManagerModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_provider_display_name_not_found(self):
        self.resource.get_by_provider_display_name.return_value = None
        self.resource.get_provider_uri.return_value = None

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg="The provider 'Brocade Network Advisor' was not found."
        )


if __name__ == '__main__':
    unittest.main()
