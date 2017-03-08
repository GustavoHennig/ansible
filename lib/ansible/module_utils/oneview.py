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


from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from future import standard_library
from ansible.module_utils.basic import *
from copy import deepcopy
from collections import OrderedDict
import json
import logging

standard_library.install_aliases()

logger = logging.getLogger(__name__)

try:
    from hpOneView.oneview_client import OneViewClient
    from hpOneView.exceptions import HPOneViewException

    HAS_HPE_ONEVIEW = True
except ImportError:
    HAS_HPE_ONEVIEW = False


class OneViewModuleBase(object):
    HPE_ONEVIEW_SDK_REQUIRED = 'HPE OneView Python SDK is required for this module.'

    argument_spec = dict(
        config=dict(required=False, type='str'),
        state=dict(
            required=True,
            choices=['present', 'absent']
        ),
        data=dict(required=True, type='dict')
    )

    def __init__(self, run_callback, validate_etag_support=False):

        if validate_etag_support:
            self.argument_spec['validate_etag'] = dict(
                required=False,
                type='bool',
                default=True)

        self.module = AnsibleModule(argument_spec=self.argument_spec, supports_check_mode=False)
        if not HAS_HPE_ONEVIEW:
            self.module.fail_json(msg=self.HPE_ONEVIEW_SDK_REQUIRED)

        if not self.module.params['config']:
            self.oneview_client = OneViewClient.from_environment_variables()
        else:
            self.oneview_client = OneViewClient.from_json_file(self.module.params['config'])

        self.state = self.module.params.get('state')
        self.data = self.module.params.get('data')
        self.run_callback = run_callback
        self.validate_etag_support = validate_etag_support

    def run(self):
        try:
            if self.validate_etag_support:
                if not self.module.params.get('validate_etag'):
                    self.oneview_client.connection.disable_etag_validation()

            changed, msg, ansible_facts = self.run_callback()

            self.module.exit_json(changed=changed,
                                  msg=msg,
                                  ansible_facts=ansible_facts)

        except HPOneViewException as exception:
            self.module.fail_json(msg='; '.join(str(e) for e in exception.args))


class Comparator():
    MSG_DIFF_AT_KEY = 'Difference found at key \'{0}\'. '

    @staticmethod
    def resource_compare(first_resource, second_resource):
        """
        Recursively compares dictionary contents, ignoring type and order
        Args:
            first_resource: first dictionary
            second_resource: second dictionary

        Returns:
            bool: True when equal, False when different.
        """
        resource1 = deepcopy(first_resource)
        resource2 = deepcopy(second_resource)

        debug_resources = "resource1 = {0}, resource2 = {1}".format(resource1, resource2)

        # The first resource is True / Not Null and the second resource is False / Null
        if resource1 and not resource2:
            logger.debug("resource1 and not resource2. " + debug_resources)
            return False

        # Check all keys in first dict
        for key in resource1.keys():
            if key not in resource2:
                # no key in second dict
                if resource1[key] is not None:
                    # key inexistent is equivalent to exist and value None
                    logger.debug(Comparator.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                    return False
            # If both values are null / empty / False
            elif not resource1[key] and not resource2[key]:
                continue
            elif isinstance(resource1[key], dict):
                # recursive call
                if not Comparator.resource_compare(resource1[key], resource2[key]):
                    # if different, stops here
                    logger.debug(Comparator.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                    return False
            elif isinstance(resource1[key], list):
                # change comparison function (list compare)
                if not Comparator.resource_compare_list(resource1[key], resource2[key]):
                    # if different, stops here
                    logger.debug(Comparator.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                    return False
            elif Comparator._standardize_value(resource1[key]) != Comparator._standardize_value(resource2[key]):
                # different value
                logger.debug(Comparator.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False

        # Check all keys in second dict to find missing
        for key in resource2.keys():
            if key not in resource1:
                # not exists in first dict
                if resource2[key] is not None:
                    # key inexistent is equivalent to exist and value None
                    logger.debug(Comparator.MSG_DIFF_AT_KEY.format(key) + debug_resources)
                    return False

        # no differences found
        return True

    @staticmethod
    def resource_compare_list(first_resource, second_resource):
        """
        Recursively compares lists contents, ignoring type
        Args:
            first_resource: first list
            second_resource: second list

        Returns:
            True when equal;
            False when different.

        """

        resource1 = deepcopy(first_resource)
        resource2 = deepcopy(second_resource)

        debug_resources = "resource1 = {0}, resource2 = {1}".format(resource1, resource2)

        # The second list is null / empty  / False
        if not resource2:
            logger.debug("resource 2 is null. " + debug_resources)
            return False

        if len(resource1) != len(resource2):
            # different length
            logger.debug("resources have different length. " + debug_resources)
            return False

        resource1 = sorted(resource1, key=Comparator._str_sorted)
        resource2 = sorted(resource2, key=Comparator._str_sorted)

        for i, val in enumerate(resource1):
            if isinstance(val, dict):
                # change comparison function
                if not Comparator.resource_compare(val, resource2[i]):
                    logger.debug("resources are different. " + debug_resources)
                    return False
            elif isinstance(val, list):
                # recursive call
                if not Comparator.resource_compare_list(val, resource2[i]):
                    logger.debug("lists are different. " + debug_resources)
                    return False
            elif Comparator._standardize_value(val) != Comparator._standardize_value(resource2[i]):
                # value is different
                logger.debug("values are different. " + debug_resources)
                return False

        # no differences found
        return True

    @staticmethod
    def _str_sorted(obj):
        if isinstance(obj, dict):
            return json.dumps(obj, sort_keys=True)
        else:
            return str(obj)

    @staticmethod
    def _standardize_value(value):
        """
        Convert value to string to enhance the comparison.

        Args:
            value: Any object type.

        Returns:
            str: Converted value.
        """
        if isinstance(value, float) and value.is_integer():
            # Workaround to avoid erroneous comparison between int and float
            # Removes zero from integer floats
            value = int(value)

        return str(value)


class Merger():
    @staticmethod
    def merge_list_by_key(original_list, updated_list, key, ignore_when_null=[]):
        """
        Merge two lists by the key. It basically:
        1. Adds the items that are present on updated_list and are absent on original_list.
        2. Removes items that are absent on updated_list and are present on original_list.
        3. For all items that are in both lists, overwrites the values from the original item by the updated item.

        Args:
            original_list: original list.
            updated_list: list with changes.
            key: unique identifier.
            ignore_when_null: list with the keys from the updated items that should be ignored in the merge, if its
            values are null.
        Returns:
            list: Lists merged.
        """
        if not original_list:
            return updated_list

        items_map = OrderedDict([(i[key], i.copy()) for i in original_list])

        merged_items = OrderedDict()

        for item in updated_list:
            item_key = item[key]
            if item_key in items_map:
                for ignored_key in ignore_when_null:
                    if ignored_key in item and not item[ignored_key]:
                        item.pop(ignored_key)
                merged_items[item_key] = items_map[item_key].copy()
                merged_items[item_key].update(item)
            else:
                merged_items[item_key] = item.copy()

        return [val for (_, val) in merged_items.items()]
