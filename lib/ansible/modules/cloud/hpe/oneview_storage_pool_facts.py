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
module: oneview_storage_pool_facts
short_description: Retrieve facts about one or more Storage Pools.
description:
    - Retrieve facts about one or more of the Storage Pools from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Storage Pool name.
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Storage Pools
  oneview_storage_pool_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_pools

- name: Gather paginated, filtered and sorted facts about Storage Pools
  oneview_storage_pool_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: status='OK'

- debug: var=storage_pools

- name: Gather facts about a Storage Pool by name
  oneview_storage_pool_facts:
    config: "{{ config }}"
    name: "CPG_FC-AO"
  delegate_to: localhost

- debug: var=storage_pools
'''

RETURN = '''
storage_pools:
    description: Has all the OneView facts about the Storage Pools.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class StoragePoolFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict'),
        )
        super(StoragePoolFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.storage_pools

    def execute_module(self):
        if self.module.params.get('name'):
            storage_pool = self.oneview_client.storage_pools.get_by('name', self.module.params['name'])
        else:
            storage_pool = self.oneview_client.storage_pools.get_all(**self.params)

        return dict(changed=False, ansible_facts=dict(storage_pools=storage_pool))


def main():
    StoragePoolFactsModule().run()


if __name__ == '__main__':
    main()
