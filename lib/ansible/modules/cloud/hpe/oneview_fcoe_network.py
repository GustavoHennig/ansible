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
module: oneview_fcoe_network
short_description: Manage OneView FCoE Network resources.
description:
    - Provides an interface to manage FCoE Network resources. Can create, update, or delete.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the FCoE Network resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - List with FCoE Network properties.
        required: true

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that FCoE Network is present using the default configuration
  oneview_fcoe_network:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'Test FCoE Network'
      vlanId: '201'

- name: Ensure that FCoE Network is absent
  oneview_fcoe_network:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New FCoE Network'
'''

RETURN = '''
fcoe_network:
    description: Has the facts about the OneView FCoE Networks.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class FcoeNetworkModule(OneViewModuleBase):
    MSG_CREATED = 'FCoE Network created successfully.'
    MSG_UPDATED = 'FCoE Network updated successfully.'
    MSG_DELETED = 'FCoE Network deleted successfully.'
    MSG_ALREADY_EXIST = 'FCoE Network already exists.'
    MSG_ALREADY_ABSENT = 'Nothing to do.'
    RESOURCE_FACT_NAME = 'fcoe_network'

    def __init__(self):

        add_arg_spec = dict(data=dict(required=True, type='dict'),
                            state=dict(
                                required=True,
                                choices=['present', 'absent']))

        super(FcoeNetworkModule, self).__init__(additional_arg_spec=add_arg_spec,
                                                validate_etag_support=True)

        self.resource_client = self.oneview_client.fcoe_networks

    def execute_module(self):
        resource = self.get_by_name(self.data.get('name'))

        if self.state == 'present':
            return self.resource_present(resource, self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent(resource)


def main():
    FcoeNetworkModule().run()


if __name__ == '__main__':
    main()
