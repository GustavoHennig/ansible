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
module: oneview_rack_facts
short_description: Retrieve facts about Rack resources.
description:
    - Gets a list of rack resources. Filter by name can be used to get a specific Rack. If a name is specified, it
      is  allowed to retrieve information about the device topology.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Rack name.
      required: false
    options:
      description:
        - "Retrieve additional facts. Options available: 'deviceTopology'."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Racks
  oneview_rack_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=racks

- name: Gather paginated, filtered and sorted facts about Racks
  oneview_rack_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: 'name:descending'
      filter: "depth=1000"

- name: Gather facts about a Rack by name
  oneview_rack_facts:
    config: "{{ config }}"
    name: "Rack Name"
  delegate_to: localhost
- debug: var=racks

- name: Gather facts about the topology information for the rack
  oneview_rack_facts:
    config: "{{ config }}"
    name: "Rack Name"
    options:
      - deviceTopology
  delegate_to: localhost
- debug: var=racks
- debug: var=rack_device_topology
'''

RETURN = '''
racks:
    description: Has all the OneView facts about the Racks.
    returned: Always, but can be null.
    type: complex

rack_device_topology:
    description: Retrieves the topology information for the rack resource.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class RackFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(RackFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):

        client = self.oneview_client.racks

        facts = {}

        if self.module.params.get('name'):
            storage_volume_template = client.get_by('name', self.module.params['name'])

            options = self.module.params.get('options')
            if options and 'deviceTopology' in options and len(storage_volume_template) > 0:
                facts['rack_device_topology'] = client.get_device_topology(storage_volume_template[0]['uri'])
        else:
            params = self.module.params.get('params') or {}
            storage_volume_template = client.get_all(**params)

        facts['racks'] = storage_volume_template

        return dict(changed=False,
                    ansible_facts=facts)


def main():
    RackFactsModule().run()


if __name__ == '__main__':
    main()
