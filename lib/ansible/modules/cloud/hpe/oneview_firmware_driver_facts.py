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
module: oneview_firmware_driver_facts
short_description: Retrieve the facts about one or more of the OneView Firmware Drivers.
description:
    - Retrieve the facts about one or more of the Firmware Drivers from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    params:
      description:
        - List of params to delimit, filter and sort the list of resources.
        - "params allowed:
          C(start): The first item to return, using 0-based indexing.
          C(count): The number of resources to return.
          C(sort): The sort order of the returned data set."
      required: false
    name:
      description:
        - Firmware driver name.
      required: false
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about all Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"

- debug: var=firmware_drivers

- name: Gather paginated, filtered and sorted facts about Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'

- debug: var=firmware_drivers

- name: Gather facts about a Firmware Driver by name
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"
    name: "Service Pack for ProLiant.iso"

- debug: var=firmware_drivers
'''

RETURN = '''
firmware_drivers:
    description: Has all the OneView facts about the Firmware Drivers.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class FirmwareDriverFactsModule(OneViewModuleBase):
    def __init__(self):

        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')

        )
        super(FirmwareDriverFactsModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.firmware_drivers

    def execute_module(self):
        name = self.module.params.get("name")

        if name:
            result = self.resource_client.get_by('name', name)
        else:
            result = self.resource_client.get_all(**self.params)

        return dict(
            changed=False,
            ansible_facts=dict(firmware_drivers=result)
        )


def main():
    FirmwareDriverFactsModule().run()


if __name__ == '__main__':
    main()
