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
module: oneview_switch
short_description: Provides an interface to remove ToR Switch resources.
description:
    - Provides an interface to remove Top of Rack(ToR) Switch resources.
      The switch resource will be removed if it is in an unmanaged state.
      If the switch resource is associated with a Logical Switch, it's removal is treated as a hardware removal only.
      A reference to the switch is mantained, and the resource is marked as 'Absent'.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Switch resource.
              C(absent) will remove the resource from OneView, if it exists.
              C(ports_updated) will update the switch ports.
        choices: ['absent', 'ports_updated']
    name:
      description:
        - Switch name.
      required: true

notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Delete the Switch
  oneview_switch:
    config: "{{ config }}"
    state: absent
    name: "172.18.16.2"
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewValueError, HPOneViewResourceNotFound


class SwitchModule(OneViewModuleBase):
    MSG_DELETED = 'Switch deleted successfully.'
    MSG_ALREADY_ABSENT = 'Switch is already absent.'
    MSG_PORTS_UPDATED = "Switch ports updated successfully."
    MSG_NOT_FOUND = 'Switch not found.'

    def __init__(self):
        argument_spec = dict(
            state=dict(
                required=True,
                choices=['absent', 'ports_updated']
            ),
            data=dict(required=False, type='list'),
            name=dict(required=True, type='str'),
        )
        super(SwitchModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.switches

    def execute_module(self):
        resource = self.get_by_name(self.module.params.get('name'))

        if self.state == 'absent':
            return self.resource_absent(resource)

        if not resource:
            raise HPOneViewResourceNotFound(self.MSG_NOT_FOUND)
        else:
            return self.__update_ports(resource)

    def __update_ports(self, resource):
        self.resource_client.update_ports(id_or_uri=resource["uri"], ports=self.data)
        return dict(changed=True, msg=self.MSG_PORTS_UPDATED)


def main():
    SwitchModule().run()


if __name__ == '__main__':
    main()
