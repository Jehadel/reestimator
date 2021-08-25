# Data analysis
- Document here the project: reestimator
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for reestimator in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/reestimator`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "reestimator"
git remote add origin git@github.com:{group}/reestimator.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
reestimator-run
```

# Install

Go to `https://github.com/{group}/reestimator` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/reestimator.git
cd reestimator
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
reestimator-run
```




# Description colonnes

## Colonnes conservées

**id_mutation**(0)
id keys (str)

**date_mutation**(1)
date de la mutation (à convertir en datetime)

**nature_mutation**(3)
nature de la mutation : vente, partage, adjucation (str)
_conserver seulement les lignes 'ventes', envoyer les autres dans la table 'non-traité'

**valeur_fonciere**(5)
notre target ! (à convertir en int32)

**adresse_numero**(6)
numéro dans la rue (adresse) (à convertir en int8)

**adresse_suffixe**(7)
suffixe numéro d'adresse : A, B, bis, ter... (str)

**adresse_nom_voie**(8)
nom de la rue (str)

**code_commune**(11)
code de la commune sur le plan cadastral

**code_departement**(12)
(str à cause de la Corse)

**id_parcelle**(15)
agrége code commune / code secteur cadastral / numéro parcelle
_extraire le code secteur cadastral dans autre colonne_

**code_type_local**(29)
encodage du type de local. seul 1 (maison), 2 (appartement), et 3 (dépendance, à transformer) nous intéresse (à convertir en int8)
_supprimer ligne pour 3 (dépendance) et ajouter une colonne binaire "bien avec dépendance" -> influence sur le prix ?_

**surface_reelle_bati**(31)
un de nos rares prédicteurs (convertir en int32)

**nombre_pieces_principales**(32)
un de nos rares prédicteurs (convertir en int32)

**surface_terrain**(37)
un de nos rares prédicteurs(convertir en int32)

**longitude**(38)
**latitude**(39)
coordonnées pour la géolocalisation (float 64)
_il y a des communes non vectorisées où la géolocalisation n'est pas dispo_

## Colonnes supprimées

**adresse_code_voie**(9)
code FANTOR pour l'administration

**ancien_code_commune**(13)

**ancien_nom_commune**(14)
utile seulement si on fouille dans le cadastre passé

**ancien_id_parcelle**(16)
utile seulement si on fouille dans le cadastre passé

**numero_volume**(17)
utile seulement si on fouille dans le cadastre passé

**type_local**(30)
type du local, double emploi avec code_type_local (conservée)

**code_nature_culture**(33)
**nature_culture**(34)
**code_nature_culture_speciale**(35)
**nature_culture_speciale**(36)
pas de corrélation avec valeur foncière

## Colonnes qui posent question

**numero_disposition**(4)
Numéro d'ordre si ventes simultanées.
À conserver à priori pour différencier si ventes avec même id, à vérifier

**code_postal**(10)
code postal, différent du code commune, mais utilisé pour l'adressage

**lot1_numero**(18)
**lot1_surface_carrez**(19)
**lot2_numero**(20)
**lot2_surface_carrez**(21)
**lot3_numero**(22)
**lot3_surface_carrez**(23)
**lot4_numero**(24)
**lot4_surface_carrez**(25)
**lot5_numero**(26)
**lot5_surface_carrez** (27)
a priori on vire, mais vérifier si congruence avec surface totale

**nombre_lots**(28)
vérifier si incidence sur prix final, a priori on vire

# Description fonctions

## Preprocessing

### get_data.py

Methods (class dloading) to get datas (DataFrame) from the database Housing_France

class dloading:
  load_data_chunk(table_name,chunksize)
  _Loads a dataframe by chunks of size chunksize from table database_

  get_random_rows(table_name, numrows)
  _Loads a dataframe of size numrows from random lines of the table database_

  get_all_rows(table_name)
  _Loads a dataframe from an entire database table_

  get_num_rows(table_name, rownums)
  _Loads a dataframe of size rownums  from database table_

  show_tables()
  _show all the tables in the database Housing_France_

  data_to_sql(df, tablename, if_exists)
  _Export Data to Sql, if exists takes one of the two strings :  ['replace','append']_

### exploration.py

### preprocessing.py
