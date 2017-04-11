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
module: image_streamer_plan_script_facts
short_description: Retrieve facts about the Image Streamer Plan Scripts.
description:
    - Retrieve facts about one or more of the Image Streamer Plan Script.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author:
    - "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Plan Script name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Plan Scripts
  image_streamer_plan_script_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=plan_scripts

- name: Gather paginated, filtered and sorted facts about Plan Scripts
  image_streamer_plan_script_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: planType=capture
  delegate_to: localhost
- debug: var=plan_scripts

- name: Gather facts about a Plan Script by name
  image_streamer_plan_script_facts:
    config: "{{ config }}"
    name: "Demo Plan Script"
  delegate_to: localhost
- debug: var=plan_scripts
'''

RETURN = '''
plan_scripts:
    description: The list of Plan Scripts.
    returned: Always, but can be null.
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class PlanScriptFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(PlanScriptFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")

        ansible_facts = {}

        if name:
            plan_scripts = self.i3s_client.plan_scripts.get_by("name", name)
        else:
            plan_scripts = self.i3s_client.plan_scripts.get_all(**self.facts_params)

        ansible_facts['plan_scripts'] = plan_scripts

        return dict(changed=False, ansible_facts=ansible_facts)


def main():
    PlanScriptFactsModule().run()


if __name__ == '__main__':
    main()
