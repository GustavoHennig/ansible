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
from ansible.modules.cloud.hpe.oneview_alert_facts import AlertFactsModule
from hpe_test_utils import FactsParamsTestCase
import copy

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    params=None
)

ALL_ALERTS = [{
    "type": "AlertResourceV3",
    "alertState": "Active",
    "severity": "Warning",
    "urgency": "None",
    "description": "Utilization data has not been successfully collected for 38 minutes and 5 attempts.",
    "category": "alerts",
    "uri": "/rest/alerts/98"
}]


class TaskFactsSpec(unittest.TestCase,
                    FactsParamsTestCase):

    def setUp(self):
        self.configure_mocks(self, AlertFactsModule)
        self.resource = self.mock_ov_client.alerts
        FactsParamsTestCase.configure_client_mock(self, self.resource)

    def test_get_all(self):
        self.resource.get_all.return_value = ALL_ALERTS
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_ALL)

        AlertFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(alerts=ALL_ALERTS)
        )

    def test_get_all_with_filter(self):
        self.resource.get_all.return_value = ALL_ALERTS
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_ALL)

        AlertFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(alerts=ALL_ALERTS)
        )

    def test_get_all_with_filter_and_count(self):
        self.resource.get_all.return_value = ALL_ALERTS
        self.mock_ansible_module.params = copy.deepcopy(PARAMS_GET_ALL)

        AlertFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(alerts=ALL_ALERTS)
        )


if __name__ == '__main__':
    unittest.main()
