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
module: oneview_sas_logical_interconnect_group
short_description: Manage OneView SAS Logical Interconnect Group resources.
description:
    - Provides an interface to manage SAS Logical Interconnect Group resources. Can create, update, or delete.
version_added: "2.4"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
        description:
            - Indicates the desired state for the SAS Logical Interconnect Group resource.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
      description:
        - List with the SAS Logical Interconnect Group properties.
      required: true
notes:
    - This resource is only available on HPE Synergy

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Ensure that the SAS Logical Interconnect Group is present
  oneview_sas_logical_interconnect_group:
    config: "{{ config }}"
    state: present
    data:
      name: "Test SAS Logical Interconnect Group"
      state: "Active"
      interconnectMapTemplate:
        interconnectMapEntryTemplates:
          - logicalLocation:
              locationEntries:
                - type: "Bay"
                  relativeValue: "1"
                - type: "Enclosure"
                  relativeValue: "1"
            enclosureIndex: "1"
            permittedInterconnectTypeUri: "/rest/sas-interconnect-types/Synergy12GbSASConnectionModule"
          - logicalLocation:
              locationEntries:
                - type: "Bay"
                  relativeValue: "4"
                - type: "Enclosure"
                  relativeValue: "1"
            enclosureIndex: "1"
            permittedInterconnectTypeUri: "/rest/sas-interconnect-types/Synergy12GbSASConnectionModule"
      enclosureType: "SY12000"
      enclosureIndexes: [1]
      interconnectBaySet: "1"

- name: Ensure that the SAS Logical Interconnect Group is present with name 'Test'
  oneview_sas_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: present
    data:
      name: 'New SAS Logical Interconnect Group'
      newName: 'Test'

- name: Ensure that the SAS Logical Interconnect Group is absent
  oneview_sas_logical_interconnect_group:
    config: "{{ config_file_path }}"
    state: absent
    data:
      name: 'New SAS Logical Interconnect Group'
'''

RETURN = '''
sas_logical_interconnect_group:
    description: Has the facts about the OneView SAS Logical Interconnect Group.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class SasLogicalInterconnectGroupModule(OneViewModuleBase):
    MSG_CREATED = 'SAS Logical Interconnect Group created successfully.'
    MSG_UPDATED = 'SAS Logical Interconnect Group updated successfully.'
    MSG_DELETED = 'SAS Logical Interconnect Group deleted successfully.'
    MSG_ALREADY_PRESENT = 'SAS Logical Interconnect Group is already present.'
    MSG_ALREADY_ABSENT = 'SAS Logical Interconnect Group is already absent.'
    RESOURCE_FACT_NAME = 'sas_logical_interconnect_group'

    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):
        super(SasLogicalInterconnectGroupModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                                validate_etag_support=True)

        self.resource_client = self.oneview_client.sas_logical_interconnect_groups

    def execute_module(self):

        resource = self.get_by_name(self.data.get('name'))

        if self.state == 'present':
            return self.resource_present(resource, self.RESOURCE_FACT_NAME)
        elif self.state == 'absent':
            return self.resource_absent(resource)


def main():
    SasLogicalInterconnectGroupModule().run()


if __name__ == '__main__':
    main()
