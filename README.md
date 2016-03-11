# ganeti_ansible_setup
Ansible roles and basic playbook for ganeti automated instance installation using instance-debootstrap

## Installation
  * edit `basicsetup-vars.yml` and change every variable to a good default.
  * Fetch ganeti_ansible_facts repo using 
    `git submodule init ; git submodule update`
  * Have fun.
```sh
GNT_RAPI_CONF=/etc/ansible/ganeti_ansible_setup/basicsetup-vars.yml ansible-playbook -i /etc/ansible/ganeti-inventory.py /etc/ansible/ganeti_ansible_setup/basicsetup.yml
```

## Ganeti instance-debootstrap integration
You may configure your Debian instances automatically applying a hook to
instance-debootstrap. Add the following file to 
`/etc/ganeti/instance-debootstrap/hooks/`

```sh
#!/bin/bash

set -e

if [ -z "$TARGET" -o ! -d "$TARGET" ]; then
  log_error "Missing target directory"
  exit 1
fi

# install ansible
export LANG=C
if [ "$PROXY" ]; then
  export http_proxy="$PROXY"
  export https_proxy="$PROXY"
fi
export DEBIAN_FRONTEND=noninteractive

chroot "$TARGET" apt-get -y --force-yes -o Dpkg::Options::="--force-confdef" \
        -o Dpkg::Options::="--force-confold" install python

ansible-playbook -c chroot -i $TARGET, -e "configure_by_env=true" \
	/etc/ansible/ganeti_ansible_setup/basicsetup.yml 
```
Due to the ganeti environment variables you have to create your instance 
specifying the full FQDN on `gnt-instance add`.
