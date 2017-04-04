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

from ansible.modules.cloud.hpe.image_streamer_plan_script_facts import PlanScriptFactsModule, EXAMPLES
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'


class PlanScriptFactsSpec(unittest.TestCase,
                          FactsParamsTestCase):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """

    def setUp(self):
        self.configure_mocks(self, PlanScriptFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        FactsParamsTestCase.configure_client_mock(self, self.i3s.plan_scripts)

        # Load scenarios from module examples
        self.PLAN_SCRIPT_FACTS_EXAMPLES = yaml.load(EXAMPLES)

        self.TASK_GET_ALL = self.PLAN_SCRIPT_FACTS_EXAMPLES[0]['image_streamer_plan_script_facts']
        self.TASK_GET_BY_NAME = self.PLAN_SCRIPT_FACTS_EXAMPLES[4]['image_streamer_plan_script_facts']

        self.PLAN_SCRIPT = dict(
            name="Plan Script name",
            uri="/rest/plan-scripts/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_get_all_plan_scripts(self):
        self.i3s.plan_scripts.get_all.return_value = [self.PLAN_SCRIPT]
        self.mock_ansible_module.params = self.TASK_GET_ALL

        PlanScriptFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(plan_scripts=[self.PLAN_SCRIPT])
        )

    def test_get_a_plan_script_by_name(self):
        self.i3s.plan_scripts.get_by.return_value = [self.PLAN_SCRIPT]
        self.mock_ansible_module.params = self.TASK_GET_BY_NAME

        PlanScriptFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(plan_scripts=[self.PLAN_SCRIPT])
        )


if __name__ == '__main__':
    unittest.main()
