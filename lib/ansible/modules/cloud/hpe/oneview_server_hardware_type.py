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
module: oneview_server_hardware_type
short_description: Manage OneView Server Hardware Type resources.
description:
    - "Provides an interface to manage Server Hardware Type resources. Can update, and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Server Hardware Type resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Server Hardware Type properties and its associated states.
        required: true
extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Update the Server Hardware Type description
  oneview_server_hardware_type:
    config: "{{ config }}"
    state: present
    data:
      name: 'DL380p Gen8 1'
      description: "New Description"
  delegate_to: localhost

- name: Rename the Server Hardware Type
  oneview_server_hardware_type:
    config: "{{ config }}"
    state: present
    data:
        name: 'DL380p Gen8 1'
        newName: 'DL380p Gen8 1 (new name)'
  delegate_to: localhost

- name: Delete the Server Hardware Type
  oneview_server_hardware_type:
    config: "{{ config }}"
    state: absent
    data:
        name: 'DL380p Gen8 1 (new name)'
  delegate_to: localhost
'''

RETURN = '''
server_hardware_type:
    description: Has the OneView facts about the Server Hardware Type.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class ServerHardwareTypeModule(OneViewModuleBase):
    MSG_UPDATED = 'Server Hardware Type updated successfully.'
    MSG_ALREADY_PRESENT = 'Server Hardware Type is already present.'
    MSG_DELETED = 'Server Hardware Type deleted successfully.'
    MSG_ALREADY_ABSENT = 'Server Hardware Type is already absent.'
    MSG_RESOURCE_NOT_FOUND = 'Server Hardware Type was not found for this operation.'

    argument_spec = dict(
        state=dict(required=True, choices=['present', 'absent']),
        data=dict(required=True, type='dict'))

    def __init__(self):

        super(ServerHardwareTypeModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                       validate_etag_support=True)
        self.resource_client = self.oneview_client.server_hardware_types

    def execute_module(self):
        resource = self.get_by_name(self.data.get('name'))

        if self.state == 'present':
            return self.__present(resource)
        elif self.state == 'absent':
            return self.__absent(resource)

    def __present(self, resource):
        changed, msg = False, self.MSG_ALREADY_PRESENT

        if not resource:
            raise HPOneViewResourceNotFound(self.MSG_RESOURCE_NOT_FOUND)

        if "newName" in self.data:
            self.data["name"] = self.data.pop("newName")

        different = resource.get('name') != self.data.get('name')
        different |= resource.get('description') != self.data.get('description')

        if different:
            resource = self.resource_client.update(self.data, resource['uri'])
            changed = True
            msg = self.MSG_UPDATED

        return dict(changed=changed, msg=msg, ansible_facts=dict(server_hardware_type=resource))

    def __absent(self, resource):
        if resource:
            self.resource_client.delete(resource)
            return dict(changed=True, msg=self.MSG_DELETED)

        return dict(changed=False, msg=self.MSG_ALREADY_ABSENT)


def main():
    ServerHardwareTypeModule().run()


if __name__ == '__main__':
    main()
