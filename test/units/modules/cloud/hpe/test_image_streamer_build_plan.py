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

from oneview_module_loader import BuildPlanModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'


class BuildPlanSpec(unittest.TestCase,
                    OneViewBaseTestCase):
    """
    OneViewBaseTestCase has tests for main function,
    also provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, BuildPlanModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        # Load scenarios from module examples
        self.BUILD_PLAN_CREATE = self.EXAMPLES[0]['image_streamer_build_plan']
        self.BUILD_PLAN_UPDATE = self.EXAMPLES[1]['image_streamer_build_plan']
        self.BUILD_PLAN_DELETE = self.EXAMPLES[2]['image_streamer_build_plan']

    def test_should_create_new_build_plan(self):
        self.i3s.build_plans.get_by.return_value = []
        self.i3s.build_plans.create.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.BUILD_PLAN_CREATE

        BuildPlanModule().run()

        self.i3s.build_plans.create.assert_called_once_with(
            {'name': 'Demo OS Build Plan',
             'description': "oebuildplan",
             'oeBuildPlanType': "deploy"})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=BuildPlanModule.MSG_CREATED,
            ansible_facts=dict(build_plan={"name": "name"})
        )

    def test_should_update_the_build_plan(self):
        self.i3s.build_plans.get_by.return_value = [self.BUILD_PLAN_CREATE['data']]
        self.i3s.build_plans.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.BUILD_PLAN_UPDATE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=BuildPlanModule.MSG_UPDATED,
            ansible_facts=dict(build_plan={"name": "name"})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.i3s.build_plans.get_by.return_value = [self.BUILD_PLAN_UPDATE['data']]

        del self.BUILD_PLAN_UPDATE['data']['newName']

        self.mock_ansible_module.params = self.BUILD_PLAN_UPDATE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=BuildPlanModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(build_plan=self.BUILD_PLAN_UPDATE['data'])
        )

    def test_should_delete_the_build_plan(self):
        self.i3s.build_plans.get_by.return_value = [self.BUILD_PLAN_CREATE['data']]

        self.mock_ansible_module.params = self.BUILD_PLAN_DELETE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=BuildPlanModule.MSG_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_build_plan(self):
        self.i3s.build_plans.get_by.return_value = []

        self.mock_ansible_module.params = self.BUILD_PLAN_DELETE

        BuildPlanModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=BuildPlanModule.MSG_ALREADY_ABSENT
        )


if __name__ == '__main__':
    unittest.main()
