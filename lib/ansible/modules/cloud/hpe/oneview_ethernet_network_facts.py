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
                    'supported_by': 'committer',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_ethernet_network_facts
short_description: Retrieve the facts about one or more of the OneView Ethernet Networks.
description:
    - Retrieve the facts about one or more of the Ethernet Networks from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author:
    - "Camila Balestrin (@balestrinc)"
    - "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Ethernet Network name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about an Ethernet Network and related resources.
          Options allowed: C(associatedProfiles) and C(associatedUplinkGroups)."
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Ethernet Networks
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"

- debug: var=ethernet_networks

- name: Gather paginated and filtered facts about Ethernet Networks
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"
    params:
      start: 1
      count: 3
      sort: 'name:descending'
      filter: 'purpose=General'

- debug: var=ethernet_networks

- name: Gather facts about an Ethernet Network by name
  oneview_ethernet_network_facts:
    config: "{{ config_file_path }}"
    name: Ethernet network name

- debug: var=ethernet_networks

- name: Gather facts about an Ethernet Network by name with options
  oneview_ethernet_network_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - associatedProfiles
      - associatedUplinkGroups
  delegate_to: localhost

- debug: var=enet_associated_profiles
- debug: var=enet_associated_uplink_groups
'''

RETURN = '''
ethernet_networks:
    description: Has all the OneView facts about the Ethernet Networks.
    returned: Always, but can be null.
    type: complex

enet_associated_profiles:
    description: Has all the OneView facts about the profiles which are using the Ethernet network.
    returned: When requested, but can be null.
    type: complex

enet_associated_uplink_groups:
    description: Has all the OneView facts about the uplink sets which are using the Ethernet network.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class EthernetNetworkFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(EthernetNetworkFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

        self.resource_client = self.oneview_client.ethernet_networks

    def execute_module(self):
        ansible_facts = {}
        if self.module.params['name']:
            ethernet_networks = self.resource_client.get_by('name', self.module.params['name'])

            if self.module.params.get('options') and ethernet_networks:
                ansible_facts = self.__gather_optional_facts(ethernet_networks[0])
        else:
            ethernet_networks = self.resource_client.get_all(**self.params)

        ansible_facts['ethernet_networks'] = ethernet_networks

        return dict(changed=False, ansible_facts=ansible_facts)

    def __gather_optional_facts(self, ethernet_network):

        ansible_facts = {}

        if self.options.get('associatedProfiles'):
            ansible_facts['enet_associated_profiles'] = self.__get_associated_profiles(ethernet_network)
        if self.options.get('associatedUplinkGroups'):
            ansible_facts['enet_associated_uplink_groups'] = self.__get_associated_uplink_groups(ethernet_network)

        return ansible_facts

    def __get_associated_profiles(self, ethernet_network):
        associated_profiles = self.resource_client.get_associated_profiles(ethernet_network['uri'])
        return [self.oneview_client.server_profiles.get(x) for x in associated_profiles]

    def __get_associated_uplink_groups(self, ethernet_network):
        uplink_groups = self.resource_client.get_associated_uplink_groups(ethernet_network['uri'])
        return [self.oneview_client.uplink_sets.get(x) for x in uplink_groups]


def main():
    EthernetNetworkFactsModule().run()


if __name__ == '__main__':
    main()
