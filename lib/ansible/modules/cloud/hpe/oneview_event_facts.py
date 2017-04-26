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
module: oneview_event_facts
short_description: Retrieve the facts about one or more of the OneView Events.
description:
    - Retrieve the facts about one or more of the Events from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.2.0"
author:
    "Felipe Bulsoni (@fgbulsoni)"
options:
    name:
      description:
        - Event name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Events
  oneview_event_facts:
    config: "{{ config_file_path }}"

- debug: var=events

- name: Gather paginated, filtered and sorted facts about Events
  oneview_event_facts:
    config: "{{ config }}"
    params:
      start: 1
      count: 3
      sort: 'description:descending'
      filter: 'eventTypeID=hp.justATest'
- debug: var=events

'''

RETURN = '''
events:
    description: Has all the OneView facts about the Events.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class EventFactsModule(OneViewModuleBase):
    def __init__(self):

        argument_spec = dict(
            name=dict(required=False, type='str'),
            params=dict(required=False, type='dict')
        )

        super(EventFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):

        events = self.oneview_client.events.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(events=events))


def main():
    EventFactsModule().run()


if __name__ == '__main__':
    main()
