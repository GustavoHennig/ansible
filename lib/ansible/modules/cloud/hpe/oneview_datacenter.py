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
module: oneview_datacenter
short_description: Manage OneView Data Center resources.
description:
    - "Provides an interface to manage Data Center resources. Can add, update, and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Data Center resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Data Center properties and its associated states.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Add a Data Center
  oneview_datacenter:
    config: "{{ config }}"
    state: present
    data:
        name: "MyDatacenter"
        width: 5000
        depth: 6000
        contents:
            # You can choose either resourceName or resourceUri to inform the Rack
            - resourceName: '{{ datacenter_content_rack_name }}' # option 1
              resourceUri: ''                                    # option 2
              x: 1000
              y: 1000
  delegate_to: localhost

- name: Update the Data Center with specified properties (no racks)
  oneview_datacenter:
    config: "{{ config }}"
    state: present
    data:
        name: "MyDatacenter"
        coolingCapacity: '5'
        costPerKilowattHour: '0.10'
        currency: USD
        deratingType: NaJp
        deratingPercentage: '20.0'
        defaultPowerLineVoltage: '220'
        coolingMultiplier: '1.5'
        width: 4000
        depth: 5000
        contents: ~

  delegate_to: localhost

- name: Rename the Data Center
  oneview_datacenter:
    config: "{{ config }}"
    state: present
    data:
        name: "MyDatacenter"
        newName: "My Datacenter"
  delegate_to: localhost

- name: Remove the Data Center
  oneview_datacenter:
    config: "{{ config }}"
    state: absent
    data:
        name: 'My Datacenter'
  delegate_to: localhost
'''

RETURN = '''
datacenter:
    description: Has the OneView facts about the Data Center.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class DatacenterModule(OneViewModuleBase):
    MSG_CREATED = 'Data Center added successfully.'
    MSG_UPDATED = 'Data Center updated successfully.'
    MSG_ALREADY_EXIST = 'Data Center is already present.'
    MSG_DELETED = 'Data Center removed successfully.'
    MSG_ALREADY_ABSENT = 'Data Center is already absent.'
    RACK_NOT_FOUND = 'Rack was not found.'
    RESOURCE_FACT_NAME = 'datacenter'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(DatacenterModule, self).__init__(additional_arg_spec=self.argument_spec,
                                               validate_etag_support=True)
        self.resource_client = self.oneview_client.datacenters

    def execute_module(self):

        resource = self.get_by_name(self.data['name'])

        if self.state == 'present':
            self.__replace_name_by_uris(self.data)
            return self.resource_present(resource, self.RESOURCE_FACT_NAME, 'add')
        elif self.state == 'absent':
            return self.resource_absent(resource, 'remove')

    def __replace_name_by_uris(self, resource):
        contents = resource.get('contents')

        if contents:
            for content in contents:
                resource_name = content.pop('resourceName', None)
                if resource_name:
                    content['resourceUri'] = self.__get_rack_by_name(resource_name)['uri']

    def __get_rack_by_name(self, name):
        racks = self.oneview_client.racks.get_by('name', name)
        if racks:
            return racks[0]
        else:
            raise HPOneViewResourceNotFound(self.RACK_NOT_FOUND)


def main():
    DatacenterModule().run()


if __name__ == '__main__':
    main()
