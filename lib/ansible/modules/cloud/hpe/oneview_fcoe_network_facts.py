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
module: oneview_fcoe_network_facts
short_description: Retrieve the facts about one or more of the OneView FCoE Networks.
description:
    - Retrieve the facts about one or more of the FCoE Networks from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - FCoE Network name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all FCoE Networks
  oneview_fcoe_network_facts:
    config: "{{ config_file_path }}"

- debug: var=fcoe_networks

- name: Gather paginated, filtered and sorted facts about FCoE Networks
  oneview_fcoe_network_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'vlanId=2'

- debug: var=fcoe_networks

- name: Gather facts about a FCoE Network by name
  oneview_fcoe_network_facts:
    config: "{{ config_file_path }}"
    name: "Test FCoE Network Facts"

- debug: var=fcoe_networks
'''

RETURN = '''
fcoe_networks:
    description: Has all the OneView facts about the FCoE Networks.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class FcoeNetworkFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )

        super(FcoeNetworkFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):

        if self.module.params['name']:
            fcoe_networks = self.oneview_client.fcoe_networks.get_by('name', self.module.params['name'])
        else:
            fcoe_networks = self.oneview_client.fcoe_networks.get_all(**self.params)

        return dict(changed=False,
                    ansible_facts=dict(fcoe_networks=fcoe_networks))


def main():
    FcoeNetworkFactsModule().run()


if __name__ == '__main__':
    main()
