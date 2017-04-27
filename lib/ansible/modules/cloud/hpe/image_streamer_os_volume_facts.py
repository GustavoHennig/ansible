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
module: image_streamer_os_volume_facts
short_description: Retrieve facts about the Image Streamer OS Volumes.
description:
    - Retrieve facts about the Image Streamer OS Volumes.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author:
    - "Mariana Kreisig (@marikrg)"
options:
    name:
      description:
        - Name of the OS Volume.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all OS Volumes
  image_streamer_os_volume_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=os_volumes

- name: Gather paginated, filtered and sorted facts about OS Volumes
  image_streamer_os_volume_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: status=OK
  delegate_to: localhost

- debug: var=os_volumes

- name: Gather facts about an OS Volume by name
  image_streamer_os_volume_facts:
    config: "{{ config_path }}"
    name: "Test Volume"
  delegate_to: localhost

- debug: var=os_volumes
'''

RETURN = '''
os_volumes:
    description: The list of OS Volumes
    returned: Always, but can be empty.
    type: list
'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class OsVolumeFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(OsVolumeFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")

        if name:
            os_volumes = self.i3s_client.os_volumes.get_by('name', name)
        else:
            os_volumes = self.i3s_client.os_volumes.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(os_volumes=os_volumes))


def main():
    OsVolumeFactsModule().run()


if __name__ == '__main__':
    main()
