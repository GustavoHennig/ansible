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

from ansible.modules.cloud.hpe.image_streamer_deployment_group_facts import DeploymentGroupFactsModule, EXAMPLES
from hpe_test_utils import FactsParamsTestCase


class DeploymentGroupFactsSpec(unittest.TestCase,
                               FactsParamsTestCase):
    """
    FactsParamsTestCase has common tests for the parameters support.
    """

    def setUp(self):
        self.configure_mocks(self, DeploymentGroupFactsModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        FactsParamsTestCase.configure_client_mock(self, self.i3s.deployment_groups)

        # Load scenarios from module examples
        self.DEPLOYMENT_GROUP_FACTS_EXAMPLES = yaml.load(EXAMPLES)

        self.TASK_GET_ALL = self.DEPLOYMENT_GROUP_FACTS_EXAMPLES[0]['image_streamer_deployment_group_facts']
        self.TASK_GET_BY_NAME = self.DEPLOYMENT_GROUP_FACTS_EXAMPLES[4]['image_streamer_deployment_group_facts']

        self.DEPLOYMENT_GROUP = dict(
            name="OSS",
            uri="/rest/deployment-group/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_get_all_deployment_groups(self):
        self.i3s.deployment_groups.get_all.return_value = [self.DEPLOYMENT_GROUP]
        self.mock_ansible_module.params = self.TASK_GET_ALL

        DeploymentGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_groups=[self.DEPLOYMENT_GROUP])
        )

    def test_get_a_deployment_group_by_name(self):
        self.i3s.deployment_groups.get_by.return_value = [self.DEPLOYMENT_GROUP]
        self.mock_ansible_module.params = self.TASK_GET_BY_NAME

        DeploymentGroupFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(deployment_groups=[self.DEPLOYMENT_GROUP])
        )


if __name__ == '__main__':
    unittest.main()
