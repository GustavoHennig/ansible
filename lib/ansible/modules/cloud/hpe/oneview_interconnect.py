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
module: oneview_interconnect
short_description: Manage the OneView Interconnect resources.
version_added: "2.3"
description:
    - Provides an interface to manage Interconnect resources. Can change the power state, UID light state, perform
      device reset, reset port protection, and update the interconnect ports.
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Interconnect resource.
              C('powered_on') turns the power on.
              C('powered_off') turns the power off.
              C('uid_on') turns the UID light on.
              C('uid_off') turns the UID light off.
              C('device_reset') perform a device reset.
              C('update_ports') updates the interconnect ports.
              C('reset_port_protection') triggers a reset of port protection.
        choices: [
            'powered_on',
            'powered_off',
            'uid_on',
            'uid_off',
            'device_reset',
            'update_ports',
            'reset_port_protection'
        ]
    name:
      description:
        - Interconnect name.
      required: false
    ip:
      description:
        - Interconnect IP address.
      required: false
    ports:
      description:
        - List with ports to update. This option should be used together with C('update_ports') state.
      required: false

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Turn the power off for Interconnect named '0000A66102, interconnect 2'
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'powered_off'
    name: '0000A66102, interconnect 2'

- name: Turn the UID light to 'On' for interconnect named '0000A66102, interconnect 2'
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'uid_on'
    name: '0000A66102, interconnect 2'

- name: Turn the UID light to 'Off' for interconnect that matches the ip 172.18.1.114
  oneview_interconnect:
    config: "{{ config_file_path }}"
    state: 'uid_on'
    ip: '172.18.1.114'
'''

RETURN = '''
interconnect:
    description: Has the facts about the OneView Interconnect.
    returned: Always. Can be null.
    type: complex
'''

from hpOneView.common import extract_id_from_uri
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import (OneViewModuleBase,
                                          HPOneViewResourceNotFound,
                                          HPOneViewValueError)


class InterconnectModule(OneViewModuleBase):
    MSG_MISSING_KEY = "You must provide the interconnect name or the interconnect ip address"
    MSG_INTERCONNECT_NOT_FOUND = "The Interconnect was not found."

    states = dict(
        powered_on=dict(path='/powerState', value='On'),
        powered_off=dict(path='/powerState', value='Off'),
        uid_on=dict(path='/uidState', value='On'),
        uid_off=dict(path='/uidState', value='Off'),
        device_reset=dict(path='/deviceResetState', value='Reset'),
    )

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=[
                    'powered_on',
                    'powered_off',
                    'uid_on',
                    'uid_off',
                    'device_reset',
                    'update_ports',
                    'reset_port_protection'
                ]
            ),
            name=dict(required=False, type='str'),
            ip=dict(required=False, type='str'),
            ports=dict(required=False, type='list')
        )
        super(InterconnectModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        interconnect = self.__get_interconnect()
        state_name = self.module.params['state']

        if state_name == 'update_ports':
            changed, resource = self.update_ports(interconnect)
        elif state_name == 'reset_port_protection':
            changed, resource = self.reset_port_protection(interconnect)
        else:
            state = self.states[state_name]

            if state_name == 'device_reset':
                changed, resource = self.device_reset(state, interconnect)
            else:
                changed, resource = self.change_state(state, interconnect)

        return dict(
            changed=changed,
            ansible_facts=dict(interconnect=resource)
        )

    def __get_interconnect(self):
        interconnect_ip = self.module.params['ip']
        interconnect_name = self.module.params['name']

        if interconnect_ip:
            interconnects = self.oneview_client.interconnects.get_by('interconnectIP', interconnect_ip) or []
        elif interconnect_name:
            interconnects = self.oneview_client.interconnects.get_by('name', interconnect_name) or []
        else:
            raise HPOneViewValueError(self.MSG_MISSING_KEY)

        if not interconnects:
            raise HPOneViewResourceNotFound(self.MSG_INTERCONNECT_NOT_FOUND)

        return interconnects[0]

    def change_state(self, state, resource):
        changed = False

        property_name = state['path'][1:]

        if resource[property_name] != state['value']:
            resource = self.execute_operation(resource, state['path'], state['value'])
            changed = True

        return changed, resource

    def device_reset(self, state, resource):
        updated_resource = self.execute_operation(resource, state['path'], state['value'])
        return True, updated_resource

    def execute_operation(self, resource, path, value, operation="replace"):
        return self.oneview_client.interconnects.patch(
            id_or_uri=resource["uri"],
            operation=operation,
            path=path,
            value=value
        )

    def update_ports(self, resource):
        ports = self.module.params['ports']

        if not ports:
            return False, resource

        updated_resource = self.oneview_client.interconnects.update_ports(
            id_or_uri=resource["uri"],
            ports=ports
        )

        return True, updated_resource

    def reset_port_protection(self, resource):
        updated_resource = self.oneview_client.interconnects.reset_port_protection(id_or_uri=resource['uri'])
        return True, updated_resource


def main():
    InterconnectModule().run()


if __name__ == '__main__':
    main()
