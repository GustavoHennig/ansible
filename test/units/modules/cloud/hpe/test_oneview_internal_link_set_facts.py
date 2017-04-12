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
from oneview_module_loader import InternalLinkSetFactsModule
from hpe_test_utils import FactsParamsTestCase


ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="ILS58"
)

INTERNAL_LINK_SETS = [{"name": "ILS56"}, {"name": "ILS58"}, {"name": "ILS100"}]


class InternalLinkSetFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, InternalLinkSetFactsModule)
        self.internal_link_sets = self.mock_ov_client.internal_link_sets
        FactsParamsTestCase.configure_client_mock(self, self.internal_link_sets)

    def test_should_get_all_internal_link_sets(self):
        self.internal_link_sets.get_all.return_value = INTERNAL_LINK_SETS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        InternalLinkSetFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(internal_link_sets=(INTERNAL_LINK_SETS))
        )

    def test_should_get_by_name(self):
        self.internal_link_sets.get_by.return_value = [INTERNAL_LINK_SETS[1]]
        self.mock_ansible_module.params = PARAMS_GET_BY_NAME

        InternalLinkSetFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(internal_link_sets=([INTERNAL_LINK_SETS[1]]))
        )


if __name__ == '__main__':
    unittest.main()
