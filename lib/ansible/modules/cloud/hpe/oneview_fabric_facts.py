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
module: oneview_fabric_facts
short_description: Retrieve the facts about one or more of the OneView Fabrics.
description:
    - Retrieve the facts about one or more of the Fabrics from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Fabric name.
      required: false
    options:
      description:
            - "List with options to gather additional facts about an Fabrics and related resources.
          Options allowed: C(reservedVlanRange)."
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Fabrics
  oneview_fabric_facts:
    config: "{{ config_file_path }}"

- debug: var=fabrics

- name: Gather paginated, filtered and sorted facts about Fabrics
  oneview_fabric_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'name=DefaultFabric'

- debug: var=fabrics

- name: Gather facts about a Fabric by name
  oneview_fabric_facts:
    config: "{{ config_file_path }}"
    name: DefaultFabric

- debug: var=fabrics

- name: Gather facts about a Fabric by name with options
  oneview_fabric_facts:
    config: "{{ config }}"
    name: DefaultFabric
    options:
      - reservedVlanRange          # optional

- debug: var=fabrics
'''

RETURN = '''
fabrics:
    description: Has all the OneView facts about the Fabrics.
    returned: Always, but can be null.
    type: complex
fabric_reserved_vlan_range:
    description: Has all the OneView facts about the reserved VLAN range
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class FabricFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(FabricFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.fabrics

    def execute_module(self):
        ansible_facts = {}
        name = self.module.params['name']
        if name:
            fabrics = self.oneview_client.fabrics.get_by('name', name)

            if self.options and fabrics:
                ansible_facts = self.__gather_optional_facts(fabrics[0])
        else:
            fabrics = self.oneview_client.fabrics.get_all(**self.facts_params)

        ansible_facts['fabrics'] = fabrics

        return dict(changed=False, ansible_facts=dict(ansible_facts))

    def __gather_optional_facts(self, fabric):
        ansible_facts = {}

        if self.options.get('reservedVlanRange'):
            ansible_facts['fabric_reserved_vlan_range'] = self.resource_client.get_reserved_vlan_range(fabric['uri'])

        return ansible_facts


def main():
    FabricFactsModule().run()


if __name__ == '__main__':
    main()
