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

from oneview_module_loader import PlanScriptModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'


class PlanScriptSpec(unittest.TestCase,
                     OneViewBaseTestCase):
    """
    OneViewBaseTestCase has common test for main function
    """

    def setUp(self):
        self.configure_mocks(self, PlanScriptModule)
        self.i3s = self.mock_ov_client.create_image_streamer_client()

        # Load scenarios from module examples
        self.PLAN_SCRIPT_CREATE = self.EXAMPLES[0]['image_streamer_plan_script']
        self.PLAN_SCRIPT_UPDATE = self.EXAMPLES[1]['image_streamer_plan_script']
        self.PLAN_SCRIPT_DIFFERENCES = self.EXAMPLES[2]['image_streamer_plan_script']
        self.PLAN_SCRIPT_DELETE = self.EXAMPLES[4]['image_streamer_plan_script']
        self.PLAN_SCRIPT = dict(
            name="Plan Script name",
            uri="/rest/plan-scripts/d1c7b09a-6c7b-4ae0-b68e-ed208ccde1b0")

    def test_create_new_plan_script(self):
        self.i3s.plan_scripts.get_by.return_value = []
        self.i3s.plan_scripts.create.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.PLAN_SCRIPT_CREATE

        PlanScriptModule().run()

        self.i3s.plan_scripts.create.assert_called_once_with(
            {'content': 'echo "test script"',
             'planType': 'deploy',
             'hpProvided': False,
             'description': 'Description of this plan script',
             'name': 'Demo Plan Script'})

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PlanScriptModule.MSG_CREATED,
            ansible_facts=dict(plan_script={"name": "name"})
        )

    def test_update_plan_script(self):
        self.i3s.plan_scripts.get_by.return_value = [self.PLAN_SCRIPT]
        self.i3s.plan_scripts.update.return_value = {"name": "name"}

        self.mock_ansible_module.params = self.PLAN_SCRIPT_UPDATE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PlanScriptModule.MSG_UPDATED,
            ansible_facts=dict(plan_script={"name": "name"})
        )

    def test_retrieve_plan_script_content_differences(self):
        self.i3s.plan_scripts.get_by.return_value = [self.PLAN_SCRIPT]
        self.i3s.plan_scripts.retrieve_differences.return_value = {"differences": []}

        self.mock_ansible_module.params = self.PLAN_SCRIPT_DIFFERENCES

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PlanScriptModule.MSG_DIFFERENCES_RETRIEVED,
            ansible_facts=dict(plan_script_differences={"differences": []})
        )

    def test_should_not_update_when_data_is_equals(self):
        self.i3s.plan_scripts.get_by.return_value = [self.PLAN_SCRIPT_UPDATE['data']]
        self.mock_ansible_module.params = self.PLAN_SCRIPT_UPDATE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PlanScriptModule.MSG_ALREADY_EXIST,
            ansible_facts=dict(plan_script=self.PLAN_SCRIPT_UPDATE['data'])
        )

    def test_delete_plan_script(self):
        self.i3s.plan_scripts.get_by.return_value = [self.PLAN_SCRIPT]

        self.mock_ansible_module.params = self.PLAN_SCRIPT_DELETE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=PlanScriptModule.MSG_DELETED
        )

    def test_should_do_nothing_when_deleting_a_non_existent_plan_script(self):
        self.i3s.plan_scripts.get_by.return_value = []

        self.mock_ansible_module.params = self.PLAN_SCRIPT_DELETE

        PlanScriptModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=PlanScriptModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_mandatory_attributes_are_missing(self):
        self.i3s.plan_scripts.get_by.return_value = []

        del self.PLAN_SCRIPT_DIFFERENCES['data']['content']

        self.mock_ansible_module.params = self.PLAN_SCRIPT_DIFFERENCES

        PlanScriptModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(
            msg=PlanScriptModule.MSG_CONTENT_ATTRIBUTE_MANDATORY
        )


if __name__ == '__main__':
    unittest.main()
