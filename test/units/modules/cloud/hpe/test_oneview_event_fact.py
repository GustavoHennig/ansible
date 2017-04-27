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

from oneview_module_loader import EventFactsModule
from hpe_test_utils import FactsParamsTestCase

ERROR_MSG = 'Fake message error'

PARAMS_GET_ALL = dict(
    config='config.json',
    name=None
)

PARAMS_GET_BY_NAME = dict(
    config='config.json',
    name="Test Event"
)

PRESENT_EVENTS = [{
    "name": "Test Event",
    "uri": "/rest/event/c6bf9af9-48e7-4236-b08a-77684dc258a5"
}]


class EventFactsSpec(unittest.TestCase, FactsParamsTestCase):
    def setUp(self):
        self.configure_mocks(self, EventFactsModule)
        self.events = self.mock_ov_client.events
        FactsParamsTestCase.configure_client_mock(self, self.events)

    def test_should_get_all_events(self):
        self.events.get_all.return_value = PRESENT_EVENTS
        self.mock_ansible_module.params = PARAMS_GET_ALL

        EventFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(events=PRESENT_EVENTS)
        )


if __name__ == '__main__':
    unittest.main()
