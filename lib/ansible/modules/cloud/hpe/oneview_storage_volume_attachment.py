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
module: oneview_storage_volume_attachment
short_description: Provides an interface to remove extra presentations from a specified server profile.
description:
    - "Provides an interface to remove extra presentations from a specified server profile."
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author: "Camila Balestrin (@balestrinc)"
options:
    state:
      description:
        - Indicates the desired state for the Storage Volume Attachment
          C(extra_presentations_removed) will remove extra presentations from a specified server profile.
      choices: ['extra_presentations_removed']
      required: true
    server_profile:
      description:
        - Server Profile name or Server Profile URI
      required: true
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Removes extra presentations from a specified server profile URI
  oneview_storage_volume_attachment:
    config: "{{ config }}"
    state: extra_presentations_removed
    server_profile: "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
  delegate_to: localhost

- debug: var=server_profile


- name: Removes extra presentations from a specified server profile name
  oneview_storage_volume_attachment:
    config: "{{ config }}"
    state: extra_presentations_removed
    server_profile: "SV-1001"
  delegate_to: localhost

- debug: var=server_profile
'''

RETURN = '''
server_profile:
    description: Has all the OneView facts about the repaired Server Profile.
    returned: Always.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase, HPOneViewResourceNotFound


class StorageVolumeAttachmentModule(OneViewModuleBase):
    PROFILE_NOT_FOUND = "Server Profile not found."
    PRESENTATIONS_REMOVED = "Extra presentations removed"

    def __init__(self):
        argument_spec = {
            "state": {"required": True, "type": 'str'},
            "server_profile": {"required": True, "type": 'str'},
        }

        super(StorageVolumeAttachmentModule, self).__init__(additional_arg_spec=argument_spec)
        self.resource_client = self.oneview_client.storage_volume_attachments

    def execute_module(self):

        data = {
            "type": "ExtraUnmanagedStorageVolumes",
            "resourceUri": self.__get_server_profile_uri(self.module.params['server_profile'])
        }

        attachment = self.oneview_client.storage_volume_attachments.remove_extra_presentations(data)
        return dict(changed=True, msg=self.PRESENTATIONS_REMOVED,
                    ansible_facts=dict(server_profile=attachment))

    def __get_server_profile_uri(self, server_profile):
        if "/" in server_profile:
            return server_profile
        else:
            profile = self.oneview_client.server_profiles.get_by_name(server_profile)

            if profile:
                return profile['uri']
            else:
                raise HPOneViewResourceNotFound(self.PROFILE_NOT_FOUND)


def main():
    StorageVolumeAttachmentModule().run()


if __name__ == '__main__':
    main()