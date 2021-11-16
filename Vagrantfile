Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "private_network", type: "dhcp"
  config.vm.provision "shell", inline: <<-SHELL

    ## Installation de Python 3.9
    sudo apt-get update
    sudo apt-get install -y software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install -y python3.9

    ## Installation de venv
    sudo apt-get install -y python3.9-venv

    ## Création de l'environnement pour le TP1
    python3.9 -m venv /home/vagrant/inf5190_projet_venv

    ## Création du répertoire où mettre les sources
    mkdir /vagrant/inf5190_projet_src

    ## Installation de SQLite
    sudo apt-get install -y sqlite3
  SHELL
end
