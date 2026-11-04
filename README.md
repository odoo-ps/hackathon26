# 🧀 Trivi'Hackathon 2026

[🇬🇧 English](#-english) · [🇫🇷 Français](#-français)

---

## 🇬🇧 English

An Odoo hackathon in the form of a Trivial Pursuit: 6 non-profit organisations, 6 challenges, 6 wedges to collect.

| Module | Wedge | Organisation | Topic |
|---|---|---|---|
| `trivia_hackathon` | | Trivi'Hackathon | Game engine: board, checkers, flags |
| `trivia_food_bank` | 🔵 | Les Restos du Quartier | Functional: contacts, invoicing, CRM, email marketing |
| `trivia_reuse_center` | 🟢 | La Ressourcerie | Functional: inventory, traceability, pricelists, point of sale |
| `trivia_garden` | 🟡 | Gaart fir Jiddereen | Python: models, inheritance, computed fields, constraints, views |
| `trivia_animal_shelter` | 🟣 | Refuge Les 4 Pattes | Website: controllers, QWeb, Bootstrap, SCSS, PDF report |
| `trivia_charity_run` | 🟠 | La Course du Cœur | SQL: SQL views, window functions, performance, injection |
| `trivia_festival` | 🩷 | Festival Solidaire | JavaScript: OWL components, client action, services |

### How you work

- Your team has its **own branch** of this repository. Every push to it builds the team's **Odoo.sh development branch**, with a brand new database.
- To write and test your code before pushing, run Odoo **on your computer** with Docker (see below). The local database contains exactly the same hackathon data as Odoo.sh, because all the data are created by the modules.
- Locally, Odoo is the **Community** edition. It is enough for the 4 development challenges. The 2 functional challenges are played on Odoo.sh (Enterprise).
- A new Odoo.sh build means a new database: **keep the flags** of the challenges you solved, so that you can submit them again on the new database to get your wedges back.

### 1. Install Docker

You need about 4 GB of RAM for Docker and 5 GB of free disk space.

- **Windows**: [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) with the **WSL 2** backend. Clone the repository **inside WSL** (for example in your Ubuntu home folder), not in `C:\`: it is much faster, and the `make` shortcuts work there (`sudo apt install make`).
- **macOS**: [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/), or [Colima](https://github.com/abiosoft/colima): `brew install colima docker docker-compose`, then `colima start --cpu 4 --memory 8`.
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/) with the `docker compose` plugin. Add yourself to the `docker` group, then log out and back in.

Check: `docker compose version` must print version 2 or higher.

### 2. Get your team branch

```sh
git clone -b <your-team-branch> git@github.com:odoo-ps/hackathon-2026.git
cd hackathon-2026
```

### 3. Run Odoo

The commands are the same in every terminal (PowerShell, bash, zsh). On macOS, Linux and WSL, the `make` shortcuts do the same in one word.

| What | Commands | Shortcut |
|---|---|---|
| Create the database and install the modules (first time) | `docker compose run --rm odoo odoo -d trivia -i trivia_hackathon,trivia_food_bank,trivia_reuse_center,trivia_garden,trivia_animal_shelter,trivia_charity_run,trivia_festival --stop-after-init`<br>`docker compose up -d` | `make init` |
| Update the modules after a change | `docker compose stop odoo`<br>`docker compose run --rm odoo odoo -d trivia -u trivia_hackathon,trivia_food_bank,trivia_reuse_center,trivia_garden,trivia_animal_shelter,trivia_charity_run,trivia_festival --stop-after-init`<br>`docker compose up -d` | `make update` |
| Start / stop Odoo | `docker compose up -d` / `docker compose down` | `make up` / `make down` |
| Follow the logs (your errors are there!) | `docker compose logs -f odoo` | `make logs` |
| Odoo shell | `docker compose exec odoo odoo shell -d trivia` | `make shell` |
| PostgreSQL console | `docker compose exec db psql -U odoo trivia` | `make psql` |
| Start over: deletes the local database! | `docker compose down -v` | `make reset` |

Then open <http://localhost:8069> and log in with `admin` / `admin`.

### Good to know

- Changed an **existing view**? Reloading the page is enough: views are read from the XML files.
- Changed **Python code**, added a **field**, a **model**, a **file** or a **record**? Update the modules (`make update`, all of them at once), and don't forget to declare the new files in `__manifest__.py`.
- Port 8069 already used on your computer? Create a `.env` file next to `docker-compose.yml` containing `ODOO_PORT=8070`, then use <http://localhost:8070>.

---

## 🇫🇷 Français

Un hackathon Odoo façon Trivial Pursuit : 6 ASBL, 6 challenges, 6 parts de camembert à collectionner.

| Module | Part | ASBL | Thème |
|---|---|---|---|
| `trivia_hackathon` | | Trivi'Hackathon | Moteur de jeu : plateau, checkers, flags |
| `trivia_food_bank` | 🔵 | Les Restos du Quartier | Fonctionnel : contacts, facturation, CRM, marketing par email |
| `trivia_reuse_center` | 🟢 | La Ressourcerie | Fonctionnel : inventaire, traçabilité, listes de prix, point de vente |
| `trivia_garden` | 🟡 | Gaart fir Jiddereen | Python : modèles, héritage, champs calculés, contraintes, vues |
| `trivia_animal_shelter` | 🟣 | Refuge Les 4 Pattes | Website : contrôleurs, QWeb, Bootstrap, SCSS, rapport PDF |
| `trivia_charity_run` | 🟠 | La Course du Cœur | SQL : vues SQL, fonctions de fenêtre, performance, injection |
| `trivia_festival` | 🩷 | Festival Solidaire | JavaScript : composants OWL, client action, services |

### Organisation du travail

- Votre équipe a **sa propre branche** de ce dépôt. Chaque push dessus construit la **branche de développement Odoo.sh** de l'équipe, avec une base de données toute neuve.
- Pour écrire et tester votre code avant de pousser, lancez Odoo **sur votre ordinateur** avec Docker (voir ci-dessous). La base locale contient exactement les mêmes données de hackathon qu'Odoo.sh, car toutes les données sont créées par les modules.
- En local, Odoo est en édition **Community**. Cela suffit pour les 4 challenges de développement. Les 2 challenges fonctionnels se jouent sur Odoo.sh (Enterprise).
- Un nouveau build Odoo.sh signifie une nouvelle base : **gardez les flags** des challenges résolus, pour les soumettre à nouveau sur la nouvelle base et récupérer vos parts.

### 1. Installer Docker

Il faut environ 4 Go de RAM pour Docker et 5 Go d'espace disque libre.

- **Windows** : [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) avec le moteur **WSL 2**. Clonez le dépôt **dans WSL** (par exemple dans votre dossier personnel Ubuntu), pas dans `C:\` : c'est beaucoup plus rapide, et les raccourcis `make` y fonctionnent (`sudo apt install make`).
- **macOS** : [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/), ou [Colima](https://github.com/abiosoft/colima) : `brew install colima docker docker-compose`, puis `colima start --cpu 4 --memory 8`.
- **Linux** : [Docker Engine](https://docs.docker.com/engine/install/) avec le plugin `docker compose`. Ajoutez-vous au groupe `docker`, puis déconnectez-vous et reconnectez-vous.

Vérification : `docker compose version` doit afficher la version 2 ou plus.

### 2. Récupérer la branche de votre équipe

```sh
git clone -b <branche-de-votre-equipe> git@github.com:odoo-ps/hackathon-2026.git
cd hackathon-2026
```

### 3. Lancer Odoo

Les commandes sont les mêmes dans tous les terminaux (PowerShell, bash, zsh). Sous macOS, Linux et WSL, les raccourcis `make` font la même chose en un mot.

| Quoi | Commandes | Raccourci |
|---|---|---|
| Créer la base et installer les modules (première fois) | `docker compose run --rm odoo odoo -d trivia -i trivia_hackathon,trivia_food_bank,trivia_reuse_center,trivia_garden,trivia_animal_shelter,trivia_charity_run,trivia_festival --stop-after-init`<br>`docker compose up -d` | `make init` |
| Mettre à jour les modules après une modification | `docker compose stop odoo`<br>`docker compose run --rm odoo odoo -d trivia -u trivia_hackathon,trivia_food_bank,trivia_reuse_center,trivia_garden,trivia_animal_shelter,trivia_charity_run,trivia_festival --stop-after-init`<br>`docker compose up -d` | `make update` |
| Démarrer / arrêter Odoo | `docker compose up -d` / `docker compose down` | `make up` / `make down` |
| Suivre les logs (vos erreurs sont là !) | `docker compose logs -f odoo` | `make logs` |
| Shell Odoo | `docker compose exec odoo odoo shell -d trivia` | `make shell` |
| Console PostgreSQL | `docker compose exec db psql -U odoo trivia` | `make psql` |
| Repartir de zéro : supprime la base locale ! | `docker compose down -v` | `make reset` |

Ouvrez ensuite <http://localhost:8069> et connectez-vous avec `admin` / `admin`.

### Bon à savoir

- Vous avez modifié une **vue existante** ? Recharger la page suffit : les vues sont lues depuis les fichiers XML.
- Vous avez modifié du **code Python**, ajouté un **champ**, un **modèle**, un **fichier** ou un **enregistrement** ? Mettez les modules à jour (`make update`, tous en une fois), sans oublier de déclarer les nouveaux fichiers dans `__manifest__.py`.
- Le port 8069 est déjà utilisé sur votre ordinateur ? Créez un fichier `.env` à côté de `docker-compose.yml` contenant `ODOO_PORT=8070`, puis utilisez <http://localhost:8070>.
