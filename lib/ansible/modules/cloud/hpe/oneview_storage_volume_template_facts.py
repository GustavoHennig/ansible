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
                    'supported_by': 'committer',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: oneview_storage_volume_template_facts
short_description: Retrieve facts about Storage Volume Templates of the OneView.
description:
    - Retrieve facts about Storage Volume Templates of the OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Storage Volume Template name.
      required: false
    options:
      description:
        - "Retrieve additional facts. Options available: C(connectableVolumeTemplates)."
      required: false
extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Storage Volume Templates
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=storage_volume_templates

- name: Gather paginated, filtered and sorted facts about Storage Volume Templates
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: 'name:descending'
      filter: status='OK'

- debug: var=storage_volume_templates

- name: Gather facts about a Storage Volume Template by name
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
    name: "FusionTemplateExample"
  delegate_to: localhost

- debug: var=storage_volume_templates


- name: Gather facts about the connectable Storage Volume Templates
  oneview_storage_volume_template_facts:
    config: "{{ config }}"
    name: "FusionTemplateExample"
    options:
      - connectableVolumeTemplates
  delegate_to: localhost

- debug: var=storage_volume_templates
- debug: var=connectable_volume_templates
'''

RETURN = '''
storage_volume_templates:
    description: Has all the OneView facts about the Storage Volume Templates.
    returned: Always, but can be null.
    type: complex

connectable_volume_templates:
    description: Has facts about the Connectable Storage Volume Templates.
    returned: When requested, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class StorageVolumeTemplateFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            name=dict(required=False, type='str'),
            options=dict(required=False, type='list'),
            params=dict(required=False, type='dict'),
        )
        super(StorageVolumeTemplateFactsModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.storage_volume_templates

    def execute_module(self):

        if self.module.params.get('name'):
            storage_volume_template = self.resource_client.get_by('name', self.module.params['name'])
        else:
            storage_volume_template = self.resource_client.get_all(**self.params)

        ansible_facts = dict(storage_volume_templates=storage_volume_template)

        if 'connectableVolumeTemplates' in self.options:
            ansible_facts['connectable_volume_templates'] = self.resource_client.get_connectable_volume_templates()

        return dict(changed=False, ansible_facts=ansible_facts)


def main():
    StorageVolumeTemplateFactsModule().run()


if __name__ == '__main__':
    main()