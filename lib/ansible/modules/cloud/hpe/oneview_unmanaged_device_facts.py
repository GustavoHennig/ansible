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
module: oneview_unmanaged_device_facts
short_description: Retrieve facts about one or more of the OneView Unmanaged Device.
description:
    - Retrieve facts about one or more of the Unmanaged Device from OneView.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    name:
      description:
        - Unmanaged Device name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about the Unmanaged Device.
          Options allowed:
          C(environmental_configuration) gets a description of the environmental configuration for the Unmnaged Device."

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Unmanaged Devices
  oneview_unmanaged_device_facts:
    config: "{{ config }}"

- debug: var=unmanaged_devices

- name: Gather paginated, filtered and sorted facts about Unmanaged Devices
  oneview_unmanaged_device_facts:
  config: "{{ config }}"
  params:
    start: 0
    count: 2
    sort: 'name:descending'
    filter: "status='Disabled'"

- debug: var=unmanaged_devices

- name: Gather facts about an Unmanaged Device by name
  oneview_unmanaged_device_facts:
    config: "{{ config }}"
    name: "{{ name }}"

- debug: var=unmanaged_devices

- name: Gather facts about an Unmanaged Device by name with environmental configuration
  oneview_unmanaged_device_facts:
    config: "{{ config }}"
    name: "{{ name }}"
    options:
      - environmental_configuration

- debug: var=unmanaged_device_environmental_configuration
'''

RETURN = '''
unmanaged_devices:
    description: The list of unmanaged devices.
    returned: Always, but can be null.
    type: list

unmanaged_device_environmental_configuration:
    description: The description of the environmental configuration for the logical interconnect.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class UnmanagedDeviceFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type="list"),
        params=dict(required=False, type='dict'),
    )

    def __init__(self):
        super(UnmanagedDeviceFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.unmanaged_devices

    def execute_module(self):
        name = self.module.params["name"]
        facts = dict()

        if name:
            unmanaged_devices = self.resource_client.get_by('name', name)
            environmental_configuration = self.__get_environmental_configuration(unmanaged_devices)

            if environmental_configuration is not None:
                facts["unmanaged_device_environmental_configuration"] = environmental_configuration
        else:
            unmanaged_devices = self.resource_client.get_all(**self.facts_params)

        facts["unmanaged_devices"] = unmanaged_devices
        return dict(ansible_facts=facts)

    def __get_environmental_configuration(self, unmanaged_devices):
        environmental_configuration = None

        if unmanaged_devices and "environmental_configuration" in self.options:
            unmanaged_device_uri = unmanaged_devices[0]["uri"]
            environmental_configuration = self.resource_client.get_environmental_configuration(
                id_or_uri=unmanaged_device_uri
            )

        return environmental_configuration


def main():
    UnmanagedDeviceFactsModule().run()


if __name__ == '__main__':
    main()
