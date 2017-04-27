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
module: oneview_firmware_bundle
short_description: Upload OneView Firmware Bundle resources.
description:
    - Upload an SPP ISO image file or a hotfix file to the appliance.
notes:
   - "This module is non-idempotent"
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the Firmware Driver resource.
              C(present) will ensure that the firmware bundle is at OneView.
        choices: ['present']
    file_path:
      description:
        - The full path of a local file to be loaded.
      required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that the Firmware Driver is present
  oneview_firmware_bundle:
    config: "{{ config_file_path }}"
    state: present
    file_path: "/home/user/Downloads/hp-firmware-hdd-a1b08f8a6b-HPGH-1.1.x86_64.rpm"

'''

RETURN = '''
firmware_bundle:
    description: Has the facts about the OneView Firmware Bundle.
    returned: Always. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class FirmwareBundleModule(OneViewModuleBase):
    MSG_FIRMWARE_BUNDLE_UPLOADED = 'Firmware Bundle uploaded sucessfully.'

    argument_spec = dict(
        state=dict(required=True, choices=['present']),
        file_path=dict(required=True, type='str')
    )

    def __init__(self):
        super(FirmwareBundleModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        file_path = self.module.params['file_path']

        new_firmware = self.oneview_client.firmware_bundles.upload(file_path)
        return dict(changed=True,
                    msg=self.MSG_FIRMWARE_BUNDLE_UPLOADED,
                    ansible_facts=dict(firmware_bundle=new_firmware))


def main():
    FirmwareBundleModule().run()


if __name__ == '__main__':
    main()
