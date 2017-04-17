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
module: oneview_storage_pool
short_description: Manage OneView Storage Pool resources.
description:
    - "Provides an interface to manage Storage Pool resources. Can add and remove."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Storage Pool resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Storage Pool properties and its associated states.
        required: true
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Create a Storage Pool
  oneview_storage_pool:
    config: "{{ config }}"
    state: present
    data:
       storageSystemUri: "/rest/storage-systems/TXQ1010307"
       poolName: "FST_CPG2"
  delegate_to: localhost

- name: Delete the Storage Pool
  oneview_storage_pool:
    config: "{{ config }}"
    state: absent
    data:
       poolName: "FST_CPG2"
  delegate_to: localhost
'''

RETURN = '''
storage_pool:
    description: Has the OneView facts about the Storage Pool.
    returned: On 'present' state, but can be null.
    type: complex
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewValueError


class StoragePoolModule(OneViewModuleBase):
    MSG_CREATED = 'Storage Pool added successfully.'
    MSG_ALREADY_PRESENT = 'Storage Pool is already present.'
    MSG_DELETED = 'Storage Pool deleted successfully.'
    MSG_ALREADY_ABSENT = 'Storage Pool is already absent.'
    MSG_MANDATORY_FIELD_MISSING = "Mandatory field was not informed: data.poolName"

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['present', 'absent']
            ),
            data=dict(required=True, type='dict')
        )

        super(StoragePoolModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.storage_pools

    def execute_module(self):
        if not self.data.get('poolName'):
            raise HPOneViewValueError(self.MSG_MANDATORY_FIELD_MISSING)

        resource = self.get_by_name(self.data['poolName'])

        if self.state == 'present':
            return self.__present(self.data, resource)
        elif self.state == 'absent':
            return self.resource_absent(resource, 'remove')

    def __present(self, data, resource):

        changed = False
        msg = self.MSG_ALREADY_PRESENT

        if not resource:
            resource = self.oneview_client.storage_pools.add(data)
            changed = True
            msg = self.MSG_CREATED

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(storage_pool=resource))


def main():
    StoragePoolModule().run()


if __name__ == '__main__':
    main()
