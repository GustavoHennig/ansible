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

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_logical_switch_group_facts
short_description: Retrieve facts about OneView Logical Switch Groups.
description:
    - Retrieve facts about the Logical Switch Groups of the OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Logical Switch Group name.
      required: false
notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Logical Switch Groups
  oneview_logical_switch_group_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=logical_switch_groups

- name: Gather paginated, filtered and sorted facts about Logical Switch Groups
  oneview_logical_switch_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "name='Logical_Switch_Group+56'"

- debug: var=logical_switch_groups

- name: Gather facts about a Logical Switch Group by name
  oneview_logical_switch_group_facts:
    config: "{{ config }}"
    name: "LogicalSwitchGroupDemo"
  delegate_to: localhost

- debug: var=logical_switch_groups
'''

RETURN = '''
logical_switch_groups:
    description: Has all the OneView facts about the Logical Switch Groups.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class LogicalSwitchGroupFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(LogicalSwitchGroupFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.logical_switch_groups

    def execute_module(self):

        if self.module.params.get('name'):
            logical_switch_groups = self.resource_client.get_by('name', self.module.params['name'])
        else:
            logical_switch_groups = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(logical_switch_groups=logical_switch_groups))


def main():
    LogicalSwitchGroupFactsModule().run()


if __name__ == '__main__':
    main()
