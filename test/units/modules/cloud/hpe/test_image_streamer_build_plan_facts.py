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

from ansible.modules.cloud.hpe.image_streamer_build_plan_facts import BuildPlanFactsModule, EXAMPLES
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'


class BuildPlanFactsSpec(unittest.TestCase,
                         FactsParamsTestCase):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """
    def setUp(self):
        self.configure_mocks(self, BuildPlanFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        FactsParamsTestCase.configure_client_mock(self, self.i3s.build_plans)

        # Load scenarios from module examples
        self.BUILD_PLAN_FACTS_EXAMPLES = yaml.load(EXAMPLES)

        self.TASK_GET_ALL = self.BUILD_PLAN_FACTS_EXAMPLES[0]['image_streamer_build_plan_facts']
        self.TASK_GET_BY_NAME = self.BUILD_PLAN_FACTS_EXAMPLES[4]['image_streamer_build_plan_facts']

        self.BUILD_PLAN = dict(
            name="Build Plan name",
            uri="/rest/build-plans/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_get_all_build_plans(self):
        self.i3s.build_plans.get_all.return_value = [self.BUILD_PLAN]
        self.mock_ansible_module.params = self.TASK_GET_ALL

        BuildPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(build_plans=[self.BUILD_PLAN])
        )

    def test_get_a_build_plan_by_name(self):
        self.i3s.build_plans.get_by.return_value = [self.BUILD_PLAN]
        self.mock_ansible_module.params = self.TASK_GET_BY_NAME

        BuildPlanFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(build_plans=[self.BUILD_PLAN])
        )


if __name__ == '__main__':
    unittest.main()
