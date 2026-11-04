# 🧀 Trivi'Hackathon 2026 : consignes du Dry Run

Six ASBL ont besoin de votre aide. Chaque challenge rapporte une part de camembert. Vous avez **2 heures** : ce document vous oriente pour chaque problème, mais **le code, c'est vous qui l'écrivez**.

## 0. Démarrer

**Prérequis** :
- Git, avec un accès GitHub au dépôt `odoo-ps/hackathon-2026` ;
- Docker, avec `docker compose` version 2 ou plus ;
- sous Windows : Docker Desktop avec WSL 2, et le dépôt cloné **dans** WSL.

```sh
git clone -b <branche-communiquée> git@github.com:odoo-ps/hackathon-2026.git
cd hackathon-2026
make init        # la première fois : crée la base et installe les modules
```
Sans `make`, utilisez les commandes équivalentes du `README.md`.

Si le `git clone` répond « Permission denied (publickey) », clonez en HTTPS : `git clone -b <branche-communiquée> https://github.com/odoo-ps/hackathon-2026.git`.

Ouvrez <http://localhost:8069> et connectez-vous avec `admin` / `admin`.

**Les commandes utiles** :

| Quoi | Commande |
|---|---|
| Mettre à jour les modules après une modification (tous en une fois, en quelques secondes) | `make update` |
| Lire les logs (vos erreurs y sont !) | `make logs` |
| Console PostgreSQL | `make psql` |
| Repartir de zéro (efface la base) | `make reset && make init` |

**La boucle de travail** :
1. lire l'énoncé de la carte, dans **Trivi'Hackathon › Plateau de jeu** ;
2. coder ;
3. lancer `make update` ;
4. cliquer sur **Vérifier** sur la carte : le rapport liste chaque étape (✅ ou ❌, avec la raison).


---

## 1. 🔵 Les Restos du Quartier : fonctionnel, sans code

Tout se fait dans l'interface. Les noms sont comparés sans tenir compte des accents ni des majuscules.

### 1.1 Les donateurs
- **À faire** :
  - importer `donors.csv` (lien dans l'énoncé) depuis **Contacts**, avec l'import de fichier ;
  - étiqueter : `Donateur` pour les 10 contacts, `Bénévole` pour Élise Bernard et Marc Kieffer, `Entreprise` pour Boulangerie Kremer.
- **Attendu** : les 10 donateurs importés, Boulangerie Kremer en société avec ses 2 contacts, et les étiquettes posées.
- ⚠️ En Odoo 20, « Société » se déduit d'un numéro de TVA : le CSV en contient un. Les colonnes sont reconnues automatiquement.

### 1.2 Les produits
- **À faire** : dans **Facturation**, créer `Don libre` et `Cotisation membre` (prix de vente 25), de type *Service*, dans une catégorie de produits `Dons`.
- **Attendu** : les 2 services dans la catégorie Dons, et la Cotisation à 25.

### 1.3 Les mécènes
- **À faire** : dans **CRM**, créer l'équipe commerciale `Mécénat`, son pipeline avec les étapes `Identifié`, `Contacté`, `Dossier envoyé` et `Signé`, puis 3 opportunités. Marquer l'une d'elles comme gagnée.
- **Attendu** : les 4 étapes, 3 opportunités de l'équipe, dont une gagnée.

### 1.4 Merci !
- **À faire** :
  - créer une liste de diffusion `Donateurs` avec les 10 donateurs (depuis la liste des contacts : **Actions › Add to Mailing List**, libellé non traduit) ;
  - envoyer un mailing à cette liste depuis **Marketing par e-mail**.
- **Attendu** : la liste avec les 10 donateurs, et un mailing qui n'est plus en brouillon.
- ⚠️ La base est neutralisée : les e-mails ne partent pas vraiment, et c'est normal.

### 1.5 Les dons
- **À faire** :
  - confirmer 3 factures client à des donateurs, avec Don libre ou Cotisation membre ;
  - analyser les factures par donateur et enregistrer cette analyse dans vos favoris.
- **Attendu** : 3 factures confirmées, et un favori de l'analyse des factures regroupé par partenaire.
- ⚠️ Le menu est **Facturation › Analyse › Gestion › Analyse des factures**. Regroupez par **Partenaire**, puis, dans le menu de la barre de recherche : **Favoris › Save search** (non traduit).

### ⭐ Bonus
- Un champ « N° d'entreprise » sur les contacts. En local : mode développeur, puis **Paramètres › Technique › Champs**.
- Une taxe à 0 % sur les 2 produits.
- Une activité planifiée sur une opportunité.
- Le mailing réellement traité : lancer à la main l'action planifiée *Mail Marketing: Process queue*.
- Une facture payée.

---

## 2. 🟢 La Ressourcerie : fonctionnel, sans code

### 2.1 Les articles
- **À faire** : dans **Inventaire**, créer 8 produits dont l'inventaire est suivi, avec un prix de vente, répartis dans 3 catégories `Vêtements`, `Meubles` et `Électro`. Les rendre disponibles au Point de Vente.
- **Attendu** : 8 produits stockables, avec un prix, et les 3 catégories utilisées.

### 2.2 Le tarif social
- **À faire** :
  - activer les listes de prix ;
  - créer la liste `Tarif social`, qui donne 50 % de remise ;
  - la rendre disponible dans la boutique.
- **Attendu** : Tarif social divise par 2 le prix d'au moins un article.
- ⚠️ En Odoo 20, les listes de prix s'activent dans **Point de Vente › Configuration › Paramètres**, case **Listes de prix flexibles**. Ces réglages portent sur une boutique : créez-la d'abord, avec la tuile **Vente au détail** de l'app Point de Vente. Ajoutez ensuite Tarif social dans **Disponible**, puis enregistrez.

### 2.3 Un don
- **À faire** : enregistrer et valider la réception de quelques objets donnés par le contact `Donateur anonyme`.
- **Attendu** : une réception validée de ce contact.

### 2.4 La caisse
- **À faire** : ouvrir une session de caisse et faire 3 ventes, dont une au Tarif social.
- **Attendu** : 3 ventes payées, dont une au Tarif social.
- ⚠️ En caisse, on choisit la liste de prix dans **Actions › Liste de prix**. Si le tarif a été ajouté pendant que la session était ouverte, rechargez la page de la caisse.

### 2.5 La fin de la journée
- **À faire** : fermer la session de caisse.
- **Attendu** : vos 3 ventes sont dans des sessions fermées.

### 2.6 La commode perdue
- **À faire** :
  - retrouver la commode Art déco rapportée par Josiane Feller : les transferts et la traçabilité des numéros de série sont vos amis ;
  - créer un emplacement interne `Atelier réparation` ;
  - y déplacer **cette** commode.
- **Attendu** : la bonne commode (le bon numéro de série) dans l'Atelier réparation.

### ⭐ Bonus
- Une description de vente sur les 8 articles.
- Le Tarif social limité à une catégorie de produits.
- Un client sur un ticket.
- L'analyse des ventes par catégorie de produits enregistrée en favori : **Point de Vente › Analyse › Commandes**.

---

## 3. 🟡 Gaart fir Jiddereen (`trivia_garden`) : Python

Les TODO du code sont numérotés comme les problèmes. Après chaque problème : `make update`, puis **Vérifier**.

### 3.1 Les cotisations (TODO 1)
- **Fichier** : `models/garden_membership_fee.py`.
- **À faire** : créer la classe `GardenMembershipFee`, modèle `garden.membership.fee`, avec :
  - les champs `partner_id` (lien vers un contact, requis), `year` (entier, requis), `amount`, `state` (`draft` ou `paid`, requis, `draft` par défaut) et `payment_date` ;
  - une contrainte d'unicité `_partner_year_uniq` sur le couple membre et année ;
  - la méthode `action_mark_paid()`, qui passe les cotisations à payées avec la date du jour.
- ⚠️ En Odoo 20, une contrainte SQL s'écrit avec `models.Constraint`. `_sql_constraints` n'existe plus.
- Facultatif : un `_compute_display_name`, pour afficher « 2026 - Marie Weber » au lieu de `garden.membership.fee,12`.

### 3.2 Les droits d'accès (TODO 2)
- **Fichier** : `security/ir.access.csv`.
- **À faire** : ajouter une ligne qui donne aux utilisateurs internes (`base.group_user`) tous les droits sur les cotisations.
- ⚠️ Odoo 20 remplace `ir.model.access.csv` par `ir.access.csv`, avec d'autres colonnes : inspirez-vous des lignes existantes. Sans cette ligne, le modèle est invisible.

### 3.3 Les vues des cotisations (TODO 3)
- **Fichiers** : `views/garden_membership_fee_views.xml` et `views/menus.xml`.
- **À faire** :
  - une vue liste et une vue formulaire ;
  - dans le `<header>` du formulaire : le champ `state` en `statusbar`, et un bouton qui appelle `action_mark_paid`, visible seulement sur les cotisations en brouillon ;
  - une action, et un menu *Membership Fees* sous le menu du jardin.
- ⚠️ En Odoo 20 : `<list>` et non `<tree>`, et `invisible="…"` au lieu de `attrs`.

### 3.4 Les membres (TODO 4)
- **Fichier** : `models/res_partner.py`.
- **À faire** : sur les contacts (héritage de `res.partner`), ajouter :
  - `membership_type` (individual, family ou patron) ;
  - `member_since` ;
  - `fee_ids`, le lien inverse des cotisations ;
  - `last_paid_year` : la dernière année payée, 0 sinon. C'est un champ **calculé et stocké**, avec la méthode `_compute_last_paid_year`.
- ⚠️ Le checker paie, change l'année et supprime des cotisations : vos dépendances (`@api.depends`) doivent couvrir tous ces changements.

### 3.5 La fiche contact (TODO 5)
- **Fichier** : `views/res_partner_views.xml`.
- **À faire** :
  - hériter du formulaire `base.view_partner_form` pour ajouter un onglet *Membership*, avec les 4 nouveaux champs (passez par un `xpath`) ;
  - hériter de la recherche `base.view_res_partner_filter` pour ajouter un filtre *Not up to date* : les membres dont la dernière année payée est antérieure à l'année en cours, **sans année écrite en dur**.

### 3.6 Les parcelles (TODO 6)
- **Fichier** : `models/garden_plot.py`.
- **À faire** : une méthode `_check_tenant` avec `@api.constrains`, qui refuse (`ValidationError`) deux cas :
  - un locataire qui n'a pas payé l'année en cours ;
  - un membre qui loue déjà une parcelle.

### 3.7 Les données (TODO 7)
- **Fichier** : `__manifest__.py`.
- **À faire** : charger `data/garden_membership_fee_data.xml`, après les vues.

### ⭐ Bonus
- **Bouton intelligent *Fees*** sur la fiche contact, avec le nombre de cotisations : un champ calculé, une méthode qui renvoie une action, et un bouton dans le `div` `button_box`.
- **Kanban des parcelles** groupé par site (`default_group_by`), ouvert par l'action des parcelles.

---

## 4. 🟣 Refuge Les 4 Pattes (`trivia_animal_shelter`) : site web

Gardez les contrôleurs minces : le checker teste directement les méthodes des modèles.

### 4.1 Les animaux adoptables (TODO 1)
- **Fichier** : `models/shelter_animal.py`.
- **À faire** : `_get_adoptable_animals(species=None)` renvoie les animaux publiés et pas encore adoptés, triés par nom. Si `species` est donnée, seulement cette espèce.

### 4.2 La page /adopt (TODO 2)
- **Fichiers** : `controllers/main.py` et `views/website_templates.xml`.
- **À faire** :
  - une route publique `/adopt` (accessible sans connexion, page du site) qui affiche le gabarit `animal_list` avec les animaux adoptables ;
  - dans `animal_list`, une grille Bootstrap **responsive** (une, deux puis trois colonnes selon l'écran) qui appelle le gabarit `animal_card` pour chaque animal ;
  - `animal_card` : la racine imposée par le commentaire du gabarit, avec l'emoji, le nom, la race, l'âge et un lien vers `animal.website_url`.

### 4.3 La page d'un animal (TODO 3)
- **Fichiers** : les mêmes.
- **À faire** : une route `/adopt/<model("shelter.animal"):animal>` qui affiche `animal_detail`, avec l'emoji, le nom, la race, l'âge, le sexe et la description. Conseillé : une 404 si l'animal n'est pas adoptable.

### 4.4 La demande d'adoption (TODO 4)
- **Fichiers** : `models/shelter_adoption_request.py`, le gabarit `animal_detail` et le contrôleur.
- **À faire** :
  - `_create_from_website(animal, values)` crée la demande en toute sécurité :
    - elle refuse un animal non adoptable (`UserError`) ;
    - elle ne garde que les champs du formulaire (une liste blanche) ;
    - l'animal est celui de la page ;
    - elle crée en `sudo()`, car le visiteur n'a aucun droit sur les demandes ;
    - elle renvoie la demande.
  - un formulaire `post` sur la page de l'animal, vers son URL suivie de `/request`, avec les champs `name`, `email`, `phone` et `message`, **et le jeton CSRF** ;
  - la route correspondante, **POST uniquement**, qui affiche `adoption_thanks`.
- Puis **adoptez vous-même un animal** depuis une fenêtre de navigation privée : le checker attend une demande créée par un visiteur.
- ⚠️ Après l'envoi, rouvrir la page de remerciement donne « 405 Method Not Allowed ». C'est connu, et la demande est bien créée.

### 4.5 Le style et le menu (TODO 5)
- **Fichiers** : `static/src/scss/shelter.scss`, `__manifest__.py` et `views/website_templates.xml`.
- **À faire** :
  - styler les cartes (`.o_shelter_card`), par exemple avec une ombre et un léger zoom au survol ;
  - déclarer le fichier dans les assets du site (`web.assets_frontend`) ;
  - ajouter un menu *Adopt* dans le menu principal du site (un `website.menu`).

### 4.6 Le certificat d'adoption (TODO 6)
- **Fichier** : `report/adoption_certificate_report.xml`.
- **À faire** : un rapport PDF sur les demandes, imprimable depuis le menu *Imprimer* d'une demande. Il montre le nom du demandeur et l'animal ; utilisez `web.external_layout`.
- ⚠️ Odoo 20 : le champ `report_file` n'existe plus, et le mettre fait échouer l'installation.

### ⭐ Bonus
- Des boutons de filtre par espèce au-dessus de la grille (`/adopt?species=cat`).
- Un bloc « Animal of the week » dans l'éditeur du site (`t-snippet`).

---

## 5. 🟠 La Course du Cœur (`trivia_charity_run`) : SQL

Explorez les données avec `make psql`. Après chaque modification : `make update` (la vue SQL est recréée).

### 5.1 Les résultats (TODO 1)
- **Fichier** : `report/run_result_report.py`, méthode `init()`.
- **À faire** : remplacer la vue vide par la vraie vue SQL : une ligne par coureur **arrivé** (un temps au km 10), avec les colonnes décrites dans le TODO :
  - le temps en minutes entre **son** départ (km 0) et son arrivée ;
  - l'allure en minutes par km ;
  - le rang dans l'édition et dans la catégorie, les ex aequo partageant le même rang (1, 2, 2, 4).
- Indices : `EXTRACT(EPOCH FROM …)` et les fonctions de fenêtre `… OVER (PARTITION BY … ORDER BY …)`.

### 5.2 La performance (TODO 2)
- **Fichiers** : `models/run_runner.py` et `models/run_split.py`.
- **À faire** :
  - réécrire `_compute_amount_raised` pour calculer tous les coureurs en quelques requêtes, et non une par coureur (pensez à `_read_group`) ;
  - ajouter l'index manquant sur le coureur des temps de passage.
- ⚠️ En SQL brut, il faut d'abord envoyer en base les modifications de l'ORM (`flush_model`).

### 5.3 La sécurité (TODO 3)
- **Fichier** : `models/run_runner.py`.
- **À faire** : `search_by_bib_or_name()` est vulnérable à l'injection SQL, et ne trouve même pas Seán O'Brien. Passez les valeurs en **paramètres** de la requête, jamais dans le texte.

### 5.4 Le tricheur (TODO 4)
- **À faire** : dans la dernière édition, un coureur a couru les km 5 à 10 plus vite que le record du monde du 5 km (12 min 35 s).
  - Trouvez-le en SQL dans `make psql` (pensez à `LAG()`).
  - Disqualifiez-le avec le bouton de sa fiche. Lui seul, et dans la dernière édition uniquement.

### ⭐ Bonus
- Les disqualifiés exclus des résultats, avec des rangs recalculés sans eux.
- Des vues pivot et graphique des résultats, ouvertes par l'action des résultats.

---

## 6. 🩷 Festival Solidaire (`trivia_festival`) : JavaScript / OWL 3

⚠️ Odoo 20 utilise **OWL 3**, et la documentation comme l'IA montrent souvent OWL 2. Lisez l'antisèche en haut de `static/src/fill_gauge/fill_gauge.js`, et ouvrez Odoo avec `?debug=assets` pour lire les erreurs dans la console du navigateur.

### 6.1 La jauge (TODO 1)
- **Fichiers** : `static/src/fill_gauge/fill_gauge.js`, `fill_gauge.xml` et `views/event_event_views.xml`.
- **À faire** :
  - dans le composant, compléter les getters : le maximum (`seats_max` de l'enregistrement), le pourcentage et la couleur (vert sous 70 %, orange sous 90 %, rouge au-delà) ;
  - le gabarit : une barre de progression Bootstrap et le texte « pris / max (pourcentage %) » ;
  - enregistrer le widget sous le nom `festival_fill_gauge` dans le registre `fields` ;
  - l'utiliser sur le champ `seats_taken` du formulaire de l'événement.
- **Où le voir** : **Festival Solidaire › Festival**, ligne *Remplissage*. Attendu : « 120 / 150 (80 %) », en orange.

### 6.2 L'accueil (TODO 2)
- **Fichiers** : `static/src/kiosk/kiosk.js`, `kiosk.xml` et `views/menus.xml`.
- **À faire** :
  - `loadData()` et `checkIn()` appellent le serveur avec le service `orm` : les méthodes sont prêtes et décrites en haut du fichier ;
  - dans le gabarit, un badge *Present* pour les personnes arrivées, et sinon un bouton *Check in* ;
  - enregistrer le composant sous le nom `festival_kiosk` dans le registre `actions` ;
  - créer l'action client correspondante et un menu *Welcome Desk*.

### 6.3 Ouvrir les portes (TODO 3)
- **À faire** : enregistrer l'arrivée de 3 personnes depuis votre écran d'accueil.

### ⭐ Bonus
- Un compteur des personnes présentes dans le systray (les icônes en haut à droite).
- Un champ de recherche dans l'accueil. ⚠️ En OWL 3, `t-model` exige un `signal`.
