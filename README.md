Projet de session -- INF5190-A2021
=========================

## Crédits

La majorité de cette documentation a été produite par François-Xavier
Guillemette. Cette documentation est utilisée avec permission de l'auteur et la
version originale est disponible à l'adresse https://github.com/fxg42/inf2050-exemples-build/blob/master/README.md

## :clipboard: Prérequis

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


## :bomb: Troubleshooting

### VT-x is disabled in the BIOS for all CPU modes

Le message suivant peut subvenir lors de la première exécution de Vagrant:

    VBoxManage.exe: error: Not in a hypervisor partition (HVP=0) (VERR_NEM_NOT_AVAILABLE).
    VBoxManage.exe: error: VT-x is disabled in the BIOS for all CPU modes (VERR_VMX_MSR_ALL_VMX_DISABLED)

Les architectures Intel requièrent parfois l'activation des extensions de
virtualisation (VT-x) dans le BIOS de votre ordinateur. Vérifiez la
documentation du manufacturier pour savoir comment entrer dans le BIOS
(généralement en appuyant sur F2 ou F12 au boot). Vous pourrez alors activer
l'option.

L'option équivalente pour les architectures AMD (AMD-V) est habituellement déjà
activée et la modification du BIOS n'est pas nécessaire.


### The guest machine entered an invalid state while waiting for it to boot.

Ce message d'erreur vagrant peut apparaître pour différentes raisons.

Vérifiez d'abord que les extensions de virtualisation sont activées dans le
BIOS et que vous utilisez une version à jour de VirtualBox et que celle-ci est
adéquate pour votre système d'exploitation.

L'exécution de la commande `vagrant reload` peut être suffisante pour régler le
problème. L'exécution de `vagrant destroy` puis de `vagrant up` pourrait être
nécessaire.


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

Vous êtes prêts à développer.

### Tests dans un fureteur

Lors de la connexion à la VM via SSH, le système d'exploitation vous donnera
l'adresse IP de la VM. Prenez l'adresse IP de l'interface eth1.

Une fois l'application Flask lancée dans votre VM, utilisez le fureteur de votre
ordinateur pour accéder à l'application Flask. Vous pouvez y accéder en
utilisant l'adresse IP de eth1 et en spécifiant le port de Flask. Exemple :
http://192.168.50.12:5000/
