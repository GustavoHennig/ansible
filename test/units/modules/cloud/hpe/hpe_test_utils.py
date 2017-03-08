#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (2016) Hewlett Packard Enterprise Development LP
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

from mock import Mock, patch
from hpOneView.oneview_client import OneViewClient


class PreloadedMocksBaseTestCaseV2(object):
    mock_ov_client_from_json_file = None

    mock_ansible_module = None
    mock_ov_client = None

    def configure_mocks(self, test_case):
        """
        Preload mocked OneViewClient instance and AnsibleModule
        Args:
            test_case (object): class instance (self) that are inheriting from ModuleContructorTestCase
            testing_class (object): class being tested
        """

        # Define OneView Client Mock (FILE)
        patcher_json_file = patch.object(OneViewClient, 'from_json_file')
        test_case.addCleanup(patcher_json_file.stop)
        self.mock_ov_client_from_json_file = patcher_json_file.start()

        # Define OneView Client Mock
        self.mock_ov_client = self.mock_ov_client_from_json_file.return_value

        # Define Ansible Module Mock
        # patcher_ansible = patch(self._testing_module + '.AnsibleModule')
        patcher_ansible = patch('_ansible.module_utils.oneview.AnsibleModule')
        test_case.addCleanup(patcher_ansible.stop)
        mock_ansible_module = patcher_ansible.start()
        self.mock_ansible_module = Mock()
        mock_ansible_module.return_value = self.mock_ansible_module
