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
module: oneview_event
short_description: Manage OneView Events.
description:
    - Provides an interface to manage Events. Can only create.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Felipe Bulsoni (@fgbulsoni)"
options:
    state:
        description:
            - Indicates the desired state for the Event.
              C(present) will ensure data properties are compliant with OneView. This operation is non-idempotent.
        choices: ['present']
    data:
        description:
            - List with the Event properties.
        required: true

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that the Event is present using a test type id
  oneview_event:
    config: "{{ config_file_path }}"
    state: present
    data:
      description: "This is a very simple test event"
      eventTypeID: "hp.justATest"
      eventDetails:
        - eventItemName: ipv4Address
          eventItemValue: 198.51.100.5
          isThisVarbindData: false
          varBindOrderIndex: -1
'''

RETURN = '''
event:
    description: Has the facts about the OneView Events.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class EventModule(OneViewModuleBase):
    MSG_CREATED = 'Event created successfully.'

    def __init__(self):
        additional_arg_spec = dict(data=dict(required=True, type='dict'),
                                   state=dict(
                                       required=True,
                                       choices=['present']))

        super(EventModule, self).__init__(additional_arg_spec=additional_arg_spec)

        self.resource_client = self.oneview_client.events

    def execute_module(self):
        if self.state == 'present':
            resource = self.resource_client.create(self.data)
            return dict(changed=True, msg=self.MSG_CREATED, ansible_facts=dict(event=resource))


def main():
    EventModule().run()


if __name__ == '__main__':
    main()
