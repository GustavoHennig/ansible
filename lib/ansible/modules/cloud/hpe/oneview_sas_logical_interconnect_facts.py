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
module: oneview_sas_logical_interconnect_facts
short_description: Retrieve facts about one or more of the OneView SAS Logical Interconnects.
description:
    - Retrieve facts about one or more of the OneView SAS Logical Interconnects.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author:
    - "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - SAS Logical Interconnect name.
      required: false
    options:
      description:
        - List with options to gather additional facts about SAS Logical Interconnect.
          C(firmware) gets the installed firmware for a SAS Logical Interconnect.
        - These options are valid just when a C(name) is provided. Otherwise it will be ignored.
      required: false


notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all SAS Logical Interconnects
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=sas_logical_interconnects

- name: Gather paginated, filtered and sorted facts about SAS Logical Interconnects
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 2
      sort: 'name:descending'
      filter: "status='OK'"
- debug: var=sas_logical_interconnects

- name: Gather facts about a SAS Logical Interconnect by name
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    name: "LOG_EN-LIG_SAS-1"
  delegate_to: localhost
- debug: var=sas_logical_interconnects

- name: Gather facts about an installed firmware for a SAS Logical Interconnect that matches the specified name
  oneview_sas_logical_interconnect_facts:
    config: "{{ config }}"
    name: "LOG_EN-LIG_SAS-1"
    options:
      - firmware
  delegate_to: localhost
- debug: var=sas_logical_interconnect_firmware
'''

RETURN = '''
sas_logical_interconnects:
    description: The list of SAS Logical Interconnects.
    returned: Always, but can be null.
    type: list

sas_logical_interconnect_firmware:
    description: The installed firmware for a SAS Logical Interconnect.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class SasLogicalInterconnectFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict')
        )

        super(SasLogicalInterconnectFactsModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.sas_logical_interconnects

    def execute_module(self):
        ansible_facts = {}

        if self.module.params['name']:
            sas_logical_interconnects = self.resource_client.get_by('name', self.module.params['name'])

            if sas_logical_interconnects and self.options:
                options_facts = self.__gather_option_facts(sas_logical_interconnects[0])
                ansible_facts.update(options_facts)
        else:
            sas_logical_interconnects = self.resource_client.get_all(**self.facts_params)

        ansible_facts['sas_logical_interconnects'] = sas_logical_interconnects

        return dict(changed=False, ansible_facts=ansible_facts)

    def __gather_option_facts(self, resource):
        ansible_facts = {}

        if self.options.get('firmware'):
            ansible_facts['sas_logical_interconnect_firmware'] = self.resource_client.get_firmware(resource['uri'])

        return ansible_facts


def main():
    SasLogicalInterconnectFactsModule().run()


if __name__ == '__main__':
    main()
