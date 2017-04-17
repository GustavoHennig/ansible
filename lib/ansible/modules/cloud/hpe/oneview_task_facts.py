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
module: oneview_task_facts
short_description: Retrieve facts about the OneView Tasks.
description:
    - Retrieve facts about the OneView Tasks.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Bruno Souza (@bsouza)"
options:
    params:
      description:
        - "List with parameters to help filter the tasks.
          Params allowed: C(count), C(fields), C(filter), C(query), C(sort), C(start), and C(view)."
      required: false

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about the last 2 tasks
  oneview_task_facts:
    config: "{{ config }}"
    params:
      count: 2

- debug: var=tasks

- name: Gather facts about the last 2 tasks associated to Server Profile templates
  oneview_task_facts:
    config: "{{ config }}"
    params:
      count: 2
      filter: "associatedResource.resourceCategory='server-profile-templates'"

- debug: var=tasks
'''

RETURN = '''
tasks:
    description: The list of tasks.
    returned: Always, but can be null.
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class TaskFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            params=dict(required=False, type='dict')
        )
        super(TaskFactsModule, self).__init__(additional_arg_spec=argument_spec)

        self.resource_client = self.oneview_client.tasks

    def execute_module(self):
        facts = self.resource_client.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(tasks=facts))


def main():
    TaskFactsModule().run()


if __name__ == '__main__':
    main()
