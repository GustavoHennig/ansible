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
ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['stableinterface'],
                    'supported_by': 'curated'}

DOCUMENTATION = '''
---
module: oneview_logical_downlinks_facts
short_description: Retrieve facts about one or more of the OneView Logical Downlinks.
version_added: "2.3"
description:
    - Retrieve facts about one or more of the Logical Downlinks from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    name:
        description:
          - Logical Downlink name.
        required: false
    excludeEthernet:
        description:
          - Excludes any facts about Ethernet networks from the Logical Downlinks.
        required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Logical Downlinks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    delegate_to: localhost

- debug: var=logical_downlinks

- name: Gather paginated, filtered and sorted facts about Logical Downlinks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: "name='LDa4c64fd9-0b76-46c3-8335-0bbb76459aff (Cisco Fabric Extender for HP BladeSystem)'"

- debug: var=logical_downlinks

- name: Gather facts about all Logical Downlinks excluding any existing Ethernet networks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    excludeEthernet: true
    delegate_to: localhost

- debug: var=logical_downlinks

- name: Gather facts about a Logical Downlink by name and excluding any existing Ethernet networks
  oneview_logical_downlinks_facts:
    config: "{{ config }}"
    name: "LD415a472f-ed77-42cc-9a5e-b9bd5d096923 (HP VC FlexFabric-20/40 F8 Module)"
    excludeEthernet: true
    delegate_to: localhost

- debug: var=logical_downlinks
'''

RETURN = '''
logical_interconnects:
    description: The list of logical downlinks.
    returned: Always, but can be null.
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class LogicalDownlinksFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            excludeEthernet=dict(type='bool', default=False),
            params=dict(required=False, type='dict'),
        )
        super(LogicalDownlinksFactsModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.logical_downlinks

    def execute_module(self):
        name = self.module.params.get("name")
        excludeEthernet = self.module.params.get("excludeEthernet")
        logical_downlinks = None

        if name and excludeEthernet:
            logical_downlink_by_name = self.get_by_name(name)
            logical_downlinks = []
            if logical_downlink_by_name:
                logical_downlinks = self.resource_client.get_without_ethernet(id_or_uri=logical_downlink_by_name["uri"])
        elif name:
            logical_downlinks = self.resource_client.get_by('name', name)
        elif excludeEthernet:
            logical_downlinks = self.resource_client.get_all_without_ethernet()
        else:
            logical_downlinks = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(logical_downlinks=logical_downlinks))


def main():
    LogicalDownlinksFactsModule().run()


if __name__ == '__main__':
    main()
