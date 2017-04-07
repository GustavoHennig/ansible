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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: image_streamer_build_plan
short_description: Manages Image Stream OS Build Plan resources.
description:
    - "Provides an interface to manage Image Stream OS Build Plans. Can create, update, and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the OS Build Plan resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with OS Build Plan properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create an OS Build Plan
  image_streamer_build_plan:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo OS Build Plan'
      description: "oebuildplan"
      oeBuildPlanType: "deploy"
  delegate_to: localhost

- name: Update the OS Build Plan description and name
  image_streamer_build_plan:
    config: "{{ config }}"
    state: present
    data:
      name: 'Demo OS Build Plan'
      description: "New description"
      newName: 'OS Build Plan Renamed'
  delegate_to: localhost

- name: Remove an OS Build Plan
  image_streamer_build_plan:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Demo OS Build Plan'
  delegate_to: localhost
'''

RETURN = '''
build_plan:
    description: Has the OneView facts about the OS Build Plan.
    returned: On state 'present'.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewValueError


class BuildPlanModule(OneViewModuleBase):
    MSG_CREATED = 'OS Build Plan created successfully.'
    MSG_UPDATED = 'OS Build Plan updated successfully.'
    MSG_ALREADY_EXIST = 'OS Build Plan is already present.'
    MSG_DELETED = 'OS Build Plan deleted successfully.'
    MSG_ALREADY_ABSENT = 'OS Build Plan is already absent.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(BuildPlanModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()
        self.resource_client = self.i3s_client.build_plans

    def execute_module(self):
        resource = self.get_by_name(self.data['name'])
        result = {}

        if self.state == 'present':
            result = self.resource_present(resource, 'build_plan')
        elif self.state == 'absent':
            result = self.resource_absent(resource)

        return result


def main():
    BuildPlanModule().run()


if __name__ == '__main__':
    main()