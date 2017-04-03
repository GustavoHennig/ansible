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
from hpe_test_utils import OneViewBaseTestCase
from ansible.modules.cloud.hpe.oneview_fabric import FabricModule

FAKE_MSG_ERROR = 'Fake message error'
NO_CHANGE_MSG = 'No change found'


class FabricModuleSpec(unittest.TestCase,
                       OneViewBaseTestCase):

    PRESENT_FABRIC_VLAN_RANGE = dict(
        name="DefaultFabric",
        uri="/rest/fabrics/421fe408-589a-4a7e-91c5-a998e1cf3ec1",
        reservedVlanRange=dict(
            start=300,
            length=62
        ))

    FABRIC_PARAMS = dict(
        config="{{ config }}",
        state="reserved_vlan_range_updated",
        data=dict(
            name="DefaultFabric",
            reservedVlanRangeParameters=dict(
                start=300,
                length=67
            )
        )
    )

    FABRIC_PARAMS_DATA_IS_EQUALS = dict(
        config="{{ config }}",
        state="reserved_vlan_range_updated",
        data=dict(
            name="DefaultFabric",
            reservedVlanRangeParameters=dict(
                start=300,
                length=62
            )
        )
    )

    EXPECTED_FABRIC_VLAN_RANGE = dict(start=300, length=67)

    def setUp(self):
        self.configure_mocks(self, FabricModule)
        self.resource = self.mock_ov_client.fabrics

    def test_should_update_vlan_range(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = [self.PRESENT_FABRIC_VLAN_RANGE]
        self.resource.update_reserved_vlan_range.return_value = self.PRESENT_FABRIC_VLAN_RANGE

        # Mock Ansible params
        self.mock_ansible_module.params = self.FABRIC_PARAMS

        FabricModule().run()

        self.resource.update_reserved_vlan_range.assert_called_once_with(
            self.PRESENT_FABRIC_VLAN_RANGE["uri"],
            self.EXPECTED_FABRIC_VLAN_RANGE
        )

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            ansible_facts=dict(fabric=self.PRESENT_FABRIC_VLAN_RANGE)
        )

    def test_should_not_update_when_data_is_equals(self):
        # Mock OneView resource functions
        self.resource.get_by.return_value = [self.PRESENT_FABRIC_VLAN_RANGE]
        self.resource.update_reserved_vlan_range.return_value = self.PRESENT_FABRIC_VLAN_RANGE

        # Mock Ansible params
        self.mock_ansible_module.params = self.FABRIC_PARAMS_DATA_IS_EQUALS

        FabricModule().run()

        self.resource.update_reserved_vlan_range.not_been_called()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=NO_CHANGE_MSG,
            ansible_facts=dict(fabric=self.PRESENT_FABRIC_VLAN_RANGE)
        )
