# R5C06_Project 

Nous nous sommes mis dans la peau de jeunes entrepreneurs créant leur propre boutique de sport à l’échelle nationale. Certaines régions (proches de la Bretagne) seront privilégiées car le siège social se situera à Rennes.

Sachant que les boutiques ne peuvent pas couvrir tous les sports, la question est la suivante :

> **Quels sont les sports les plus pratiqués et dans lesquels investir ?**

---

### 📋 Pré-requis

Ce qui est requis pour commencer avec le projet :
* Python 3.13

### ⚙️ Installation et Configuration

Suivez ces étapes pour installer et lancer l'analyse.

#### 1. Récupération des données
1. Téléchargez le fichier CSV des licences sportives sur [data.gouv.fr](https://www.data.gouv.fr/datasets/donnees-geocodees-issues-du-recensement-des-licences-et-clubs-aupres-des-federations-sportives-agreees-par-le-ministere-charge-des-sports/).
2. Renommez le fichier téléchargé en **`sport.csv`**.
3. Placez-le dans le dossier `data/` à la racine du projet.

#### 2. Environnement virtuel
Créez et activez votre environnement virtuel :

```bash
# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
````

#### 3\. Installation des dépendances

Installez les librairies nécessaires :

```bash
pip install -r requirements.txt
```

#### 4\. Préparation des données

Lancez les scripts de nettoyage pour générer les fichiers nécessaires à l'application :

```bash
python3 create_standardized_file.py
python3 src/clean/main.py
```

-----

### 🚀 Démarrage de l'application

Pour lancer le dashboard interactif :

```bash
python3 -m streamlit run app.py
```

*(Si cela ne fonctionne pas, essayez la méthode robuste : `python3 -m streamlit run app.py`)*

-----

### 🛠️ Versions

**V1.0**

### 👥 Auteurs

  * **Richard Terrade** *alias* [@zenpoxa](https://github.com/zenpoxa)
  * **Thibault DUBOIS** *alias* [@tbtdbs29](https://github.com/tbtdbs29)