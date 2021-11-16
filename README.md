Projet de session
=========================
## Description

Ce projet a été créé dans le cadre du cours Web Avancée (INF5190) à l’UQAM.

Ceci est un travail du cours ci-dessous

   * **Cours** : *Programmation Web Avancée*
   * **Sigle** : *INF5190*
   * **Session** : *Automne 2021*
   * **Université** : *Université du Québec à Montréal (UQAM)*

## Auteurs

+ Alex, XXXXXX **(XXXXXXXXXXXX)**
+ Sally Junior Jean Axel, SALLY **(SALS20029908)**

## Environnement de développement

La majorité de cette documentation a été produite par François-Xavier
Guillemette. Cette documentation est utilisée avec permission de l'auteur et la
version originale est disponible à l'adresse https://github.com/fxg42/inf2050-exemples-build/blob/master/README.md

## :clipboard: Prérequis

- Python version 3.9.0 et plus
- VirtualBox: https://www.virtualbox.org/wiki/Downloads
- Vagrant: https://www.vagrantup.com/downloads.html
- git: https://git-scm.com/downloads
- Les extensions de virtualisation (VT-x ou AMD-V) doivent être activées dans le
  BIOS de votre ordinateur.


## :wrench: Installation initiale

> :warning: L'exécution de la commande `vagrant up` prend plusieurs minutes à se
compléter. Créez un répertoire vide et placez-y le Vagrantfile et le fichier
`requirements.txt` disponibles à l'adresse https://github.com/jacquesberger/inf5190-projet-vm

### Linux / MacOS

Dans un terminal:

    $ vagrant up

### Windows

Dans cmd, powershell, cmder ou tout autre terminal:

    > vagrant.exe up



## :shell: Autres commandes

### Ouvrir une connexion SSH sur la machine virtuelle:

    $ vagrant ssh

### Sortir de la machine virtuelle:

    vagrant@vagrant$ exit

### Supprimer la machine virtuelle et libérer l'espace disque:

    $ vagrant destroy

### Arrêter la machine virtuelle

    $ vagrant halt

### Redémarrer la machine virtuelle

    $ vagrant reload


## Développement avec Python3 et Flask

### Activation de l'environnement virtuel

Une fois connecté sur la VM, il faut activer l'environnement virtuel de Python
avec la commande suivante.

    $ source /home/vagrant/inf5190_projet_venv/bin/activate

### Répertoire partagé entre l'ordinateur hôte et la VM

Le répertoire où vous avez lancé le `vagrant up` sera disponible dans la VM sous
`/vagrant`

### Installation des dépendances

Uniquement les librairies présentes dans `requirements.txt` sont permises.

    $ cd /vagrant
    $ sudo pip install -r requirements.txt

Vous êtes prêts à développer. Voici la commande pour lancer le serveur:

    $ make run

### Tests dans un fureteur

Lors de la connexion à la VM via SSH, le système d'exploitation vous donnera
l'adresse IP de la VM. Prenez l'adresse IP de l'interface `eth1`. Sinon entrez cette commande dans votre terminal pour récupérer l'adresse IP.

    $ ip a | grep eth1

Une fois l'application Flask lancée dans votre VM, utilisez le fureteur de votre
ordinateur pour accéder à l'application Flask. Vous pouvez y accéder en
utilisant l'adresse IP de eth1 et en spécifiant le port de Flask. Exemple :
http://192.168.50.12:5000/
