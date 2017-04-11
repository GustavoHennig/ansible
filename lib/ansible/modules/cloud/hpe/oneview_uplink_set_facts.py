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
module: oneview_uplink_set_facts
short_description: Retrieve facts about one or more of the OneView Uplink Sets.
version_added: "2.3"
description:
    - Retrieve facts about one or more of the Uplink Sets from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Uplink Set name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Uplink Sets
  oneview_uplink_set_facts:
    config: "{{ config_file_path }}"

- debug: var=uplink_sets

- name: Gather paginated, filtered and sorted facts about Uplink Sets
  oneview_uplink_set_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "logicalInterconnectUri='/rest/logical-interconnects/4a49ca0d-3782-4c11-b93e-79d8f90c5487'"

- debug: var=uplink_sets

- name: Gather facts about a Uplink Set by name
  oneview_uplink_set_facts:
    config: "{{ config_file_path }}"
    name: logical lnterconnect group name

- debug: var=uplink_sets
'''

RETURN = '''
uplink_sets:
    description: Has all the OneView facts about the Uplink Sets.
    returned: Always, but can be null.
    type: complex
'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class UplinkSetFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )
        super(UplinkSetFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        if self.module.params['name']:
            resources = self.oneview_client.uplink_sets.get_by('name', self.module.params['name'])
        else:
            resources = self.oneview_client.uplink_sets.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(uplink_sets=resources))


def main():
    UplinkSetFactsModule().run()


if __name__ == '__main__':
    main()
