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
module: image_streamer_deployment_group_facts
short_description: Retrieve facts about the Image Streamer Deployment Groups.
description:
    - Retrieve facts about the Image Streamer Deployment Groups.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author:
    - "Abilio Parada (@abiliogp)"
options:
    name:
      description:
        - Name of the Deployment Group.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Deployment Groups
  image_streamer_deployment_group_facts:
    config: "{{ config }}"
  delegate_to: localhost

- debug: var=deployment_groups

- name: Gather paginated, filtered and sorted facts about Deployment Groups
  image_streamer_deployment_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: state=OK
  delegate_to: localhost

- debug: var=deployment_groups

- name: Gather facts about a Deployment Group by name
  image_streamer_deployment_group_facts:
    config: "{{ config_path }}"
    name: "OSS"
  delegate_to: localhost

- debug: var=deployment_groups
'''

RETURN = '''
deployment_groups:
    description: The list of Deployment Groups
    returned: Always, but can be empty.
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class DeploymentGroupFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(DeploymentGroupFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")

        if name:
            deployment_groups = self.i3s_client.deployment_groups.get_by('name', name)
        else:
            deployment_groups = self.i3s_client.deployment_groups.get_all(**self.params)

        return dict(changed=False, ansible_facts=dict(deployment_groups=deployment_groups))


def main():
    DeploymentGroupFactsModule().run()


if __name__ == '__main__':
    main()
