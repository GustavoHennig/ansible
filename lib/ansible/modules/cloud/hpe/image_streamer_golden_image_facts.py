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
module: image_streamer_golden_image_facts
short_description: Retrieve facts about one or more of the Image Streamer Golden Image.
description:
    - Retrieve facts about one or more of the Image Streamer Golden Image.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.1"
author:
    - "Gustavo Hennig (@GustavoHennig)"
options:
    name:
      description:
        - Golden Image name.
      required: false

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all Golden Images
  image_streamer_golden_image_facts:
    config: "{{ config }}"
  delegate_to: localhost
- debug: var=golden_images

- name: Gather paginated, filtered and sorted facts about Golden Images
  image_streamer_golden_image_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 3
      sort: name:ascending
      filter: importedFromBundle=true
  delegate_to: localhost
- debug: var=golden_images

- name: Gather facts about a Golden Image by name
  image_streamer_golden_image_facts:
    config: "{{ config }}"
    name: "{{ name }}"
  delegate_to: localhost
- debug: var=golden_images
'''

RETURN = '''
golden_images:
    description: The list of Golden Images.
    returned: Always, but can be null.
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class GoldenImageFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(GoldenImageFactsModule, self).__init__(additional_arg_spec=self.argument_spec)
        self.i3s_client = self.oneview_client.create_image_streamer_client()

    def execute_module(self):
        name = self.module.params.get("name")

        ansible_facts = {}

        if name:
            golden_images = self.i3s_client.golden_images.get_by("name", name)
        else:
            golden_images = self.i3s_client.golden_images.get_all(**self.facts_params)

        ansible_facts['golden_images'] = golden_images

        return dict(changed=False, ansible_facts=ansible_facts)


def main():
    GoldenImageFactsModule().run()


if __name__ == '__main__':
    main()
