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
module: oneview_alert_facts
short_description: Retrieve facts about the OneView Alerts.
description:
    - Retrieve facts about the OneView Alerts.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpOneView >= 3.0.0"
author: "Andressa Cruz (@asserdna)"
options:
    params:
      description:
        - "List with parameters to help filter the alerts.
          Params allowed: C(count), C(fields), C(filter), C(query), C(sort), C(start), and C(view)."
      required: false

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Gather facts about the last 2 alerts
  oneview_alert_facts:
    config: "{{ config_file_path }}"
    params:
      count: 2

- debug: var=alerts

- name: Gather facts about the alerts with state 'Cleared'
  oneview_alert_facts:
    config: "{{ config_file_path }}"
    params:
      count: 2
      filter: "alertState='Cleared'"

- debug: var=alerts

- name: Gather facts about the alerts with urgency 'High'
  oneview_alert_facts:
    config: "{{ config_file_path }}"
    params:
      count: 5
      filter: "urgency='High'"

- debug: var=alerts
'''

RETURN = '''
alerts:
    description: The list of alerts.
    returned: Always, but can be null.
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneview import OneViewModuleBase


class AlertFactsModule(OneViewModuleBase):
    def __init__(self):
        argument_spec = dict(
            params=dict(required=False, type='dict')
        )
        super(AlertFactsModule, self).__init__(additional_arg_spec=argument_spec)

    def execute_module(self):
        facts = self.oneview_client.alerts.get_all(**self.params)

        return dict(changed=False, ansible_facts=dict(alerts=facts))


def main():
    AlertFactsModule().run()


if __name__ == '__main__':
    main()
