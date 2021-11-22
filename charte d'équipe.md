Charte d'équipe
================

## I. Ententes

- On va communiquer prioritairement sur Discord
- On va développer en Agile en utilisant l'onglet projet de Github pour créer un KanBan
- Pour résoudre les conflits concernant le code: **Demander au prof ou à un démonstrateur**
- Notre définition de _"Terminé"_ est:
  - **la tâche est implémentée**,
  - **la tâche respecte les critères d'acceptation**,
  - **la tâche a été vérifié par un autre membre d'équipe grâce au pull request**
  - **la branche de la tâche a été mergée dans `dev` puis dans `main`**

## II. Règles générales d'organisation et de lisibilité du code:

Pour faire simple, nous allons **utiliser les conventions de style de PEP8**. Il faudrait donc que la
commande  ci-dessous ne retourne pas d'erreur.

    $ pycodestyle


### 1. Variables

- Pour nommer une variable, on utilisera le **snake_case**

- Les variables doivent être déclarées au tout début de la méthode/fonction dans laquelle elles existent juste pour ne pas casser le fil de lecture

```python
// Exemple
integer_variable_entiere = 0

real_variable = 0.0

bool_variable = False

object_variable = None

string_variable = ""
...
```


- **La langue privilégiée** pour le nommage des variables est l’anglais car c'est plus facile de
  faire du nommage et la taille des noms est moins long qu'en français.

- **Les noms des variables** doivent être spécifique de sortes à ce qu’on puisse comprendre ce que fait la variable juste en lisant son nom. On ne devrait pas à chaque fois demander l’assistance d’un autre membre pour comprendre ce que fait une variable.
  - Le nom doit **correspondre au contenu de la variable**
  > Exemple : `quizz_score = 0` est plus significatif et plus compréhensible que `score = 0` ou `result_integer = 0`

### 2. Constantes

Les constantes sont écrites en **UPPER_SNAKE_CASE** et le nommage doit être significatif comme pour les variables.

### 3. Méthodes et fonctions

- Elles doivent avoir une seule responsabilité (faire qu'une seule et unique chose)
- Elles ne doivent pas dépasser 25 lignes (sauf cas exceptionnel **justifiable**)
- Les nom des fonctions et des méthodes sont écrites en **snake_case**. Elles doivent avoir un nom
  siginificatif et être minimalement documentés.

- La documentation suit les standards de PEP8 (_voir PEP257_ pour plus d'info)
- La documentation devrait normalement être en anglais mais c'est à discuter avec les membres.

- Si vous avez la possibilité de
  faire une documentation complète alors faite la; ce sera un gain de temps considérable.
  L’idée derrière la documentation minimale c’est de s’assurer que tout est documenté même si
  nous n’avons pas eu le temps de faire une documentation complète. Voici ci-dessous un exemple:

  - _Documentation minimal_

   ```python
   def example_function(example_parameter):
     """Description en une ligne"""
  
     //Du code
     ...
   ```

   - _Documentation Complète_

   ```python
   def example_function(example_parameter):
     """
     Description détaillée
     
     sur....................
     plusieurs..............
     lignes..................
  
     Keyword arguments:
     example_parameter -- description du paramètre
     example_parameter2 -- description du paramètre2
  
     return
     description de la valeur retournée
     """
  
     //Du code
     ...
     return valeur
   ```
   > ATTENTION À L'INDENTATION

### 4. Classes

Les classes sont écrites en **PascalCase**. Elles doivent être préalablement documentées. (Voir le point sur les méthodes)

### 5. Indentations et blocs

On va utiliser les tabulations (_TAB_) pour le développement mais on créera plus tard une action sur github qui va les convertir en espace car
l'utilisation des espaces est standard (_Sally croit que oui_)

(Voir le point sur les méthodes pour les exemples)

### 6. Commentaire et Documentation

- La langue des commentaires et de la documentation est le **Français ou Anglais** (À discuter).
- Pour le style de la documentation, on utilise les **docstring** selon la **_convention PEP257_**.
- L’utilité de la documentation c’est la compréhension. N’oublions pas qu’on est une équipe et nous devons tout faire pour faciliter la compréhension.

## III. Environnement de développement

### 1. IDE

Pas d'IDE en particulier mais ce qui est recommandé c'est:
- Visual Studio Code
- (Neo)Vim
- Pycharm
- Tout éditeur de texte + terminal

### 2. Langages

- Python version 3.9.0 et plus....
- Flask pour framework web.
- Vagrant pour l'environnement de développement

### 3. Utilisation de Github

- On va suivre `Gitflow`

- `main` : branche principale. Elle contiendra toutes nos releases (Tout le code testé et que l’équipe aura jugé prêt à être remis)

- `dev` : Branche de développement. Elle contiendra tous les commits en rapport avec le développement. On fera nos merges dans dev puis on fera
  des tests d'acceptations avant de merge à `master`
  
- `feature/<numéro_tâche>`: branche sur laquelle la fonctionnalité/la tâche est développée. Une branche par feature

  > Exemple: feature/A1

- `bug/<numéro_tâche>`: branche sur laquelle on résoud un bug découvert.

- Lorsqu’une tâche (issue) est implémenté, il faudrait faire un pull request vers `develop` afin que l’équipe puisse faire de la revue de code et ajouter la documentation avant de faire le merge dans master.

- Ce serait bien de faire des tests unitaires si possible (à en discuter)

- N’oublions pas de faire des commits en Français ou en Anglais (à discuter)

- Voici une idée du format des commits `<type>(<numéro_tâche>): <description_du_commit>` où `type` est:

  - `docs`: pour ajouter de la documentation ou modifier le rapport
  - `feat` : pour ajouter des nouvelles fonctionnalité
  - `refact:` pour du refactoring
  - `fix`: au cas où on veut résoudre un bug
  - `ci`: tout ce qui attrait à la configuration des pipelines github

  - Exemple `feat(A1): ajout du script de la base de données`

REMARQUE : Ceci n’est pas la norme définitive. Elle est sujette à modification. N’oubliez pas que le but premier est de faciliter la collaboration entre nous et non de créer un régime totalitaire.
