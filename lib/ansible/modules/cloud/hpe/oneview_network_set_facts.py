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
module: oneview_network_set_facts
short_description: Retrieve facts about the OneView Network Sets.
description:
    - Retrieve facts about the Network Sets from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Network Set name.
      required: false
    options:
      description:
        - "List with options to gather facts about Network Set.
          Option allowed: C(withoutEthernet).
          The option C(withoutEthernet) retrieves the list of network_sets excluding Ethernet networks."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Network Sets
  oneview_network_set_facts:
    config: '{{ config_path }}'

- debug: var=network_sets

- name: Gather paginated, filtered, and sorted facts about Network Sets
  oneview_network_set_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: name='netset001'

- debug: var=network_sets

- name: Gather facts about all Network Sets, excluding Ethernet networks
  oneview_network_set_facts:
    config: '{{ config_path }}'
    options:
        - withoutEthernet

- debug: var=network_sets


- name: Gather facts about a Network Set by name
  oneview_network_set_facts:
    config: '{{ config_path }}'
    name: 'Name of the Network Set'

- debug: var=network_sets


- name: Gather facts about a Network Set by name, excluding Ethernet networks
  oneview_network_set_facts:
    config: '{{ config_path }}'
    name: 'Name of the Network Set'
    options:
        - withoutEthernet

- debug: var=network_sets
'''

RETURN = '''
network_sets:
    description: Has all the OneView facts about the Network Sets.
    returned: Always, but can be empty.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class NetworkSetFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(NetworkSetFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):

        name = self.module.params.get('name')

        if 'withoutEthernet' in self.options:
            filter_by_name = "\"'name'='{}'\"".format(name) if name else ''
            network_sets = self.oneview_client.network_sets.get_all_without_ethernet(filter=filter_by_name)
        elif name:
            network_sets = self.oneview_client.network_sets.get_by('name', name)
        else:
            network_sets = self.oneview_client.network_sets.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(network_sets=network_sets))


def main():
    NetworkSetFactsModule().run()


if __name__ == '__main__':
    main()
