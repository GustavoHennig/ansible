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
module: oneview_logical_enclosure_facts
short_description: Retrieve facts about one or more of the OneView Logical Enclosures.
description:
    - Retrieve facts about one or more of the Logical Enclosures from OneView.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author:
    - "Gustavo Hennig (@GustavoHennig)"
    - "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Logical Enclosure name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about a Logical Enclosure and related resources.
          Options allowed: script."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Logical Enclosures
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather paginated, filtered and sorted facts about Logical Enclosures
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
  delegate_to: localhost

- debug: var=logical_enclosures

- name: Gather facts about a Logical Enclosure by name with options
  oneview_logical_enclosure_facts:
    config: "{{ config_file_path }}"
    name: "Encl1"
    options:
      - script
  delegate_to: localhost

- debug: var=logical_enclosures
- debug: var=logical_enclosure_script
'''

RETURN = '''
logical_enclosures:
    description: Has all the OneView facts about the Logical Enclosures.
    returned: Always, but can be null.
    type: complex

logical_enclosure_script:
    description: Has the facts about the script of a Logical Enclosure.
    returned: When required, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class LogicalEnclosureFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(LogicalEnclosureFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):

        ansible_facts = {}

        if self.module.params.get('name'):
            logical_enclosures = self.oneview_client.logical_enclosures.get_by('name', self.module.params['name'])

            if self.options and logical_enclosures:
                ansible_facts = self.__gather_optional_facts(self.options, logical_enclosures[0])
        else:
            logical_enclosures = self.oneview_client.logical_enclosures.get_all(**self.facts_params)

        ansible_facts['logical_enclosures'] = logical_enclosures

        return dict(changed=False, ansible_facts=ansible_facts)

    def __gather_optional_facts(self, options, logical_enclosure):

        logical_enclosure_client = self.oneview_client.logical_enclosures
        ansible_facts = {}

        if options.get('script'):
            ansible_facts['logical_enclosure_script'] = logical_enclosure_client.get_script(logical_enclosure['uri'])

        return ansible_facts


def main():
    LogicalEnclosureFactsModule().run()


if __name__ == '__main__':
    main()
