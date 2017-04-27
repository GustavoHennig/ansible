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


ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'curated',
                    'metadata_version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_logical_switch_facts
short_description: Retrieve the facts about one or more of the OneView Logical Switches.
description:
    - Retrieve the facts about one or more of the Logical Switches from OneView.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Logical Switch name.
      required: false
notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Logical Switches
  oneview_logical_switch_facts:
    config: "{{ config_file_path }}"

- debug: var=logical_switches

- name: Gather paginated, filtered and sorted facts about Logical Switches
  oneview_logical_switch_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=logical_switches

- name: Gather facts about a Logical Switch by name
  oneview_logical_switch_facts:
    config: "{{ config_file_path }}"
    name: 'Name of the Logical Switch'

- debug: var=logical_switches
'''

RETURN = '''
logical_switches:
    description: Has all the OneView facts about the Logical Switches.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class LogicalSwitchFactsModule(OneViewModuleBase):

    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )

        super(LogicalSwitchFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        name = self.module.params.get('name')
        if name:
            logical_switches = self.oneview_client.logical_switches.get_by('name', name)
        else:
            logical_switches = self.oneview_client.logical_switches.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(logical_switches=logical_switches))


def main():
    LogicalSwitchFactsModule().run()


if __name__ == '__main__':
    main()
