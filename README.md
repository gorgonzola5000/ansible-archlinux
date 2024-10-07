# Arch Linux Bootstrap and configuration using Ansible

This project is based on [this one](https://codeberg.org/dliebich/ansible-archlinux/wiki)

This project was made to bootstrap Arch Linux with systemd-boot, LUKS on root partition, BTRFS, zram and NetworkManager and then configure your system with a sudo user, GitHub CLI, your packages and dotfiles. The goal of the post-install playbook (setup.yml) is to keep your system fresh and have all its configuration defined in code.

## Quickstart

### Fork the repo
You first need to fork this repository and then change a few things. This will make it possible to bootstrap your system in a single command on your machine afterwards.

### Variables
You need to change a few variables before you begin. Most of them are kept either in `group_vars` or `host_vars`.

1. Change `repo_url` in `group_vars/bootstrap.yml` to your repo URL.
2. Change `username` in `group_vars/dev.yml` to your username as well as `dotfiles_repo_url`
3. Delete `group_vars/all/secrets.yml`, in the same directory rename `default.secrets.yml` to `secrets.yml`, change values in this file and then encrypt them using ansible-vault:
`$ ansible-vault encrypt secrets.yml`
4. Hostname and the drive used for root partition is set in file named `inventory`. Change the hostname in the first column and drive variable
5. Lastly, change stuff in `roles/locale/vars/main.yml` to suit your needs

### ArchISO

To use `ansible-pull` you are going to need 2 packages: ansible and git. You can have them preloaded if you create a custom ISO using [this wiki page](https://wiki.archlinux.org/title/Archiso#Selecting_packages). Alternatively, you can just install them on your ArchISO during system setup by running:
```
$ pacman -Sy
$ pacman -S ansible git

```
Then, you can execute the setup script with a single command:
```
$ ansible-pull -k <your-repo-url> --checkout <branch> bootstrap.yml
```
It is going to prompt you for your password to the Ansible Vault you created and then bootstrap your system. Now, reboot.

## Post-install

If the installation succeeded you will be prompted for your LUKS partition password and then put into TTY where you should login as root using the credentials you setup. You can then execute the script that was copied to your machine to further configure your OS: `# ansible_archlinux.sh <branch_name>`.

You can now once again reboot your system and you should be good to go.

You can 'refresh' your system by running `setup.yml` on your system from time to time. It will keep your dotfiles in sync and delete any orphan packages and create your list of installed packages. 


## Contributions

If you find any issues, have any suggestions or features to implement feel free to contribute.
