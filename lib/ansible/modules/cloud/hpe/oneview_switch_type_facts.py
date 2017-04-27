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
module: oneview_switch_type_facts
short_description: Retrieve facts about the OneView Switch Types.
description:
    - Retrieve facts about the Switch Types from OneView.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Name of the Switch Type.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Switch Types
  oneview_switch_type_facts:
    config: "{{ config_path }}"

- debug: var=switch_types

- name: Gather paginated, filtered and sorted facts about Switch Types
  oneview_switch_type_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "partNumber='N5K-C56XX'"

- debug: var=switch_types

- name: Gather facts about a Switch Type by name
  oneview_switch_type_facts:
    config: "{{ config_path }}"
    name: "Name of the Switch Type"

- debug: var=switch_types
'''

RETURN = '''
switch_types:
    description: Has all the OneView facts about the Switch Types.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class SwitchTypeFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )
        super(SwitchTypeFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        if self.module.params['name']:
            switch_types = self.oneview_client.switch_types.get_by('name', self.module.params['name'])
        else:
            switch_types = self.oneview_client.switch_types.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(switch_types=switch_types))


def main():
    SwitchTypeFactsModule().run()


if __name__ == '__main__':
    main()
