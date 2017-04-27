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
import mock
import ansible.modules.cloud.hpe.hpe_icsp_os_deployment
from copy import deepcopy

MODULE_NAME = 'ansible.modules.cloud.hpe.hpe_icsp_os_deployment'

TASK_OS_DEPLOYMENT = {
    "icsp_host": "16.124.133.251",
    "api_version": 300,
    "username": "Administrator",
    "password": "admin",
    "server_id": "VCGYZ33007",
    "os_build_plan": "RHEL 7.2 x64",
    "personality_data": None,
    "custom_attributes": None
}

DEFAULT_SERVER = {"name": "SP-01",
                  "uri": "/uri/239",
                  "ilo": {"ipAddress": "16.124.135.239"},
                  "state": "",
                  'attributes': {'osdServerId': '123456',
                                 'osdServerSerialNumber': 'VCGYZ33007'},
                  "customAttributes": []}

DEFAULT_SERVER_UPDATED = {"name": "SP-01",
                          "uri": "/uri/239",
                          "ilo": {"ipAddress": "16.124.135.239"},
                          "state": "OK",
                          "customAttributes":
                              [{'values': [{'scope': 'server', 'value': "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"}],
                                'key': 'SSH_CERT'}]}

DEFAULT_BUILD_PLAN = {"name": "RHEL 7.2 x64", "uri": "/rest/os-deployment-build-plans/222"}


class IcspOsDeploymentSpec(unittest.TestCase):
    def setUp(self):
        self.patcher_ansible_module = mock.patch(MODULE_NAME + '.AnsibleModule')
        self.mock_ansible_module = self.patcher_ansible_module.start()

        self.mock_ansible_instance = mock.Mock()
        self.mock_ansible_module.return_value = self.mock_ansible_instance

        self.patcher_icsp_service = mock.patch(MODULE_NAME + '.hpICsp')
        self.mock_icsp = self.patcher_icsp_service.start()

        self.patcher_time_sleep = mock.patch('time.sleep', return_value=None)
        self.mock_time_sleep = self.patcher_time_sleep.start()

        self.mock_connection = mock.Mock()
        self.mock_connection.login.return_value = {}
        self.mock_icsp.connection.return_value = self.mock_connection

        self.mock_icsp_common = mock.Mock()
        self.mock_icsp.common.return_value = self.mock_icsp_common

        self.mock_icsp_jobs = mock.Mock()
        self.mock_icsp.jobs.return_value = self.mock_icsp_jobs

        self.mock_server_service = mock.Mock()
        self.mock_icsp.servers.return_value = self.mock_server_service

        self.mock_build_plans_service = mock.Mock()
        self.mock_icsp.buildPlans.return_value = self.mock_build_plans_service

    def tearDown(self):
        self.patcher_ansible_module.stop()
        self.patcher_icsp_service.stop()
        self.patcher_time_sleep.stop()

    def get_as_rest_collection(self, server):
        return {
            'members': server,
            'count': len(server)
        }

    def test_should_not_add_server_when_already_present(self):
        server_already_deployed = dict(DEFAULT_SERVER, state="OK")

        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN]),
                                                self.get_as_rest_collection([DEFAULT_SERVER])]

        self.mock_server_service.get_server.return_value = server_already_deployed

        self.mock_ansible_instance.params = TASK_OS_DEPLOYMENT

        hpe_icsp_os_deployment.main()

        self.mock_time_sleep.assert_not_called()

        self.mock_ansible_instance.exit_json.assert_called_once_with(
            changed=False, msg="Server already deployed.", ansible_facts={'icsp_server': server_already_deployed}
        )

    def test_should_fail_after_try_get_server_by_serial_21_times(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN])]

        self.mock_server_service.get_server.return_value = DEFAULT_SERVER

        self.mock_ansible_instance.params = TASK_OS_DEPLOYMENT

        with mock.patch(MODULE_NAME + '.get_server_by_serial') as mock_get_srv_ser:
            mock_get_srv_ser.return_value = None
            hpe_icsp_os_deployment.main()

        times_sleep_called = self.mock_time_sleep.call_count
        self.assertEqual(21, times_sleep_called)

        self.mock_ansible_instance.fail_json.assert_called_once_with(msg='Cannot find server in ICSP.')

    def test_should_deploy_server(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN]),
                                                self.get_as_rest_collection([DEFAULT_SERVER])]

        self.mock_server_service.get_server.side_effect = [DEFAULT_SERVER, DEFAULT_SERVER_UPDATED]

        self.mock_ansible_instance.params = TASK_OS_DEPLOYMENT

        hpe_icsp_os_deployment.main()

        times_sleep_called = self.mock_time_sleep.call_count
        self.assertEqual(0, times_sleep_called)

        self.mock_ansible_instance.exit_json.assert_called_once_with(changed=True, msg='OS Deployed Successfully.',
                                                                     ansible_facts={
                                                                         'icsp_server': DEFAULT_SERVER_UPDATED})

    def test_should_try_deploy_server_3_times(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN]),
                                                self.get_as_rest_collection([]),
                                                self.get_as_rest_collection([]),
                                                self.get_as_rest_collection([DEFAULT_SERVER])]

        self.mock_server_service.get_server.side_effect = [DEFAULT_SERVER, DEFAULT_SERVER_UPDATED]

        self.mock_ansible_instance.params = TASK_OS_DEPLOYMENT

        hpe_icsp_os_deployment.main()

        times_sleep_called = self.mock_time_sleep.call_count
        self.assertEqual(2, times_sleep_called)

        self.mock_ansible_instance.exit_json.assert_called_once_with(changed=True, msg='OS Deployed Successfully.',
                                                                     ansible_facts={
                                                                         'icsp_server': DEFAULT_SERVER_UPDATED})

    def test_should_fail_when_os_build_plan_not_found(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([]),
                                                self.get_as_rest_collection([]),
                                                self.get_as_rest_collection([]),
                                                self.get_as_rest_collection([DEFAULT_SERVER])]

        self.mock_server_service.get_server.return_value = DEFAULT_SERVER

        self.mock_ansible_instance.params = TASK_OS_DEPLOYMENT

        hpe_icsp_os_deployment.main()

        self.mock_ansible_instance.fail_json.assert_called_once_with(msg='Cannot find OS Build plan: RHEL 7.2 x64')

    def test_should_update_server_when_task_include_network_personalization(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN]),
                                                self.get_as_rest_collection([DEFAULT_SERVER])]

        self.mock_server_service.get_server.side_effect = [DEFAULT_SERVER, DEFAULT_SERVER_UPDATED]
        self.mock_icsp.common.monitor_execution.return_value = {}
        self.mock_icsp_jobs.add_job.return_value = {"job mock return"}

        task_with_network_personalization = deepcopy(TASK_OS_DEPLOYMENT)
        network_config = {"network_config": {"hostname": "test-web.io.fc.hpe.com", "domain": "demo.com"}}
        task_with_network_personalization['personality_data'] = network_config
        self.mock_ansible_instance.params = task_with_network_personalization

        hpe_icsp_os_deployment.main()

        server_data = {"serverUri": DEFAULT_SERVER['uri'], "personalityData": None}
        network_config = {"serverData": [server_data]}
        build_plan_body = {"osbpUris": [DEFAULT_BUILD_PLAN['uri']], "serverData": [server_data], "stepNo": 1}

        monitor_build_plan = mock.call(self.mock_icsp_jobs.add_job(build_plan_body), self.mock_icsp_jobs)
        monitor_update_server = mock.call(self.mock_icsp_jobs.add_job(network_config), self.mock_icsp_jobs)
        calls = [monitor_build_plan, monitor_update_server]

        self.mock_icsp.common.monitor_execution.assert_has_calls(calls)

    def test_should_update_server_when_task_include_custom_attributes(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN]),
                                                self.get_as_rest_collection([DEFAULT_SERVER])]

        self.mock_server_service.get_server.side_effect = [DEFAULT_SERVER, DEFAULT_SERVER_UPDATED]
        self.mock_server_service.update_server.return_value = DEFAULT_SERVER_UPDATED

        task_with_custom_attr = deepcopy(TASK_OS_DEPLOYMENT)
        custom_attr = [{"SSH_CERT": "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"}]
        task_with_custom_attr['custom_attributes'] = custom_attr
        self.mock_ansible_instance.params = task_with_custom_attr

        hpe_icsp_os_deployment.main()

        personality_data = deepcopy(DEFAULT_SERVER)
        personality_data['customAttributes'] = [
            {'values': [{'scope': 'server', 'value': "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"}],
             'key': 'SSH_CERT'}]

        self.mock_server_service.update_server.assert_called_once_with(personality_data)

    def test_get_server_by_serial_with_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_SERVER])]

        server = hpe_icsp_os_deployment.get_server_by_serial(self.mock_connection, 'VCGYZ33007')

        expected = {'uri': '/rest/os-deployment-servers/123456'}
        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?category=osdserver&query=\'osdServerSerialNumber:"VCGYZ33007"\'')

        self.assertEqual(server, expected)

    def test_get_server_by_serial_with_non_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_SERVER])]

        server = hpe_icsp_os_deployment.get_server_by_serial(self.mock_connection, '000')

        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?category=osdserver&query=\'osdServerSerialNumber:"000"\'')

        self.assertIsNone(server)

    def test_get_build_plan_with_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN])]

        server = hpe_icsp_os_deployment.get_build_plan(self.mock_connection, 'RHEL 7.2 x64')

        expected = {'name': 'RHEL 7.2 x64', 'uri': '/rest/os-deployment-build-plans/222'}
        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?filter="name=\'RHEL%207.2%20x64\'"&category=osdbuildplan')

        self.assertEqual(server, expected)

    def test_get_build_plan_with_non_matching_result(self):
        self.mock_connection.get.side_effect = [self.get_as_rest_collection([DEFAULT_BUILD_PLAN])]

        server = hpe_icsp_os_deployment.get_build_plan(self.mock_connection, 'BuildPlan')

        self.mock_connection.get.assert_called_once_with(
            '/rest/index/resources?filter="name=\'BuildPlan\'"&category=osdbuildplan')

        self.assertIsNone(server)


if __name__ == '__main__':
    unittest.main()