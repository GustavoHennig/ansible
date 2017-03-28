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


import unittest
import yaml

from ansible.modules.cloud.hpe.oneview_storage_volume_attachment import StorageVolumeAttachmentModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

SERVER_PROFILE_NAME = "SV-1001"

YAML_EXTRA_REMOVED_BY_NAME = """
        config: "{{ config }}"
        state: extra_presentations_removed
        server_profile: "SV-1001"
        """
YAML_EXTRA_REMOVED_BY_URI = """
        config: "{{ config }}"
        state: extra_presentations_removed
        server_profile: "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
        """

REPAIR_DATA = {
    "type": "ExtraUnmanagedStorageVolumes",
    "resourceUri": "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d"
}

MOCK_SERVER_PROFILE = {
    "affinity": "BayAndServer",
    "associatedServer": "SGH106X8RN",
    "name": "SV-1001",
    "uri": "/rest/server-profiles/e6516410-c873-4644-ab93-d26dba6ccf0d",
    "sanStorage": {
        "manageSanStorage": True,
        "volumeAttachments": [
            {
                "id": 1,
                "lun": "1",
                "lunType": "Auto",
                "state": "AttachFailed",
                "storagePaths": [
                    {
                        "connectionId": 1,
                        "isEnabled": True,
                        "storageTargets": [
                            "20:00:00:02:AC:00:08:F7"
                        ]
                    }
                ],
                "volumeStoragePoolUri": "/rest/storage-pools/280FF951-F007-478F-AC29-E4655FC76DDC",
                "volumeStorageSystemUri": "/rest/storage-systems/TXQ1010307",
                "volumeUri": "/rest/storage-volumes/89118052-A367-47B6-9F60-F26073D1D85E"
            }
        ]
    },
}


class StorageVolumeAttachmentSpec(unittest.TestCase,
                                  OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, StorageVolumeAttachmentModule)

    def test_should_remove_extra_presentation_by_profile_name(self):
        self.mock_ov_client.server_profiles.get_by_name.return_value = MOCK_SERVER_PROFILE
        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.return_value = MOCK_SERVER_PROFILE

        self.mock_ansible_module.params = yaml.load(YAML_EXTRA_REMOVED_BY_NAME)

        StorageVolumeAttachmentModule().run()

        self.mock_ov_client.server_profiles.get_by_name.assert_called_once_with(SERVER_PROFILE_NAME)
        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.assert_called_once_with(REPAIR_DATA)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageVolumeAttachmentModule.PRESENTATIONS_REMOVED,
            ansible_facts=dict(server_profile=MOCK_SERVER_PROFILE)
        )

    def test_should_fail_when_profile_name_not_found(self):
        self.mock_ov_client.server_profiles.get_by_name.return_value = None
        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.return_value = MOCK_SERVER_PROFILE

        self.mock_ansible_module.params = yaml.load(YAML_EXTRA_REMOVED_BY_NAME)

        StorageVolumeAttachmentModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(msg=StorageVolumeAttachmentModule.PROFILE_NOT_FOUND)

    def test_should_remove_extra_presentation_by_profile_uri(self):
        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.return_value = MOCK_SERVER_PROFILE

        self.mock_ansible_module.params = yaml.load(YAML_EXTRA_REMOVED_BY_URI)

        StorageVolumeAttachmentModule().run()

        self.mock_ov_client.storage_volume_attachments.remove_extra_presentations.assert_called_once_with(REPAIR_DATA)

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=StorageVolumeAttachmentModule.PRESENTATIONS_REMOVED,
            ansible_facts=dict(server_profile=MOCK_SERVER_PROFILE)
        )


if __name__ == '__main__':
    unittest.main()
