#!/usr/bin/python

# Copyright: (c) 2023, Dominik Liebich
# GNU Affero General Public License v3.0+ (see LICENSES/AGPL-3.0-or-later.txt or https://www.gnu.org/licenses/agpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: uuid_facts
short_description: Get UUID of block devices

description:
    - Determines the UUID of a partition or volume and sets
      a correspondig variable in ansible_facts.

options:
    device:
        description:
          - block device to get the UUID from
        required: true
        type: str
    name:
        description:
          - suffix of the variable added to ansible_facts
        required: true
        type: str

author:
    - Dominik Liebich (@dliebich)
'''

EXAMPLES = r'''
- name: Gathering Facts - UUID of boot partition (/dev/sda1)
  uuid_facts:
    device: /dev/sda1
    name: boot
'''

RETURN = r'''
ansible_facts['uuid_boot']:
    description: UUID of given block device
    type: str
    returned: always
    sample: c16446c1-b791-4e13-abdb-ceb75e88bea1
'''

from ansible.module_utils.basic import AnsibleModule

from sys import stdout
from subprocess import run
from pathlib import Path


def run_module():
    module_args = dict(
        device = dict(type='str', required=True),
        name = dict(type='str', required=True)
    )

    result = dict(
        changed = False,
        ansible_facts = dict()
    )

    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = True
    )

    fact = "uuid_" + module.params['name']
    device = module.params['device']

    if not Path(device).is_block_device():
        module.fail_json(msg='%s does not exist or is not a block device.' % device)

    uuid = run(
        ['blkid', '-s', 'UUID', '-o', 'value', device],
        capture_output = True
    ).stdout.decode(stdout.encoding).rstrip('\n')

    result['ansible_facts'] = {
        fact: uuid
    }

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

