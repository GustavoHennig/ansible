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

import copy
import unittest

from oneview_module_loader import ScopeFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Scope 2"
)

SCOPE_1 = dict(name="Scope 1", uri='/rest/scopes/a0336853-58d7-e021-b740-511cf971e21f0')
SCOPE_2 = dict(name="Scope 2", uri='/rest/scopes/b3213123-44sd-y334-d111-asd34sdf34df3')

ALL_SCOPES = [SCOPE_1, SCOPE_2]


class ScopeFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, ScopeFactsModule)
        self.resource = self.mock_ov_client.scopes

        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_should_get_all_scopes(self):
        self.resource.get_all.return_value = ALL_SCOPES
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_ALL)

        ScopeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(scopes=ALL_SCOPES)
        )

    def test_should_get_scope_by_name(self):
        self.resource.get_by_name.return_value = SCOPE_2
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_BY_NAME)

        ScopeFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(scopes=[SCOPE_2])
        )


if __name__ == '__main__':
    unittest.main()
