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
module: oneview_appliance_time_and_locale_configuration_facts
short_description: Retrieve the facts about the OneView appliance time and locale configuration.
description:
    - Retrieve the facts about the OneView appliance time and locale configuration.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 2.0.1"
author:
    "Thiago Miotto (@tmiotto)"
extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about the Appliance time and locale configuration
  oneview_appliance_time_and_locale_configuration_facts:
    config: "{{ config_file_path }}"

- debug: var=appliance_time_and_locale_configuration
'''

RETURN = '''
appliance_time_and_locale_configuration:
    description: Has all the OneView facts about the Appliance time and locale configuration.
    returned: Always.
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class ApplianceTimeAndLocaleConfigurationFactsModule(OneViewModuleBase):
    def __init__(self):
        super(ApplianceTimeAndLocaleConfigurationFactsModule, self).__init__(additional_arg_spec=dict())

    def execute_module(self):
        appliance_time_and_locale_configuration = self.oneview_client.appliance_time_and_locale_configuration.get()
        return dict(changed=False,
                    ansible_facts=dict(appliance_time_and_locale_configuration=appliance_time_and_locale_configuration))


def main():
    ApplianceTimeAndLocaleConfigurationFactsModule().run()


if __name__ == '__main__':
    main()
