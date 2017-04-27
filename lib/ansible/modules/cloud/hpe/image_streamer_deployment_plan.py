#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: image_streamer_deployment_plan
short_description: Manage Image Streamer Deployment Plan resources.
description:
    - "Provides an interface to manage Image Streamer Deployment Plans. Can create, update, and remove."
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Deployment Plan resource.
              C(present) will ensure data properties are compliant with Synergy Image Streamer.
              C(absent) will remove the resource from Synergy Image Streamer, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Deployment Plan properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create a Deployment Plan
  image_streamer_deployment_plan:
    config: "{{ config }}"
    state: present
    data:
      description: "Description of this Deployment Plan"
      name: 'Demo Deployment Plan'
      hpProvided: 'false'
      oeBuildPlanName: "Demo Build Plan"
  delegate_to: localhost

- name: Update the Deployment Plan
  image_streamer_deployment_plan:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo Deployment Plan'
      newName:  'Demo Deployment Plan (changed)'
      description: "New description"
  delegate_to: localhost

- name: Remove the Deployment Plan
  image_streamer_deployment_plan:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Demo Deployment Plan'
  delegate_to: localhost
'''

RETURN = '''
deployment_plan:
    description: Has the facts about the Image Streamer Deployment Plan.
    returned: On state 'present', but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class DeploymentPlanModule(OneViewModuleBase):
    MSG_CREATED = 'Deployment Plan created successfully.'
    MSG_UPDATED = 'Deployment Plan updated successfully.'
    MSG_ALREADY_PRESENT = 'Deployment Plan is already present.'
    MSG_DELETED = 'Deployment Plan deleted successfully.'
    MSG_ALREADY_ABSENT = 'Deployment Plan is already absent.'
    MSG_BUILD_PLAN_WAS_NOT_FOUND = 'OS Build Plan was not found.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(DeploymentPlanModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()
        self.resource_client = self.i3s_client.deployment_plans

    def execute_module(self):
        resource = self.get_by_name(self.data['name'])
        result = {}

        if self.state == 'present':
            self.__replace_name_by_uris(self.data)
            result = self.resource_present(resource, 'deployment_plan')
        elif self.state == 'absent':
            result = self.resource_absent(resource)

        return result

    def __replace_name_by_uris(self, data):
        build_plan_name = data.pop('oeBuildPlanName', None)
        if build_plan_name:
            data['oeBuildPlanURI'] = self.__get_build_plan_by_name(build_plan_name)['uri']

    def __get_build_plan_by_name(self, name):
        build_plan = self.i3s_client.build_plans.get_by('name', name)
        if build_plan:
            return build_plan[0]
        else:
            raise HPOneViewResourceNotFound(self.MSG_BUILD_PLAN_WAS_NOT_FOUND)


def main():
    DeploymentPlanModule().run()


if __name__ == '__main__':
    main()