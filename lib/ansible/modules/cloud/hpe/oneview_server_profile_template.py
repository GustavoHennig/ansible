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
module: oneview_server_profile_template
short_description: Manage OneView Server Profile Template resources.
description:
    - Provides an interface to create, modify, and delete server profile templates.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.1.0"
author: "Bruno Souza (@bsouza)"
options:
    state:
        description:
            - Indicates the desired state for the Server Profile Template.
              C(present) will ensure data properties are compliant with OneView.
              C(absent) will remove the resource from OneView, if it exists.
        choices: ['present', 'absent']
    data:
        description:
            - Dict with Server Profile Template properties.
        required: true
notes:
    - "For the following data, you can provide either a name  or a URI: enclosureGroupName or enclosureGroupUri,
       osDeploymentPlanName or osDeploymentPlanUri (on the osDeploymentSettings), networkName or networkUri (on the
       connections list), volumeName or volumeUri (on the volumeAttachments list), volumeStoragePoolName or
       volumeStoragePoolUri (on the volumeAttachments list), volumeStorageSystemName or volumeStorageSystemUri (on the
       volumeAttachments list), serverHardwareTypeName or  serverHardwareTypeUri, enclosureName or enclosureUri,
       firmwareBaselineName or firmwareBaselineUri (on the firmware), and sasLogicalJBODName or sasLogicalJBODUri (on
       the sasLogicalJBODs list)"

extends_documentation_fragment:
    - oneview
    - oneview.validateetag
'''

EXAMPLES = '''
- name: Create a basic connection-less server profile template (using URIs)
  oneview_server_profile_template:
    config: "{{ config }}"
    state: present
    data:
      name: "ProfileTemplate101"
      serverHardwareTypeUri: "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
      enclosureGroupUri: "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"
    delegate_to: localhost

- name: Create a basic connection-less server profile template (using names)
  oneview_server_profile_template:
    config: "{{ config }}"
    state: present
    data:
      name: "ProfileTemplate102"
      serverHardwareTypeName: "BL460c Gen8 1"
      enclosureGroupName: "EGSAS_3"
  delegate_to: localhost

- name: Delete the Server Profile Template
  oneview_server_profile_template:
    config: "{{ config }}"
    state: absent
    data:
      name: "ProfileTemplate101"
    delegate_to: localhost
'''

RETURN = '''
server_profile_template:
    description: Has the OneView facts about the Server Profile Template.
    returned: On state 'present'. Can be null.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import (OneViewModuleBase,
                                          ServerProfileReplaceNamesByUris,
                                          ServerProfileMerger,
                                          ResourceComparator)

SRV_PROFILE_TEMPLATE_CREATED = 'Server Profile Template created successfully.'
SRV_PROFILE_TEMPLATE_UPDATED = 'Server Profile Template updated successfully.'
SRV_PROFILE_TEMPLATE_DELETED = 'Server Profile Template deleted successfully.'
SRV_PROFILE_TEMPLATE_ALREADY_EXIST = 'Server Profile Template already exists.'
SRV_PROFILE_TEMPLATE_ALREADY_ABSENT = 'Server Profile Template is already absent.'
SRV_PROFILE_TEMPLATE_SRV_HW_TYPE_NOT_FOUND = 'Server Hardware Type not found: '
SRV_PROFILE_TEMPLATE_ENCLOSURE_GROUP_NOT_FOUND = 'Enclosure Group not found: '

HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'


class ServerProfileTemplateModule(OneViewModuleBase):
    argument_spec = dict(
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self):

        super(ServerProfileTemplateModule, self).__init__(additional_arg_spec=self.argument_spec,
                                                          validate_etag_support=True)

        self.resource_client = self.oneview_client.server_profile_templates

    def execute_module(self):

        template = self.resource_client.get_by_name(self.data["name"])

        if self.state == 'present':
            result = self.__present(self.data, template)
        else:
            result = self.__absent(template)

        return result

    def __present(self, data, template):

        ServerProfileReplaceNamesByUris().replace(self.oneview_client, data)

        if not template:
            changed, msg, resource = self.__create(data)
        else:
            changed, msg, resource = self.__update(data, template)

        return dict(
            changed=changed,
            msg=msg,
            ansible_facts=dict(server_profile_template=resource)
        )

    def __create(self, data):
        resource = self.resource_client.create(data)
        return True, SRV_PROFILE_TEMPLATE_CREATED, resource

    def __update(self, data, template):
        resource = template.copy()

        merged_data = ServerProfileMerger().merge_data(resource, data)

        equal = ResourceComparator.compare(merged_data, resource)

        if equal:
            msg = SRV_PROFILE_TEMPLATE_ALREADY_EXIST
        else:
            resource = self.resource_client.update(resource=merged_data, id_or_uri=merged_data["uri"])
            msg = SRV_PROFILE_TEMPLATE_UPDATED

        changed = not equal

        return changed, msg, resource

    def __absent(self, template):
        msg = SRV_PROFILE_TEMPLATE_ALREADY_ABSENT

        if template:
            self.resource_client.delete(template)
            msg = SRV_PROFILE_TEMPLATE_DELETED

        changed = template is not None
        return dict(changed=changed, msg=msg)


def main():
    ServerProfileTemplateModule().run()


if __name__ == '__main__':
    main()