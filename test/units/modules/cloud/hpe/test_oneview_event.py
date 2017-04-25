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

from oneview_module_loader import EventModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

PARAMS_FOR_PRESENT = dict(
    config='config.json',
    state='present',
    data={
          'description': "This is a very simple test event",
          'eventTypeID': "hp.justATest",
          'eventDetails': [{
              'eventItemName': "ipv4Address",
              'eventItemValue': "198.51.100.5",
              'isThisVarbindData': "false",
              'varBindOrderIndex': -1
          }]
    }
)


class EventModuleSpec(unittest.TestCase, OneViewBaseTestCase):
    """
    OneViewBaseTestCase provides the mocks used in this test case
    """

    def setUp(self):
        self.configure_mocks(self, EventModule)
        self.resource = self.mock_ov_client.events

    def test_should_create_new_event(self):
        self.resource.get_by.return_value = []
        self.resource.create.return_value = PARAMS_FOR_PRESENT['data']

        self.mock_ansible_module.params = PARAMS_FOR_PRESENT

        EventModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=EventModule.MSG_CREATED,
            ansible_facts=dict(event=PARAMS_FOR_PRESENT['data'])
        )


if __name__ == '__main__':
    unittest.main()
