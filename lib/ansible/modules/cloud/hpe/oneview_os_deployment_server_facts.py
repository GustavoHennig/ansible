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
module: oneview_os_deployment_server_facts
short_description: Retrieve facts about one or more OS Deployment Servers.
description:
    - Retrieve facts about one or more of the OS Deployment Servers from OneView.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.1"
author: "Camila Balestrin (@balestrinc)"
options:
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          C(start): The first item to return, using 0-based indexing.
          C(count): The number of resources to return.
          C(filter): A general filter/query string to narrow the list of items returned.
          C(sort): The sort order of the returned data set.
          C(query): A general query string to narrow the list of resources returned.
          C(fields): Specifies which fields should be returned in the result set.
          C(view): Return a specific subset of the attributes of the resource or collection, by
          specifying the name of a predefined view."
      required: false
    name:
      description:
        - OS Deployment Server name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about an OS Deployment Server and related resources.
          Options allowed: C(networks), C(appliances), and C(appliance)."
      required: false
notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about all OS Deployment Servers
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"

- debug: var=os_deployment_servers

- name: Gather facts about an OS Deployment Server by name
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"
    name: "OS Deployment Server-Name"
  delegate_to: localhost

- debug: var=os_deployment_servers

- name: Gather facts about an OS Deployment Server by name with options
  oneview_os_deployment_server_facts:
    config: "{{ config_file_path }}"
    name: 'Test-OS Deployment Server'
    options:
      - networks                    # optional
      - appliances                  # optional
      - appliance: 'Appliance name' # optional
  delegate_to: localhost

- debug: var=os_deployment_servers
- debug: var=os_deployment_server_networks
- debug: var=os_deployment_server_appliances
- debug: var=os_deployment_server_appliance
'''

RETURN = '''
os_deployment_servers:
    description: Has all the OneView facts about the OS Deployment Servers.
    returned: Always, but can be null.
    type: complex

os_deployment_server_networks:
    description: Has all the OneView facts about the OneView networks.
    returned: When requested, but can be null.
    type: complex

os_deployment_server_appliances:
    description: Has all the OneView facts about all the Image Streamer resources.
    returned: When requested, but can be null.
    type: complex

os_deployment_server_appliance:
    description: Has the facts about the particular Image Streamer resource.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class OsDeploymentServerFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(OsDeploymentServerFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        ansible_facts = {}

        if self.module.params.get('name'):
            os_deployment_servers = self.oneview_client.os_deployment_servers.get_by('name',
                                                                                     self.module.params['name'])
        else:
            os_deployment_servers = self.oneview_client.os_deployment_servers.get_all(**self.facts_params)

        if self.options:
            ansible_facts = self.__gather_optional_facts(self.options)

        ansible_facts['os_deployment_servers'] = os_deployment_servers

        return dict(changed=False,
                    ansible_facts=ansible_facts)

    def __gather_optional_facts(self, options):

        facts = {}

        if options.get('networks'):
            facts['os_deployment_server_networks'] = self.oneview_client.os_deployment_servers.get_networks()
        if options.get('appliances'):
            facts['os_deployment_server_appliances'] = self.oneview_client.os_deployment_servers.get_appliances()
        if options.get('appliance'):
            facts['os_deployment_server_appliance'] = self.oneview_client.os_deployment_servers.get_appliance_by_name(
                options.get('appliance'))

        return facts


def main():
    OsDeploymentServerFactsModule().run()


if __name__ == '__main__':
    main()
