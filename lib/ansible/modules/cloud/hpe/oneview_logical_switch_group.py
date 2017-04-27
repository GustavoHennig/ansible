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
module: oneview_logical_switch_group
short_description: Manage OneView Logical Switch Group resources.
description:
    - "Provides an interface to manage Logical Switch Group resources. Can add, update, remove."
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    state:
        description:
            - Indicates the desired state for the Logical Switch Group resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
        required: true
    data:
        description:
            - List with Logical Switch Group properties and its associated states.
        required: true
notes:
    - This resource is only available on C7000 enclosures

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a Logical Switch Group
  oneview_logical_switch_group:
    config: "{{ config }}"
    state: present
    data:
        name: "OneView Test Logical Switch Group"
        switchMapTemplate:
            switchMapEntryTemplates:
                - logicalLocation:
                    locationEntries:
                       - relativeValue: 1
                         type: "StackingMemberId"
                  # You can choose either permittedSwitchTypeName or permittedSwitchTypeUri to inform the Switch Type
                  permittedSwitchTypeName: 'Cisco Nexus 50xx'
                  permittedSwitchTypeUri: '/rest/switch-types/2f36bc8f-65d8-4ea2-9300-750180402a5e'
  delegate_to: localhost

- name: Update the Logical Switch Group
  oneview_logical_switch_group:
    config: "{{ config }}"
    state: present
    data:
        name: "OneView Test Logical Switch Group"
        newName: "Test Logical Switch Group"
        switchMapTemplate:
            switchMapEntryTemplates:
                - logicalLocation:
                    locationEntries:
                       - relativeValue: 1
                         type: "StackingMemberId"
                  permittedSwitchTypeUri: '/rest/switch-types/2f36bc8f-65d8-4ea2-9300-750180402a5e'
  delegate_to: localhost

- name: Delete the Logical Switch Group
  oneview_logical_switch_group:
    config: "{{ config }}"
    state: absent
    data:
        name: 'Test Logical Switch Group'
  delegate_to: localhost
'''

RETURN = '''
logical_switch_group:
    description: Has the OneView facts about the Logical Switch Group.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class LogicalSwitchGroupModule(OneViewModuleBase):
    MSG_CREATED = 'Logical Switch Group created successfully.'
    MSG_UPDATED = 'Logical Switch Group updated successfully.'
    MSG_ALREADY_PRESENT = 'Logical Switch Group is already present.'
    MSG_DELETED = 'Logical Switch Group deleted successfully.'
    MSG_ALREADY_ABSENT = 'Logical Switch Group is already absent.'
    MSG_SWITCH_TYPE_NOT_FOUND = 'Switch type was not found.'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(LogicalSwitchGroupModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                       validate_etag_support=True)

        self.resource_client = self.oneview_client.logical_switch_groups

    def execute_module(self):
        resource = self.get_by_name(self.data['name'])

        if self.state == 'present':
            self.__replace_name_by_uris(self.data)
            return self.resource_present(resource, 'logical_switch_group')
        elif self.state == 'absent':
            return self.resource_absent(resource)

    def __replace_name_by_uris(self, resource):
        switch_map_template = resource.get('switchMapTemplate')

        if switch_map_template:
            switch_map_entry_templates = switch_map_template.get('switchMapEntryTemplates')
            if switch_map_entry_templates:
                for value in switch_map_entry_templates:
                    permitted_switch_type_name = value.pop('permittedSwitchTypeName', None)
                    if permitted_switch_type_name:
                        value['permittedSwitchTypeUri'] = self.__get_switch_by_name(permitted_switch_type_name)['uri']

    def __get_switch_by_name(self, name):
        switch_type = self.oneview_client.switch_types.get_by('name', name)
        if switch_type:
            return switch_type[0]
        else:
            raise HPOneViewResourceNotFound(self.MSG_SWITCH_TYPE_NOT_FOUND)


def main():
    LogicalSwitchGroupModule().run()


if __name__ == '__main__':
    main()
