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
module: oneview_drive_enclosure_facts
short_description: Retrieve the facts about one or more of the OneView Drive Enclosures.
description:
    - Retrieve the facts about one or more of the Drive Enclosures from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Drive Enclosure name.
      required: false
    options:
      description:
        - "List with options to gather additional facts about Drive Enclosure related resources.
          Options allowed: C(portMap). To gather additional facts it is required to inform the Drive Enclosure name.
          Otherwise, these options will be ignored."
      required: false
notes:
    - This resource is only available on HPE Synergy.

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Drive Enclosures
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"

- debug: var=drive_enclosures

- name: Gather paginated, filtered and sorted facts about Drive Enclosures
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: 'status=Warning'

- debug: var=drive_enclosures

- name: Gather facts about a Drive Enclosure by name
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"
    name: Default Drive Enclosure

- debug: var=drive_enclosures

- name: Gather facts about a Drive Enclosure and the Port Map
  oneview_drive_enclosure_facts:
    config: "{{ config_file_path }}"
    name: Default Drive Enclosure
    options:
        - portMap

- debug: var=drive_enclosures
- debug: var=drive_enclosure_port_map
'''

RETURN = '''
drive_enclosures:
    description: Has all the OneView facts about the Drive Enclosures.
    returned: Always, but can be null.
    type: complex

drive_enclosure_port_map:
    description: Has all the OneView facts about the Drive Enclosure Port Map.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class DriveEnclosureFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(DriveEnclosureFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.resource_client = self.oneview_client.drive_enclosures

    def execute_module(self):
        facts = {}
        name = self.module.params.get('name')

        if name:
            drive_enclosures = self.resource_client.get_by('name', name)
            if drive_enclosures:
                drive_enclosures_uri = drive_enclosures[0]['uri']
                if self.options:
                    if self.options.get('portMap'):
                        facts['drive_enclosure_port_map'] = self.resource_client.get_port_map(drive_enclosures_uri)
        else:
            drive_enclosures = self.resource_client.get_all(**self.facts_params)

        facts['drive_enclosures'] = drive_enclosures

        return dict(changed=False, ansible_facts=facts)


def main():
    DriveEnclosureFactsModule().run()


if __name__ == '__main__':
    main()
