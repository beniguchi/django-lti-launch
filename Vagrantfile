# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

  config.vm.network "forwarded_port", guest: 8000, host: 8000, auto_correct: true
  config.vm.network "forwarded_port", guest: 5432, host: 15432, auto_correct: true

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
  end

end
