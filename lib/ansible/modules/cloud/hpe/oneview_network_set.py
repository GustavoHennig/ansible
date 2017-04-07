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
module: oneview_network_set
short_description: Manage OneView Network Set resources.
description:
    - Provides an interface to manage Network Set resources. Can create, update, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
      description:
        - Indicates the desired state for the Network Set resource.
          C(present) ensures data properties are compliant with OneView.
          C(absent) removes the resource from OneView, if it exists.
      choices: ['present', 'absent']
    data:
      description:
        - List with the Network Set properties.
      required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Network Set
  oneview_network_set:
    config: '{{ config_path }}'
    state: present
    data:
      name: 'OneViewSDK Test Network Set'
      networkUris:
        - 'Test Ethernet Network_1'                                       # can be a name
        - '/rest/ethernet-networks/e4360c9d-051d-4931-b2aa-7de846450dd8'  # or a URI

- name: Update the Network Set name to 'OneViewSDK Test Network Set - Renamed' and change the associated networks
  oneview_network_set:
    config: '{{ config_path }}'
    state: present
    data:
      name: 'OneViewSDK Test Network Set'
      newName: 'OneViewSDK Test Network Set - Renamed'
      networkUris:
        - 'Test Ethernet Network_1'

- name: Delete the Network Set
  oneview_network_set:
    config: '{{ config_path }}'
    state: absent
    data:
        name: 'OneViewSDK Test Network Set - Renamed'
'''

RETURN = '''
network_set:
    description: Has the facts about the Network Set.
    returned: On state 'present', but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class NetworkSetModule(OneViewModuleBase):
    MSG_CREATED = 'Network Set created successfully.'
    MSG_UPDATED = 'Network Set updated successfully.'
    MSG_DELETED = 'Network Set deleted successfully.'
    MSG_ALREADY_EXIST = 'Network Set already exists.'
    MSG_ALREADY_ABSENT = 'Network Set is already absent.'
    NETWORK_SET_ENET_NETWORK_NOT_FOUND = 'Ethernet network not found: '
    RESOURCE_FACT_NAME = 'network_set'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict'))

    def __init__(self):
        super(NetworkSetModule, self).__init__(additional_arg_spec=self.argument_spec,
                                               validate_etag_support=True)
        self.resource_client = self.oneview_client.network_sets

    def execute_module(self):
        resource = self.get_by_name(self.data.get('name'))

        if self.state == 'present':
            self.__replace_network_name_by_uri(self.data)
            return self.resource_present(resource, self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent(resource)

    def __get_ethernet_network_by_name(self, name):
        result = self.oneview_client.ethernet_networks.get_by('name', name)
        return result[0] if result else None

    def __get_network_uri(self, network_name_or_uri):
        if network_name_or_uri.startswith('/rest/ethernet-networks'):
            return network_name_or_uri
        else:
            enet_network = self.__get_ethernet_network_by_name(network_name_or_uri)
            if enet_network:
                return enet_network['uri']
            else:
                raise HPOneViewResourceNotFound(self.NETWORK_SET_ENET_NETWORK_NOT_FOUND + network_name_or_uri)

    def __replace_network_name_by_uri(self, data):
        if 'networkUris' in data:
            data['networkUris'] = [self.__get_network_uri(x) for x in data['networkUris']]


def main():
    NetworkSetModule().run()


if __name__ == '__main__':
    main()