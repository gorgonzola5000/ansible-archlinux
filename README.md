# Installing Arch Linux with Ansible

This [Ansible](https://www.ansible.com/) playbook enables the automated installation of [Arch Linux](https://archlinux.org). Many settings can be influenced using variables on host, group or role level.

All roles aim to closely follow the instructions in the [Arch Linux Installation guide](https://wiki.archlinux.org/title/Installation_guide). Some tasks however go beyond the installation guide, whenever this was considered appropriate. The resulting base system can be reached via SSH logging in as `root`. Adding further tasks and roles, your Arch Linux systems can be completely deployed and maintained via Ansible, requiring only minimal manual interaction with the Arch Linux live system.


## Quick guide

Please refer to the [Wiki](https://codeberg.org/dliebich/ansible-archlinux/wiki) of this repository.

* [Preparing the Arch Linux Live System](https://codeberg.org/dliebich/ansible-archlinux/wiki/Prepare-Live-System)
* [Preparing the Ansible host](https://codeberg.org/dliebich/ansible-archlinux/wiki/Prepare-Ansible)
* [Configuration via host or group variables](https://codeberg.org/dliebich/ansible-archlinux/wiki#user-content-2-configuration)

On your Ansible host, checkout this repository and switch to a custom branch which will hold your customizations:

    $ git clone https://codeberg.org/dliebich/ansible-archlinux.git
    $ cd ansible-archlinux/
    $ git checkout -b local

This playbook has been tested with Ansible version 2.14. You can either install Ansible using the package manager of your distribution or in a Python virtual environment:

    $ python -m venv .python
    $ source .python/bin/activate
    $ pip install ansible

Apply your own customizations to the different roles. Describe your host under `host_vars/{hostname}.yml`. Any host you want to install Arch Linux on must be added to the `[bootstrap]` host group. If necessary, explicitly set the IP address of the Arch Linux live system in your inventory file using the `ansible_host` variable.

    $ ansible-playbook -k bootstrap.yml

By default, the `staging` inventory file is active in `ansible.cfg`. After successful installation of Arch Linux, remove your host from the `[bootstrap]` group and consider moving it to the `production` inventory file.


## Default passwords

This repository uses some default passwords, which you should change immediately.

1. There is an [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#changing-the-password-and-or-vault-id-on-encrypted-files) under `group_vars/all/secrets.yml`. Its default password is `ansible`.
2. The LUKS passphrase is set to `archlinux` by default.
3. The `root` password defaults to `archlinux`.

Both the LUKS passphrase and the `root` password are defined in `group_vars/all/secrets.yml`.
