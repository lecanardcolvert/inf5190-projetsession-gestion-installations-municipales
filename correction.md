Liste des fonctionnalités
=========================

## Tables des matières

- [Fonctionnalités A1](#A1)
- [Fonctionnalités A2](#A2)
- [Fonctionnalités A3](#A3)
- [Fonctionnalités A4](#A4)
- [Fonctionnalités A5](#A5)
- [Fonctionnalités A6](#A6)
- [Fonctionnalités B1](#B1)
- [Fonctionnalités B2](#B2)
- [Fonctionnalités C1](#C1)
- [Fonctionnalités C2](#C2)
- [Fonctionnalités C3](#C3)
- [Fonctionnalités D1](#D1)
- [Fonctionnalités D2](#D2)
- [Fonctionnalités D3](#D3)

## Fonctionnalités A1 <a name = "A1"></a>

> Auteur: Sally Junior Jean Axel, SALLY (SALS20029908)

Dans cette fonctionnalités, il faut remplir la base de donnée avec les données provenant de
La ville de Montréal.

- La liste des piscines et installations aquatiques en format CSV :
  https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-
  4b4a-805d-9af73af03b14/download/piscines.csv

- La liste des patinoires en format XML :
  https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-
  4def-903f-db24408bacd0/download/l29-patinoire.xml

- La liste des aires de jeux d'hiver (glissades) en format XML :
  http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml

Pour tester l'application:
1. il suffit de lancer l'application

  ```sh
  make run
  ```
  Un message apparaitra dans la console.

2. Un fichier `database.db` devrait apparaitre dans le dossier `/db`
3. Il suffit de consulter la BD avec `sqlite3`
  ```sh
  # à la racine du projet
  cd app/db
  sqlite3 database.db
  sqlite3> SELECT * From Arrondissement;
  # // résultat de la requête
  sqlite3> SELECT * From Patinoire;
  # // résultat de la requête
  sqlite3> SELECT * From InstallationAquatique;
  # // résultat de la requête
  sqlite3> SELECT * From Glissade;
  # // résultat de la requête
  sqlite3> .quit
  ```
4. Fin du scénario de test

## Fonctionnalités A2 <a name = "A2"></a>

> Auteur: Sally Junior Jean Axel, SALLY (SALS20029908)

Dans cette fonctionnalité, il faut que l'application mette à jour automatiquement la BD.
Pour tester, il faut attendre à 0h00 heure de montreal et corriger ce projet qu'à cette heure.

Ou sinon, vous modifiez la cronjob pour lancer la mise à jour chaque minute. C'est plus simple et plus pratique

1. Modifier la cronjob dans le fichier `app.py`
  ```python
  update_job.add_job(
      lambda: update_database(),
      "cron",
      day="*",
      hour="0",
      minute="00",
  )
  ```
2. Pour faire une mise à jour chaque minute de chaque heure, il faut modifier comme ci-dessous:
  ```python
  update_job.add_job(
      lambda: update_database(),
      "cron",
      day="*",
      hour="*",
      minute="*",
  )
  ```
3. Supprimer une donnée dans la BD. On va supprimer l'arrondissement Anjou
  ```sh
  # à la racine du projet
  cd app/db
  sqlite3 database.db
  sqlite3> SELECT * From Arrondissement;
  # // résultat de la requête
  sqlite3> DELETE FROM Arrondissement WHERE nom="Anjou"
  # // résultat de la requête
  sqlite3> .quit
  ```

4. On lance l'application avec `make run`. Une minute plus tard, on verra un message
   s'afficher dans la console signifiant la mise à jour.

5. Consulter la BD après la mise à jour
  ```sh
  # à la racine du projet
  cd app/db
  sqlite3 database.db
  sqlite3> SELECT * From Arrondissement;
  # // résultat de la requête. On devrait revoir Anjou.
  sqlite3> .quit
  ```
6. Fin du scénario de test

## Fonctionnalités A3 <a name = "A3"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Cette fonctionnalité consiste à générer la doc de l'API
Pour tester cette fonctionnalité, il faut:

1. Lancer l'application avec `make run`
2. Dans votre fureteur, il faut se rendre à l'adresse `http://<ip_de_votre_machine_vagrant>:5000/doc`3. Fin du scénario de test

## Fonctionnalités A4 <a name = "A4"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Pour tester cette fonctionnalité, il faut juste lancer une requête `GET` (avec l'outil de votre choix)

à l'url `/api/v1/installations?arrondissement=##` où \#\# represente le nom de l'arrondissement
que vous recherchez.
1. `GET /api/v1/installations?arrondissement=Verdun`
2. Vous allez recevoir un JSON avec toutes les installations de Verdun.
  2a. Si Verdun n'est pas dans la BD, alors vous recevrez un JSON avec des valeurs vide.
3. fin du scénario de test

## Fonctionnalités A5 <a name = "A5"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Pour tester cette fonctionnalité:
1. Lancer l'application
2. Se rendre sur la route `/` (page d'accueil)
3. Cliquer sur `Par arrondissement` pour faire une recherche par nom
4. Saisir l'arrondissement dans la barre de recherche et cliquer sur le bouton de recherche.
5. Le résultat s'affichera dans le tableau présent sur la page
6. Fin du scénario de test

_NB_: Il est a préciser que les résultats sont rangés par type d'installations.
Il faut donc consulter chacune des catégories. Il est possible par exemple qu'un
arrondissement n'ai pas de glissade mais a une patinoire.

## Fonctionnalités A6 <a name = "A6"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Pour tester cette fonctionnalité:
1. Lancer l'application
2. Se rendre sur la route `/` (page d'accueil)
3. Cliquer sur `Par nom` pour faire une recherche par nom
4. Sélectionner une installation et cliquer sur le bouton de recherche
5. Le résultat s'affichera dans le tableau présent sur la page
6. Fin du scénario de test

_NB_: Il est a préciser que les résultats sont rangés par type d'installations.
Il faut donc consulter chacune des catégories. Il est possible par exemple qu'un
arrondissement n'ai pas de glissade mais a une patinoire.

## Fonctionnalités B1 <a name = "B1"></a>

> Auteur: Sally Junior Jean Axel, SALLY (SALS20029908)

Cette fonctionnalité consiste à notifier par courriel lorsqu'il y'a une nouvelle installation
dans la BD. Pour cela, un compte gmail(vziguehi@gmail.com) a été créé pour l'application.
Vous aurez donc à ajouter les variables d'environnement suivante: pour que ça fonctionne.

1. Entrez ces commandes dans votre shell:
  ```sh
  # GMAIL config
  export INF5190_SERVER_MAIL="vziguehi@gmail.com"
  export INF5190_MAIL_SERVER_PASSWORD="cwidszwepzojqvim"
  ```
2. Changer le destinataire dans le fichier `config.yml`
  ```yml
  mail:
    recipient: "Courriel du destinataire"
    subject: "INF5190 - PROJET DE SESSION"
  ```
3. Refaire les étapes 1 à 4 de la [fonctionnalité A2](#A2)
4. Des messages apparaitront dans la console.
5. Consulter la boite courriel du destinataire pour voir le résultat

_NB_: Techniquement les credentials ne devrait pas être sur git. Mais comme c'est un cadre académique c'est toléré.

## Fonctionnalités B2 <a name = "B2"></a>

> Auteur: Sally Junior Jean Axel, SALLY (SALS20029908)

Cette fonctionnalité consiste à notifier sur twitter lorsqu'il y'a une nouvelle installation
dans la BD. Pour cela, un compte [twitter](https://twitter.com/VZiguehi) a été créé pour l'application.
Vous aurez donc à ajouter les variables d'environnement suivante: pour que ça fonctionne.

1. Entrez ces commandes dans votre shell:
  ```sh
  export TWITTER_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAHJgWwEAAAAAmF%2BRUCkGnXr36ZjonPc%2BSmd2l5E%3DSwx3bYxssApEEvbyh24b88420KOo8oDhjNWzxg6lCuAVbdOGGX"
  export TWITTER_CONSUMER_KEY="B20xvvSd9lMJOGwatOGaBlyNJ"
  export TWITTER_CONSUMER_SECRET="K85fNFZDULXAOaEp2WuvQlPygDxOaflGxpp1FUKE3epYn5Wwa1"
  export TWITTER_ACCESS_TOKEN="1469464467071242260-tlCcp7kxOqjAS7nciMBHFzv5F5oYLd"
  export TWITTER_ACCESS_TOKEN_SECRET="RcairhtImif4G2xogUbGKkEIP5RbUWJDfNCogBesdn5ZX"
  ```
2. Refaire les étapes 1 à 4 de la [fonctionnalité A2](#A2)
3. Des messages apparaitront dans la console.
4. Consulter le compte [twitter](https://twitter.com/VZiguehi) pour voir le résultat

_NB_: Techniquement les credentials ne devrait pas être sur git. Mais comme c'est un cadre académique c'est toléré.

## Fonctionnalités C1 <a name = "C1"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Il faut ici récupérer toutes les installations qui ont été mise à jour en 2021
Pour tester cette fonctionnalité, il faut juste lancer une requête `GET` (avec l'outil de votre choix)

à l'url `/api/v1/installations-maj-2021`
que vous recherchez.
1. `GET /api/v1/installations-maj-2021`
2. Vous allez recevoir un JSON avec toutes les installations mise à jour en 2021
3. fin du scénario de test

## Fonctionnalités C2 <a name = "C2"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Pour tester cette fonctionnalité, il faut juste lancer une requête `GET` (avec l'outil de votre choix)

à l'url `/api/v1/installations-maj-2021.xml`
que vous recherchez.
1. `GET /api/v1/installations-maj-2021.xml`
2. Vous allez recevoir un XML avec toutes les installations mise à jour en 2021
3. fin du scénario de test

## Fonctionnalités C3 <a name = "C3"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Pour tester cette fonctionnalité, il faut juste lancer une requête `GET` (avec l'outil de votre choix)

à l'url `/api/v1/installations-maj-2021.csv`
que vous recherchez.
1. `GET /api/v1/installations-maj-2021.csv`
2. Vous allez recevoir un CSV avec toutes les installations mise à jour en 2021
3. fin du scénario de test


## Fonctionnalités D1 <a name = "D1"></a>

> Auteur: Sally Junior Jean Axel, SALLY (SALS20029908)

Pour tester cette fonctionnalité, il faut lancer une requête `PUT` (avec l'outil de votre choix)
à l'url `/api/v1/installations/glissades/<id>` où _id_ est l'identifiant de la glissade à modifier
que vous recherchez.
1. `PUT /api/v1/installations/glissades/1`
  1a. Pour le corps de la requête, il est préférable de consulter la doc faire au point [A3](#A3)
2. Vous allez recevoir un JSON avec le contenu de la réponse (voir doc)
3. fin du scénario de test

## Fonctionnalités D2 <a name = "D2"></a>

> Auteur: Sally Junior Jean Axel, SALLY (SALS20029908)

Pour tester cette fonctionnalité, il faut lancer une requête `DELETE` (avec l'outil de votre choix)
à l'url `/api/v1/installations/glissades/<id>` où _id_ est l'identifiant de la glissade à modifier
que vous recherchez.
1. `DELETE /api/v1/installations/glissades/1`
  1a. Pour le corps de la requête, il est préférable de consulter la doc faire au point [A3](#A3)
2. Vous allez recevoir un JSON avec le contenu de la réponse (voir doc)
3. fin du scénario de test

## Fonctionnalités D3 <a name = "D3"></a>

> Auteur:

## Fonctionnalités D4 <a name = "D3"></a>

> Auteur:

## Fonctionnalités F1 <a name = "D3"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Voici le lien du projet sur: [Heroku](https://inf5190-projetsession.herokuapp.com):

## Fonctionnalités E1 <a name = "E1"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Pour tester cette fonctionnalité, il faut lancer une requête `POST` (avec l'outil de votre choix)
à l'url `/api/v1/subscribers`
que vous recherchez.
1. `PUT /api/v1/subscribers`
  1a. Pour le corps de la requête, il est préférable de consulter la doc faire au point [A3](#A3)
2. Vous allez recevoir un JSON avec le contenu de la réponse (voir doc)
3. fin du scénario de test

## Fonctionnalités E2 <a name = "E2"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Pour tester cette fonctionnalité:
1. Lancer l'application
2. Se rendre sur la route `/` (page d'accueil)
3. Cliquer sur `S'abonner`
4. Remplisser le formulaire et valider en cliquant sur `S'abonner`
5. Une page de succès s'affichera en cas de succès.
6. Fin du scénario de test

## Fonctionnalités E3 <a name = "E3"></a>

> Auteur: H. Bourdeau, Alexandre (HAMA12128907)

Pour tester cette fonctionnalité, il faut:
1. Lancer l'application
2. Aller directement au lien pour créer un nouvel abonné
3. Écrivez une vraie adresse courriel et choisissez un arrondissement
4. reproduire les mêmes étapes que [A2](#A2) mais en supprimant une donnée de l'arrondissement que
  vous avez choisi précédemment
5. À la fin de la mise à jour, consultez la boite de réception de l'adresse courriel entrée à
   l'étape 3.
6. Fin du scénario
