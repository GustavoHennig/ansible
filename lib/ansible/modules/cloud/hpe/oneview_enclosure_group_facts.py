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
module: oneview_enclosure_group_facts
short_description: Retrieve facts about one or more of the OneView Enclosure Groups.
description:
    - Retrieve facts about one or more of the Enclosure Groups from OneView.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author:
    - "Gustavo Hennig (@GustavoHennig)"
    - "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - Enclosure Group name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Enclosure Group.
          Options allowed:
          C(configuration_script) Gets the configuration script for an Enclosure Group."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Enclosure Groups
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
  delegate_to: localhost

- debug: var=enclosure_groups

- name: Gather paginated, filtered and sorted facts about Enclosure Groups
  oneview_enclosure_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=OK'

- debug: var=enclosure_groups

- name: Gather facts about an Enclosure Group by name with configuration script
  oneview_enclosure_group_facts:
    config: "{{ config_file_path }}"
    name: "Test Enclosure Group Facts"
    options:
      - configuration_script
    delegate_to: localhost

- debug: var=enclosure_groups
- debug: var=enclosure_group_script
'''

RETURN = '''
enclosure_groups:
    description: Has all the OneView facts about the Enclosure Groups.
    returned: Always, but can be null.
    type: complex

enclosure_group_script:
    description: The configuration script for an Enclosure Group.
    returned: When requested, but can be null.
    type: string
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class EnclosureGroupFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(EnclosureGroupFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        facts = {}
        name = self.module.params.get('name')

        if name:
            enclosure_groups = self.oneview_client.enclosure_groups.get_by('name', name)

            if enclosure_groups and "configuration_script" in self.options:
                facts["enclosure_group_script"] = self.__get_script(enclosure_groups)
        else:
            enclosure_groups = self.oneview_client.enclosure_groups.get_all(**self.facts_params)

        facts["enclosure_groups"] = enclosure_groups
        return dict(changed=False, ansible_facts=facts)

    def __get_script(self, enclosure_groups):
        script = None

        if enclosure_groups:
            enclosure_group_uri = enclosure_groups[0]['uri']
            script = self.oneview_client.enclosure_groups.get_script(id_or_uri=enclosure_group_uri)

        return script


def main():
    EnclosureGroupFactsModule().run()


if __name__ == '__main__':
    main()
