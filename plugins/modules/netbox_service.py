#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Kulakov Ilya  (@TawR1024)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: netbox_service
short_description: Creates or removes service from Netbox
description:
  - Creates or removes service from Netbox
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Kulakov Ilya (@TawR1024)
requirements:
  - pynetbox
version_added: '0.1.5'
options:
  netbox_url:
    description:
      - URL of the Netbox instance resolvable by Ansible control host
    required: true
    type: str
  netbox_token:
    description:
      - The token created within Netbox to authorize API access
    required: true
    type: str
  data:
    description:
      - Defines the service configuration
    suboptions:
      device:
        description:
          - Specifies on which device the service is running
        type: raw
      virtual_machine:
        description:
        type: raw
      port:
        description:
          - Specifies which port used by service
        type: int
      protocol:
        description:
          - Specifies which protocol used by service
        type: int
        choices:
            - 6 TCP
            - 17 UDP
      ipaddress:
        description:
          - VRF that prefix is associated with
        type: str
      description:
        description:
          - Service description
        type: str
      custom_fields:
        description:
          - Must exist in Netbox and in key/value format
        type: dict
    required: true
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: "yes"
    type: bool
"""

EXAMPLES = r"""
- name: "Create netbox service"
  connection: local
  hosts: all
  gather_facts: False

  tasks:
    - name: Create service
      netbox_service:
        netbox_url: netbox_url
        netbox_token: netbox_token
        data:
          device: Test666
          name: node-exporter
          port: 9100
          protocol: 6
        state: present

- name: "Delete netbox service"
  connection: local
  hosts: all
  gather_facts: False

  tasks:
    - name: Delete service
      netbox_service:
        netbox_url: netbox_url  
        netbox_token: netbox_token
        data:
          device: Test666
          name: node-exporter
          port: 9100
          protocol: 6
        state: absent
"""

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_ipam import (
    NetboxIpamModule,
    NB_SERVICES,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = NETBOX_ARG_SPEC
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    device=dict(required=True, type="raw"),
                    virtual_machine=dict(required=False, type="raw"),
                    name=dict(required=True, type="str"),
                    port=dict(required=True, type="int"),
                    protocol=dict(required=True, type="raw"),
                    ipaddresses=dict(required=False, type="raw"),
                    description=dict(required=False, type="str"),
                    custom_fields=dict(required=False, type=dict),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_service = NetboxIpamModule(module, NB_SERVICES)
    netbox_service.run()


if __name__ == "__main__":
    main()
