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
module: image_streamer_build_plan_facts
short_description: Retrieve facts about one or more of the Image Streamer Build Plans.
description:
    - Retrieve facts about one or more of the Image Streamer Build Plans.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author:
    - "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Build Plan name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Build Plans
  image_streamer_build_plan_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=build_plans

- name: Gather paginated, filtered and sorted facts about Build Plans
  image_streamer_build_plan_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: oeBuildPlanType=capture
  delegate_to: localhost
- debug: var=build_plans

- name: Gather facts about a Build Plan by name
  image_streamer_build_plan_facts:
    config: "{{ config }}"
    name: "{{ name }}"
  delegate_to: localhost
- debug: var=build_plans
'''

RETURN = '''
build_plans:
    description: The list of Build Plans.
    returned: Always, but can be null.
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class BuildPlanFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        options=dict(required=False, type='list'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(BuildPlanFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")

        if name:
            build_plans = self.i3s_client.build_plans.get_by("name", name)
        else:
            build_plans = self.i3s_client.build_plans.get_all(**self.facts_params)

        return dict(changed=False, ansible_facts=dict(build_plans=build_plans))


def main():
    BuildPlanFactsModule().run()


if __name__ == '__main__':
    main()
