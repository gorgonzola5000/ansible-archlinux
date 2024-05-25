#!/usr/bin/python

# Copyright: (c) 2023, Dominik Liebich
# GNU Affero General Public License v3.0+ (see LICENSES/AGPL-3.0-or-later.txt or https://www.gnu.org/licenses/agpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: firmware_facts
short_description: Check whether BIOS or UEFI is present

description:
    - Tests whether the system uses a legacy BIOS or UEFI firmware
      and sets ansible_facts accordingly.

author:
    - Dominik Liebich (@dliebich)
'''


EXAMPLES = r'''
- name: Gathering Facts - UEFI or BIOS
  firmware_facts:
'''


RETURN = r'''
ansible_facts['firmware_bios']:
    description:
      - True on legacy BIOS systems, False on UEFI systems
    type: bool
    returned: always
    sample: False

ansible_facts['firmware_uefi']:
    description:
      - False on legacy BIOS systems, True on UEFI systems
    type: bool
    returned: always
    sample: True
'''


from ansible.module_utils.basic import AnsibleModule
from pathlib import Path


def run_module():
    module_args = dict()

    result = dict(
        changed = False,
        ansible_facts = dict(
            firmware_bios = True,
            firmware_uefi = False
        )
    )

    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = True
    )

    if Path('/sys/firmware/efi').is_dir():
        result['ansible_facts']['firmware_bios'] = False
        result['ansible_facts']['firmware_uefi'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

