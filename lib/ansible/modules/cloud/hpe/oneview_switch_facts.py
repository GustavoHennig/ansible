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
module: oneview_switch_facts
short_description: Retrieve facts about the OneView Switches.
description:
    - Retrieve facts about the OneView Switches.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - Switch name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about the Switch.
          Options allowed:
          C(environmentalConfiguration) gets the environmental configuration for a switch."
      required: false

notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all switches
  oneview_switch_facts:
    config: "{{ config }}"

- name: Gather paginated facts about switches
  oneview_switch_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3

- debug: var=switches

- name: Gather facts about the switch that matches the specified switch name
  oneview_switch_facts:
    config: "{{ config }}"
    name: "172.18.20.1"

- name: Gather facts about the environmental configuration for the switch that matches the specified switch name
  oneview_switch_facts:
    config: "{{ config }}"
    name: "172.18.20.1"
  options:
    - environmentalConfiguration
'''

RETURN = '''
switches:
    description: The list of switches.
    returned: Always, but can be null.
    type: list

switch_environmental_configuration:
    description: The environmental configuration for a switch.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class SwitchFactsModule(OneViewModuleBase):

    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )

        super(SwitchFactsModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.switches

    def execute_module(self):
        facts = dict()
        name = self.module.params["name"]
        if name:
            facts['switches'] = self.resource_client.get_by('name', name)

            if facts['switches'] and 'environmentalConfiguration' in self.options:
                uri = facts['switches'][0]['uri']
                environmental_configuration = self.resource_client.get_environmental_configuration(id_or_uri=uri)
                facts['switch_environmental_configuration'] = environmental_configuration
        else:
            facts['switches'] = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=facts)


def main():
    SwitchFactsModule().run()


if __name__ == '__main__':
    main()
