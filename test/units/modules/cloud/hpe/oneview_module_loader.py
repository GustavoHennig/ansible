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
"""
This module was created because the code in this repository is shared with Ansible Core.
So, to avoid merging issues, and maintaining the tests code equal, we create a unique file to
configure the imports that change from ansible.modules.cloud.hpe.one repository to another.
"""

ONEVIEW_MODULE_UTILS_PATH = 'ansible.module_utils.oneview'

from ansible.module_utils.oneview import (HPOneViewException,
                                  HPOneViewTaskError,
                                  OneViewModuleBase,
                                  SPKeys,
                                  ServerProfileMerger,
                                  ServerProfileReplaceNamesByUris,
                                  ResourceComparator)
from ansible.modules.cloud.hpe.image_streamer_artifact_bundle import ArtifactBundleModule
from ansible.modules.cloud.hpe.image_streamer_artifact_bundle_facts import ArtifactBundleFactsModule
from ansible.modules.cloud.hpe.image_streamer_build_plan import BuildPlanModule
from ansible.modules.cloud.hpe.image_streamer_build_plan_facts import BuildPlanFactsModule
from ansible.modules.cloud.hpe.image_streamer_deployment_group_facts import DeploymentGroupFactsModule
from ansible.modules.cloud.hpe.image_streamer_deployment_plan import DeploymentPlanModule
from ansible.modules.cloud.hpe.image_streamer_deployment_plan_facts import DeploymentPlanFactsModule
from ansible.modules.cloud.hpe.image_streamer_golden_image import GoldenImageModule
from ansible.modules.cloud.hpe.image_streamer_golden_image_facts import GoldenImageFactsModule
from ansible.modules.cloud.hpe.image_streamer_os_volume_facts import OsVolumeFactsModule
from ansible.modules.cloud.hpe.image_streamer_plan_script import PlanScriptModule
from ansible.modules.cloud.hpe.image_streamer_plan_script_facts import PlanScriptFactsModule
from ansible.modules.cloud.hpe.oneview_alert_facts import AlertFactsModule
from ansible.modules.cloud.hpe.oneview_connection_template import ConnectionTemplateModule
from ansible.modules.cloud.hpe.oneview_connection_template_facts import ConnectionTemplateFactsModule
from ansible.modules.cloud.hpe.oneview_datacenter import DatacenterModule
from ansible.modules.cloud.hpe.oneview_datacenter_facts import DatacenterFactsModule
from ansible.modules.cloud.hpe.oneview_drive_enclosure import DriveEnclosureModule
from ansible.modules.cloud.hpe.oneview_drive_enclosure_facts import DriveEnclosureFactsModule
from ansible.modules.cloud.hpe.oneview_enclosure import EnclosureModule
from ansible.modules.cloud.hpe.oneview_enclosure_facts import EnclosureFactsModule
from ansible.modules.cloud.hpe.oneview_enclosure_group import EnclosureGroupModule
from ansible.modules.cloud.hpe.oneview_enclosure_group_facts import EnclosureGroupFactsModule
from ansible.modules.cloud.hpe.oneview_ethernet_network import EthernetNetworkModule
from ansible.modules.cloud.hpe.oneview_ethernet_network_facts import EthernetNetworkFactsModule
from ansible.modules.cloud.hpe.oneview_fabric import FabricModule
from ansible.modules.cloud.hpe.oneview_fabric_facts import FabricFactsModule
from ansible.modules.cloud.hpe.oneview_fc_network import FcNetworkModule
from ansible.modules.cloud.hpe.oneview_fc_network_facts import FcNetworkFactsModule
from ansible.modules.cloud.hpe.oneview_fcoe_network import FcoeNetworkModule
from ansible.modules.cloud.hpe.oneview_fcoe_network_facts import FcoeNetworkFactsModule
from ansible.modules.cloud.hpe.oneview_firmware_bundle import FirmwareBundleModule
from ansible.modules.cloud.hpe.oneview_firmware_driver import FirmwareDriverModule
from ansible.modules.cloud.hpe.oneview_firmware_driver_facts import FirmwareDriverFactsModule
from ansible.modules.cloud.hpe.oneview_interconnect import InterconnectModule
from ansible.modules.cloud.hpe.oneview_interconnect_facts import InterconnectFactsModule
from ansible.modules.cloud.hpe.oneview_interconnect_link_topology_facts import InterconnectLinkTopologyFactsModule
from ansible.modules.cloud.hpe.oneview_interconnect_type_facts import InterconnectTypeFactsModule
from ansible.modules.cloud.hpe.oneview_internal_link_set_facts import InternalLinkSetFactsModule
# from ansible.modules.cloud.hpe.oneview_logical_downlinks_facts import LogicalDownlinksFactsModule
from ansible.modules.cloud.hpe.oneview_logical_enclosure import LogicalEnclosureModule
from ansible.modules.cloud.hpe.oneview_logical_enclosure_facts import LogicalEnclosureFactsModule
from ansible.modules.cloud.hpe.oneview_logical_interconnect import LogicalInterconnectModule
from ansible.modules.cloud.hpe.oneview_logical_interconnect_facts import LogicalInterconnectFactsModule
from ansible.modules.cloud.hpe.oneview_logical_interconnect_group import LogicalInterconnectGroupModule
from ansible.modules.cloud.hpe.oneview_logical_interconnect_group_facts import LogicalInterconnectGroupFactsModule
from ansible.modules.cloud.hpe.oneview_logical_switch import LogicalSwitchModule
from ansible.modules.cloud.hpe.oneview_logical_switch_facts import LogicalSwitchFactsModule
from ansible.modules.cloud.hpe.oneview_logical_switch_group import LogicalSwitchGroupModule
from ansible.modules.cloud.hpe.oneview_logical_switch_group_facts import LogicalSwitchGroupFactsModule
from ansible.modules.cloud.hpe.oneview_managed_san import ManagedSanModule
from ansible.modules.cloud.hpe.oneview_managed_san_facts import ManagedSanFactsModule
from ansible.modules.cloud.hpe.oneview_network_set import NetworkSetModule
from ansible.modules.cloud.hpe.oneview_network_set_facts import NetworkSetFactsModule
from ansible.modules.cloud.hpe.oneview_os_deployment_plan_facts import OsDeploymentPlanFactsModule
from ansible.modules.cloud.hpe.oneview_os_deployment_server import OsDeploymentServerModule
from ansible.modules.cloud.hpe.oneview_os_deployment_server_facts import OsDeploymentServerFactsModule
from ansible.modules.cloud.hpe.oneview_power_device import PowerDeviceModule
from ansible.modules.cloud.hpe.oneview_power_device_facts import PowerDeviceFactsModule
from ansible.modules.cloud.hpe.oneview_rack import RackModule
from ansible.modules.cloud.hpe.oneview_rack_facts import RackFactsModule
from ansible.modules.cloud.hpe.oneview_san_manager import SanManagerModule
from ansible.modules.cloud.hpe.oneview_san_manager_facts import SanManagerFactsModule
from ansible.modules.cloud.hpe.oneview_sas_interconnect import SasInterconnectModule
from ansible.modules.cloud.hpe.oneview_sas_interconnect_facts import SasInterconnectFactsModule
from ansible.modules.cloud.hpe.oneview_sas_interconnect_type_facts import SasInterconnectTypeFactsModule
from ansible.modules.cloud.hpe.oneview_sas_logical_interconnect import SasLogicalInterconnectModule
from ansible.modules.cloud.hpe.oneview_sas_logical_interconnect_facts import SasLogicalInterconnectFactsModule
from ansible.modules.cloud.hpe.oneview_sas_logical_interconnect_group import SasLogicalInterconnectGroupModule
from ansible.modules.cloud.hpe.oneview_sas_logical_interconnect_group_facts import SasLogicalInterconnectGroupFactsModule
from ansible.modules.cloud.hpe.oneview_sas_logical_jbod_attachment_facts import SasLogicalJbodAttachmentFactsModule
from ansible.modules.cloud.hpe.oneview_sas_logical_jbod_facts import SasLogicalJbodFactsModule
from ansible.modules.cloud.hpe.oneview_scope import ScopeModule
from ansible.modules.cloud.hpe.oneview_scope_facts import ScopeFactsModule
from ansible.modules.cloud.hpe.oneview_server_hardware import ServerHardwareModule
from ansible.modules.cloud.hpe.oneview_server_hardware_facts import ServerHardwareFactsModule
from ansible.modules.cloud.hpe.oneview_server_hardware_type import ServerHardwareTypeModule
from ansible.modules.cloud.hpe.oneview_server_hardware_type_facts import ServerHardwareTypeFactsModule
from ansible.modules.cloud.hpe.oneview_server_profile import ServerProfileModule
from ansible.modules.cloud.hpe.oneview_server_profile_facts import ServerProfileFactsModule
from ansible.modules.cloud.hpe.oneview_server_profile_template import ServerProfileTemplateModule
from ansible.modules.cloud.hpe.oneview_server_profile_template_facts import ServerProfileTemplateFactsModule
from ansible.modules.cloud.hpe.oneview_storage_pool import StoragePoolModule
from ansible.modules.cloud.hpe.oneview_storage_pool_facts import StoragePoolFactsModule
from ansible.modules.cloud.hpe.oneview_storage_system import StorageSystemModule
from ansible.modules.cloud.hpe.oneview_storage_system_facts import StorageSystemFactsModule
from ansible.modules.cloud.hpe.oneview_storage_volume_attachment import StorageVolumeAttachmentModule
from ansible.modules.cloud.hpe.oneview_storage_volume_attachment_facts import StorageVolumeAttachmentFactsModule
from ansible.modules.cloud.hpe.oneview_storage_volume_template import StorageVolumeTemplateModule
from ansible.modules.cloud.hpe.oneview_storage_volume_template_facts import StorageVolumeTemplateFactsModule
# from ansible.modules.cloud.hpe.oneview_switch import SwitchModule
# from ansible.modules.cloud.hpe.oneview_switch_facts import SwitchFactsModule
from ansible.modules.cloud.hpe.oneview_switch_type_facts import SwitchTypeFactsModule
# from ansible.modules.cloud.hpe.oneview_task_facts import TaskFactsModule
from ansible.modules.cloud.hpe.oneview_unmanaged_device import UnmanagedDeviceModule
from ansible.modules.cloud.hpe.oneview_unmanaged_device_facts import UnmanagedDeviceFactsModule
from ansible.modules.cloud.hpe.oneview_uplink_set import UplinkSetModule
from ansible.modules.cloud.hpe.oneview_uplink_set_facts import UplinkSetFactsModule
from ansible.modules.cloud.hpe.oneview_volume import VolumeModule
from ansible.modules.cloud.hpe.oneview_volume_facts import VolumeFactsModule
