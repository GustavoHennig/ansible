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
module: oneview_firmware_driver
short_description: Provides an interface to remove Firmware Driver resources.
version_added: "2.4"
description:
    - Provides an interface to remove Firmware Driver resources.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Firmware Driver.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['absent']
    name:
      description:
        - Firmware driver name.
      required: True
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that Firmware Driver is absent
  oneview_firmware_driver:
    config: "{{ config_file_path }}"
    state: absent
    name: "Service Pack for ProLiant.iso"
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class FirmwareDriverModule(OneViewModuleBase):
    MSG_DELETED = 'Firmware driver deleted successfully.'
    MSG_ALREADY_ABSENT = 'Firmware driver is already absent.'

    def __init__(self):
        argument_spec = dict(state=dict(required=True, choices=['absent']),
                             name=dict(required=True, type='str'))

        super(FirmwareDriverModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.firmware_drivers

    def execute_module(self):
        resource = self.get_by_name(self.module.params.get("name"))
        return self.resource_absent(resource)


def main():
    FirmwareDriverModule().run()


if __name__ == '__main__':
    main()
