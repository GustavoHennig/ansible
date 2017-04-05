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
module: oneview_interconnect_type_facts
short_description: Retrieve facts about one or more of the OneView Interconnect Types.
description:
    - Retrieve facts about one or more of the Interconnect Types from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Interconnect Type name.
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Interconnect Types
  oneview_interconnect_type_facts:
    config: "{{ config_file_path }}"

- debug: var=interconnect_types

- name: Gather paginated, filtered and sorted facts about Interconnect Types
  oneview_interconnect_type_facts:
    config: "{{ config_file_path }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "maximumFirmwareVersion='4000.99'"

- debug: var=interconnect_types

- name: Gather facts about an Interconnect Type by name
  oneview_interconnect_type_facts:
    config: "{{ config_file_path }}"
    name: HP VC Flex-10 Enet Module

- debug: var=interconnect_types
'''

RETURN = '''
interconnect_types:
    description: Has all the OneView facts about the Interconnect Types.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class InterconnectTypeFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(InterconnectTypeFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.interconnect_types

    def execute_module(self):

        if self.module.params.get('name'):
            interconnect_types = self.oneview_client.interconnect_types.get_by('name', self.module.params['name'])
        else:
            interconnect_types = self.oneview_client.interconnect_types.get_all(**self.params)

        return dict(changed=False, ansible_facts=dict(interconnect_types=interconnect_types))


def main():
    InterconnectTypeFactsModule().run()


if __name__ == '__main__':
    main()
