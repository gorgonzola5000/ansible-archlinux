#!/usr/bin/python

# Copyright: (c) 2023, Dominik Liebich
# GNU Affero General Public License v3.0+ (see LICENSES/AGPL-3.0-or-later.txt or https://www.gnu.org/licenses/agpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: systemd_bootstrap
short_description: Enables or disables services vi systemctl

description:
    - Enables or disables services vi systemctl
    - Will be used by handlers or tasks which run during bootstrapping,
      i.e. when the Arch Linux Live System is mounting the system
      drive under '/mnt'.
    - In these roles it replaces 'ansible.builtin.systemd'
    - Please use 'ansible.builtin.systemd' instead in all handlers
      and tasks not invoked during bootstrap.

options:
    name:
        description:
          - Name of Systemd unit to enable or disable
        required: true
        type: str
    state:
        description:
          - "enabled" to enable Systemd unit
          - "disabled" to disable Systemd unit
        required: false
        type: str
    chroot_mountpoint:
        description:
          - Mountpoint of chroot environment (during bootstrap)
          - empty or '/' otherwise
        required: true
        type: str

author:
    - Dominik Liebich (@dliebich)
'''

EXAMPLES = r'''
- name: Enable 'systemd-resolved.service'
  systemd_bootstrap:
    name: systemd-resolved.service
    state: enabled
    chroot_mountpoint: '{{ "/mnt" if bootstrap }}'
'''

RETURN = r'''
stdout:
    description:
      - Output from systemctl
    type: str
    returned: failed
stderr:
    description:
      - Errors from systemctl
    type: str
    returned: failed
rc:
    description:
      - Return code of systemctl
    type: int
    returned: failed
    sample: 1
'''

from ansible.module_utils.basic import AnsibleModule

from sys import stdout as terminal
from subprocess import run
from pathlib import Path


def is_enabled(unit, chroot):
    rc = run(
        chroot.split() + [ 'systemctl', 'is-enabled' ] + unit.split(),
        capture_output = True
    ).returncode

    return rc == 0


def systemctl(unit, action, chroot):
    process = run(
        chroot.split() + [ 'systemctl', action ] + unit.split(),
        capture_output = True
    )

    rc = process.returncode
    stdout = process.stdout.decode(terminal.encoding)
    stderr = process.stderr.decode(terminal.encoding)

    return rc, stdout, stderr


def run_module():
    module_args = dict(
        name = dict(type='str', required=True),
        state = dict(type='str', required=False, default='enable'),
        chroot_mountpoint = dict(type='str', required=True)
    )

    result = dict(
        changed = False
    )

    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = False
    )

    state = module.params['state'].lower()
    if not state in [ 'enabled', 'disabled' ]:
        module.fail_json(msg='Invalid parameter state: "%s"; must be either "enabled" or "disabled".' % state)
    state = state.rstrip('d')

    mnt = module.params['chroot_mountpoint'].rstrip('/')
    if not Path(mnt + '/etc/arch-release').is_file():
        module.fail_json(msg='There is no Arch Linux environment in "%s".' % mnt)

    chroot = 'arch-chroot %s' % mnt if mnt else ''
    unit = module.params['name']

    if is_enabled(unit, chroot):
        module.exit_json(**result)

    rc, stdout, stderr = systemctl(unit, state, chroot)

    if rc != 0:
        module.fail_json(
            msg = 'Failed to %s %s.' % (state, unit),
            stdout = stdout,
            stderr = stderr,
            rc = rc
        )

    result['changed'] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

