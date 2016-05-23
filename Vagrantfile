# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

  config.vm.network "forwarded_port", guest: 8000, host: 8000, auto_correct: true
  config.vm.network "forwarded_port", guest: 5432, host: 15432, auto_correct: true

  # FIXME: workaround for https://git.io/vrVIu
  config.vm.provision :shell, inline: <<SCRIPT
GALAXY=/usr/local/bin/ansible-galaxy
echo '#!/usr/bin/env python2
import sys
import os

args = sys.argv
if args[1:] == ["--help"]:
  args.insert(1, "info")

os.execv("/usr/bin/ansible-galaxy", args)
' | sudo tee $GALAXY
sudo chmod 0755 $GALAXY
SCRIPT

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
  end
  
end
