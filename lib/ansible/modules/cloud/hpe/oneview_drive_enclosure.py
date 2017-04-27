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
module: oneview_drive_enclosure
short_description: Manage OneView Drive Enclosure resources.
description:
    - Provides an interface to manage Drive Enclosure resources.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Camila Balestrin(@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the Drive Enclosure resource.
              C(power_state_set) will set the power state for the Drive Enclosure.
              C(uid_state_set) will set the uid state for the Drive Enclosure.
              C(hard_reset_state_set) will request a hard reset of the Drive Enclosure.
              C(refresh_state_set) will refresh a Drive Enclosure.
        choices: ['power_state_set', 'uid_state_set', 'hard_reset_state_set', 'refresh_state_set']
    data:
        description:
            - List with the Drive Enclosure properties.
        required: true
notes:
    - This resource is only available on HPE Synergy.

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Power off the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: power_state_set
    data:
        name: '0000A66108, bay 1'
        powerState: 'Off'

- name: Power on the UID for the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: uid_state_set
    data:
        name: '0000A66108, bay 1'
        uidState: 'On'

- name: Request a hard reset of the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: hard_reset_state_set
    data:
        name: '0000A66108, bay 1'

- name: Refresh the Drive Enclosure
  oneview_drive_enclosure:
    config: "{{ config_file_path }}"
    state: refresh_state_set
    data:
        name: '0000A66108, bay 1'
        refreshState: 'RefreshPending'
'''

RETURN = '''
drive_enclosure:
    description: Has the facts about the Drive Enclosure.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound, HPOneViewValueError


class DriveEnclosureModule(OneViewModuleBase):
    MSG_NAME_REQUIRED = 'Drive Enclosure name is required.'
    MSG_NOT_FOUND = 'Drive Enclosure with specified name not found.'
    argument_spec = dict(
        state=dict(
            required=True,
            choices=['power_state_set', 'uid_state_set', 'hard_reset_state_set', 'refresh_state_set']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(DriveEnclosureModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):

        drive_enclosure = self.__get_drive_enclosure(self.data)
        drive_enclosure_uri = drive_enclosure['uri']

        resource_updated = drive_enclosure
        changed = False

        if self.state == 'power_state_set':
            changed = self.data.get('powerState') != drive_enclosure['powerState']
            if changed:
                resource_updated = self.oneview_client.drive_enclosures.patch(
                    drive_enclosure_uri, operation='replace', path='/powerState', value=self.data.get('powerState'))

        elif self.state == 'uid_state_set':
            changed = self.data.get('uidState') != drive_enclosure['uidState']
            if changed:
                resource_updated = self.oneview_client.drive_enclosures.patch(
                    drive_enclosure_uri, operation='replace', path='/uidState', value=self.data.get('uidState'))

        elif self.state == 'hard_reset_state_set':
            changed = True
            resource_updated = self.oneview_client.drive_enclosures.patch(
                drive_enclosure_uri, operation='replace', path='/hardResetState', value='Reset')

        elif self.state == 'refresh_state_set':
            changed = True
            refresh_data = dict(refreshState=self.data.get('refreshState'))
            resource_updated = self.oneview_client.drive_enclosures.refresh_state(drive_enclosure_uri, refresh_data)

        return dict(changed=changed, ansible_facts=dict(drive_enclosure=resource_updated))

    def __get_drive_enclosure(self, data):
        name = data.get('name')
        if not name:
            raise HPOneViewValueError(self.MSG_NAME_REQUIRED)
        else:
            result = self.oneview_client.drive_enclosures.get_by('name', name)

            if not result:
                raise HPOneViewResourceNotFound(self.MSG_NOT_FOUND)

            return result[0]


def main():
    DriveEnclosureModule().run()


if __name__ == '__main__':
    main()
