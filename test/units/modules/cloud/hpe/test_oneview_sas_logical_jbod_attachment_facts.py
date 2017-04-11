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

from oneview_module_loader import SasLogicalJbodAttachmentFactsModule
from hpe_test_utils import FactsParamsTestCase


class SasLogicalJbodAttachmentFactsSpec(unittest.TestCase,
                                        FactsParamsTestCase):
    ERROR_MSG = 'Fake message error'

    PARAMS_GET_ALL = dict(
        config='config.json',
        name=None
    )

    PARAMS_GET_BY_NAME = dict(
        config='config.json',
        name="SAS Logical JBOD Attachment 2"
    )

    SAS_JBOD_LOGICAL_ATTACHMENTS = [{"name": "SAS Logical JBOD Attachment 1"},
                                    {"name": "SAS Logical JBOD Attachment 2"}]

    def setUp(self):
        self.configure_mocks(self, SasLogicalJbodAttachmentFactsModule)
        self.resource = self.mock_ov_client.sas_logical_jbod_attachments
        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_should_get_all_sas_logical_jbod_attachments(self):
        self.resource.get_all.return_value = self.SAS_JBOD_LOGICAL_ATTACHMENTS
        self.mock_ansible_module.params = self.PARAMS_GET_ALL

        SasLogicalJbodAttachmentFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbod_attachments=(self.SAS_JBOD_LOGICAL_ATTACHMENTS))
        )

    def test_should_get_sas_logical_jbod_attachment_by_name(self):
        self.resource.get_by.return_value = [self.SAS_JBOD_LOGICAL_ATTACHMENTS[1]]
        self.mock_ansible_module.params = self.PARAMS_GET_BY_NAME

        SasLogicalJbodAttachmentFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(sas_logical_jbod_attachments=([self.SAS_JBOD_LOGICAL_ATTACHMENTS[1]]))
        )


if __name__ == '__main__':
    unittest.main()
