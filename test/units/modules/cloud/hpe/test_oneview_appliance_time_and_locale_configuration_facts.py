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

from oneview_module_loader import ApplianceTimeAndLocaleConfigurationFactsModule
from hpe_test_utils import OneViewBaseTestCase

PARAMS_GET = dict(
    config='config.json',
    name=None
)

PRESENT_CONFIGURATION = [{
    "locale": "en_US.UTF-8",
    "localeDisplayName": "English (United States)"
}]


class ApplianceTimeAndLocaleConfigurationFactsSpec(unittest.TestCase,
                                                   OneViewBaseTestCase):
    def setUp(self):
        self.configure_mocks(self, ApplianceTimeAndLocaleConfigurationFactsModule)
        self.appliance_time_and_locale_configuration = self.mock_ov_client.appliance_time_and_locale_configuration

    def test_should_get_appliance_time_and_locale_configuration(self):
        self.appliance_time_and_locale_configuration.get.return_value = PRESENT_CONFIGURATION
        self.mock_ansible_module.params = PARAMS_GET

        ApplianceTimeAndLocaleConfigurationFactsModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            ansible_facts=dict(appliance_time_and_locale_configuration=PRESENT_CONFIGURATION)
        )


if __name__ == '__main__':
    unittest.main()
