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
module: oneview_sas_logical_interconnect_group_facts
short_description: Retrieve facts about one or more of the OneView SAS Logical Interconnect Groups.
description:
    - Retrieve facts about one or more of the SAS Logical Interconnect Groups from OneView.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0"
author: "Camila Balestrin (@balestrinc)"
options:
    name:
      description:
        - Name of the SAS Logical Interconnect Group.
      required: false
notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
    - oneview.factsparams
'''

EXAMPLES = '''
- name: Gather facts about all SAS Logical Interconnect Groups
  oneview_sas_logical_interconnect_group_facts:
    config: "{{ config_path }}"
- debug: var=sas_logical_interconnect_groups

- name: Gather paginated, filtered and sorted facts about SAS Logical Interconnect Groups
  oneview_sas_logical_interconnect_group_facts:
    config: "{{ config }}"
    params:
      start: 0
      count: 5
      sort: 'name:descending'
      filter: "state='Active'"
- debug: var=sas_logical_interconnect_groups

- name: Gather facts about a SAS Logical Interconnect Group by name
  oneview_sas_logical_interconnect_group_facts:
    config: "{{ config_path }}"
    name: "LIG-SLJA-1"
- debug: var=sas_logical_interconnect_groups
'''

RETURN = '''
sas_logical_interconnect_groups:
    description: Has all the OneView facts about the SAS Logical Interconnect Groups.
    returned: Always, but can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class SasLogicalInterconnectGroupFactsModule(OneViewModuleBase):
    argument_spec = dict(
        name=dict(required=False, type='str'),
        params=dict(required=False, type='dict')
    )

    def __init__(self):
        super(SasLogicalInterconnectGroupFactsModule, self).__init__(additional_arg_spec=self.argument_spec)

    def execute_module(self):
        if self.module.params['name']:
            name = self.module.params['name']
            resources = self.oneview_client.sas_logical_interconnect_groups.get_by('name', name)
        else:
            resources = self.oneview_client.sas_logical_interconnect_groups.get_all(**self.facts_params)

        return dict(changed=False,
                    ansible_facts=dict(sas_logical_interconnect_groups=resources))


def main():
    SasLogicalInterconnectGroupFactsModule().run()


if __name__ == '__main__':
    main()
