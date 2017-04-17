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

from oneview_module_loader import InterconnectLinkTopologyFactsModule
from hpe_test_utils import FactsParamsTestCase


class InterconnectLinkTopologyFactsSpec(unittest.TestCase,
                                        FactsParamsTestCase):

    INTERCONNECT_LINK_TOPOLOGIES = [{"name": "Interconnect Link Topology 1"},
                                    {"name": "Interconnect Link Topology 2"},
                                    {"name": "Interconnect Link Topology 3"}]

    ERROR_MSG = 'Fake message error'

    PARAMS_GET_ALL = dict(
        config='config.json',
        name=None
    )

    PARAMS_GET_BY_NAME = dict(
        config='config.json',
        name="Interconnect Link Topology Name 2"
    )

    def setUp(self):
        self.configure_mocks(self, InterconnectLinkTopologyFactsModule)
        self.interconnect_link_topologies = self.mock_ov_client.interconnect_link_topologies
        FactsParamsTestCase.configure_client_mock(self, self.interconnect_link_topologies)

    def test_should_get_all_interconnect_link_topologies(self):
        self.interconnect_link_topologies.get_all.return_value = self.INTERCONNECT_LINK_TOPOLOGIES
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        InterconnectLinkTopologyFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_link_topologies=(self.INTERCONNECT_LINK_TOPOLOGIES))
        )

    def test_should_get_all_interconnect_link_topology_by_name(self):
        self.interconnect_link_topologies.get_by.return_value = [self.INTERCONNECT_LINK_TOPOLOGIES[1]]
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        InterconnectLinkTopologyFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(interconnect_link_topologies=([self.INTERCONNECT_LINK_TOPOLOGIES[1]]))
        )


if __name__ == '__main__':
    unittest.main()
