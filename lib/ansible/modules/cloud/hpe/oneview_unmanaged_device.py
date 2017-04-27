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
module: oneview_unmanaged_device
short_description: Manage OneView Unmanaged Device resources.
description:
    - Provides an interface to manage Unmanaged Device resources. Can create, update, or delete.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Unmanaged Device resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with Unmanaged Device properties.
        required: true
notes:
    - "To rename an Unamnaged Device you must inform a C(newName) in the data argument. The rename is non-idempotent"

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that the unmanaged device is present
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: present
    data:
      name: 'MyUnmanagedDevice'
      model: 'Procurve 4200VL'
      deviceType: 'Server'
    delegate_to: localhost

- debug: var=unmanaged_device

- name: Add another unmanaged device
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: present
    data:
      name: 'AnotherUnmanagedDevice'
      model: 'Procurve 4200VL'
    delegate_to: localhost

- name: Update the unmanaged device changing the name attribute
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: present
    data:
      name: 'MyUnmanagedDevice'
      newName: 'UnmanagedDeviceRenamed'
    delegate_to: localhost

- debug: var=unmanaged_device

- name: Ensure that the unmanaged device is absent
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: absent
    data:
      name: 'UnmanagedDeviceRenamed'
    delegate_to: localhost

- name: Delete all the unmanaged devices
  oneview_unmanaged_device:
    config: "{{ config }}"
    state: absent
    data:
      filter: "name matches '%'"
    delegate_to: localhost
'''

RETURN = '''
unmanaged_device:
    description: Has the OneView facts about the Unmanaged Device.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class UnmanagedDeviceModule(OneViewModuleBase):
    MSG_CREATED = 'Unmanaged Device added successfully.'
    MSG_UPDATED = 'Unmanaged Device updated successfully.'
    MSG_DELETED = 'Unmanaged Device removed successfully.'
    MSG_SET_DELETED = 'Unmanaged device set deleted successfully.'
    MSG_ALREADY_ABSENT = 'Unmanaged Device is already absent.'
    MSG_ALREADY_PRESENT = 'Unmanaged Device is already present.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(UnmanagedDeviceModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                    validate_etag_support=True)

        self.resource_client = self.oneview_client.unmanaged_devices

    def execute_module(self):
        resource = self.get_by_name(self.data["name"]) if 'name' in self.data else None

        if self.state == "present":
            return self.resource_present(resource, 'unmanaged_device', 'add')
        elif self.state == "absent":
            if not resource and "filter" in self.data:
                self.resource_client.remove_all(**self.data)
                return dict(changed=True, msg=self.MSG_SET_DELETED)
            else:
                return self.resource_absent(resource, 'remove')


def main():
    UnmanagedDeviceModule().run()


if __name__ == '__main__':
    main()
