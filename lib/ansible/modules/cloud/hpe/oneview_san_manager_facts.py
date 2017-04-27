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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: oneview_san_manager_facts
short_description: Retrieve facts about one or more of the OneView SAN Managers.
description:
    - Retrieve facts about one or more of the SAN Managers from OneView.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Mariana Kreisig (@marikrg)"
options:
    provider_display_name:
      description:
        - Provider Display Name.
      required: false
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
           C(start): The first item to return, using 0-based indexing.
           C(count): The number of resources to return.
           C(query): A general query string to narrow the list of resources returned.
           C(sort): The sort order of the returned data set."
      required: false
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about all SAN Managers
  oneview_san_manager_facts:
    config: "{{ config_path }}"

- debug: var=san_managers

- name: Gather paginated, filtered and sorted facts about SAN Managers
  oneview_san_manager_facts:
    config: "{{ config_path }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      query: isInternal eq false
  delegate_to: localhost

- debug: var=san_managers

- name: Gather facts about a SAN Manager by provider display name
  oneview_san_manager_facts:
    config: "{{ config_path }}"
    provider_display_name: "Brocade Network Advisor"

- debug: var=san_managers
'''

RETURN = '''
san_managers:
    description: Has all the OneView facts about the SAN Managers.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class SanManagerFactsModule(OneViewModuleBase):
    argument_spec = dict(
        provider_display_name=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(SanManagerFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.san_managers

    def execute_module(self):
        if self.module.params.get('provider_display_name'):
            provider_display_name = self.module.params['provider_display_name']
            san_manager = self.oneview_client.san_managers.get_by_provider_display_name(provider_display_name)
            if san_manager:
                resources = [san_manager]
            else:
                resources = []
        else:
            resources = self.oneview_client.san_managers.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(san_managers=resources))


def main():
    SanManagerFactsModule().run()


if __name__ == '__main__':
    main()
