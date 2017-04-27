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
module: oneview_interconnect_facts
short_description: Retrieve facts about one or more of the OneView Interconnects.
version_added: "2.4"
description:
    - Retrieve facts about one or more of the Interconnects from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - Interconnect name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Interconnect.
          Options allowed:
          C(nameServers) gets the named servers for an interconnect.
          C(statistics) gets the statistics from an interconnect.
          C(portStatistics) gets the statistics for the specified port name on an interconnect.
          C(subPortStatistics) gets the subport statistics on an interconnect.
          C(ports) gets all interconnect ports.
          C(port) gets a specific interconnect port."
        - "To gather additional facts it is required inform the Interconnect name. Otherwise, these options will be
          ignored."
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all interconnects
  oneview_interconnect_facts:
    config: "{{ config }}"

- debug: var=interconnects

- name: Gather paginated, filtered and sorted facts about Interconnects
  oneview_interconnect_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: 'name:descending'
      filter: "enclosureName='0000A66101'"

- debug: var=interconnects

- name: Gather facts about the interconnect that matches the specified name
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'

- debug: var=interconnects


- name: Gather facts about the interconnect that matches the specified name and its name servers
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - nameServers

- debug: var=interconnects
- debug: var=interconnect_name_servers

- name: Gather facts about statistics for the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - statistics

- debug: var=interconnects
- debug: var=interconnect_statistics

- name: Gather facts about statistics for the Port named 'd3' of the Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - portStatistics: 'd3'

- debug: var=interconnects
- debug: var=interconnect_port_statistics

- name: Gather facts about statistics for the sub Port number '1' of the Interconnect named 'Enc2, interconnect 2'
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: 'Enc2, interconnect 2'
    options:
        - subPortStatistics:
            portName: 'd4'
            subportNumber: 1

- debug: var=interconnects
- debug: var=interconnect_subport_statistics

- name: Gather facts about all the Interconnect ports
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - ports

- debug: var=interconnects
- debug: var=interconnect_ports

- name: Gather facts about an Interconnect port
  oneview_interconnect_facts:
    config: "{{ config }}"
    name: '0000A66102, interconnect 2'
    options:
        - port: d1

- debug: var=interconnects
- debug: var=interconnect_port
'''

RETURN = '''
interconnects:
    description: The list of interconnects.
    returned: Always, but can be null.
    type: list

interconnect_name_servers:
    description: The named servers for an interconnect.
    returned: When requested, but can be null.
    type: list

interconnect_statistics:
    description: Has all the OneView facts about the Interconnect Statistics.
    returned: When requested, but can be null.
    type: dict

interconnect_port_statistics:
    description: Statistics for the specified port name on an interconnect.
    returned: When requested, but can be null.
    type: dict

interconnect_subport_statistics:
    description: The subport statistics on an interconnect.
    returned: When requested, but can be null.
    type: dict

interconnect_ports:
    description: All interconnect ports.
    returned: When requested, but can be null.
    type: list

interconnect_port:
    description: The interconnect port.
    returned: When requested, but can be null.
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase
from hpOneView.common import extract_id_from_uri


class InterconnectFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )
        super(InterconnectFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        interconnect_name = self.module.params['name']
        facts = dict()

        if interconnect_name:
            interconnects = self.oneview_client.interconnects.get_by('name', interconnect_name)
            facts['interconnects'] = interconnects

            if interconnects and self.module.params.get('options'):
                self.__get_options(interconnects, facts)
        else:
            facts['interconnects'] = self.oneview_client.interconnects.get_all(**self.facts_params)

        return dict(
            changed=False,
            ansible_facts=facts
        )

    def __get_options(self, interconnects, facts):
        interconnect_uri = interconnects[0]['uri']

        if self.options.get('nameServers'):
            name_servers = self.oneview_client.interconnects.get_name_servers(interconnect_uri)
            facts['interconnect_name_servers'] = name_servers

        if self.options.get('statistics'):
            facts['interconnect_statistics'] = self.oneview_client.interconnects.get_statistics(interconnect_uri)

        if self.options.get('portStatistics'):
            port_name = self.options['portStatistics']
            port_statistics = self.oneview_client.interconnects.get_statistics(interconnect_uri, port_name)
            facts['interconnect_port_statistics'] = port_statistics

        if self.options.get('subPortStatistics'):
            facts['interconnect_subport_statistics'] = None
            sub_options = self.options['subPortStatistics']
            if isinstance(sub_options, dict) and sub_options.get('portName') and sub_options.get('subportNumber'):
                facts['interconnect_subport_statistics'] = self.oneview_client.interconnects.get_subport_statistics(
                    interconnect_uri, sub_options['portName'], sub_options['subportNumber'])

        if self.options.get('ports'):
            ports = self.oneview_client.interconnects.get_ports(interconnect_uri)
            facts['interconnect_ports'] = ports

        if self.options.get('port'):
            port_name = self.options.get('port')
            port_id = "{}:{}".format(extract_id_from_uri(interconnect_uri), port_name)
            port = self.oneview_client.interconnects.get_port(interconnect_uri, port_id)
            facts['interconnect_port'] = port


def main():
    InterconnectFactsModule().run()


if __name__ == '__main__':
    main()
