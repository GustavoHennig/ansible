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
module: oneview_server_hardware_type_facts
short_description: Retrieve facts about Server Hardware Types of the OneView.
description:
    - Retrieve facts about Server Hardware Types of the OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Server Hardware Type name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Server Hardware Types
  oneview_server_hardware_type_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=server_hardware_types

- name: Gather paginated, filtered and sorted facts about Server Hardware Types
  oneview_server_hardware_type_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: name:ascending
      filter: formFactor='HalfHeight'
  delegate_to: localhost
- debug: msg="{{server_hardware_types | map(attribute='name') | list }}"

- name: Gather facts about a Server Hardware Type by name
  oneview_server_hardware_type_facts:
    config: "{{ config }}"
    name: "BL460c Gen8 1"
  delegate_to: localhost
- debug: var=server_hardware_types
'''

RETURN = '''
server_hardware_types:
    description: Has all the OneView facts about the Server Hardware Types.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class ServerHardwareTypeFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )
        super(ServerHardwareTypeFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):

        name = self.module.params.get('name')

        if name:
            server_hardware_types = self.oneview_client.server_hardware_types.get_by('name', name)
        else:
            server_hardware_types = self.oneview_client.server_hardware_types.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(server_hardware_types=server_hardware_types))


def main():
    ServerHardwareTypeFactsModule().run()


if __name__ == '__main__':
    main()
