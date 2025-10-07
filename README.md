# 💻 System Monitor Dashboard (Flask + Tkinter + JS)

Une application **Full Stack de monitoring système**, moderne et interactive — développée avec **Flask (Python)**, **Chart.js**, et **Tkinter**.  
Elle permet de **visualiser en temps réel** les ressources de ton ordinateur (CPU, RAM, disque), de **basculer entre thème clair/sombre**, et même de **surveiller d’autres machines sur le réseau** 🌐.

---

## 🚀 Fonctionnalités principales

### 🎛️ Interface Web dynamique
- Visualisation **en temps réel** des métriques système (CPU, RAM, disque).  
- **Barres de progression** animées et **graphiques Chart.js** actualisés toutes les 3 secondes.  
- **Icônes dynamiques** pour chaque catégorie (CPU, RAM, Disque).  
- Interface **responsive** et agréable (HTML + CSS + JS).

### 🌗 Mode clair / sombre
- Basculer entre les deux thèmes via un bouton.
- **Préférence enregistrée** dans `localStorage` (le mode choisi persiste).

### 🔐 Système de login sécurisé
- Authentification simple via `/login`.  
- Gestion des **sessions Flask** pour protéger les routes sensibles.  
- Données utilisateurs stockées dans `users.json`.  
- Redirection automatique vers `/login` si l’utilisateur n’est pas connecté.

### ⚙️ Page “Settings”
- L’utilisateur peut choisir les **informations à afficher** (CPU, RAM, disque, réseau).  
- Préférences sauvegardées côté client.

### 🖥️ Monitoring distant
- Entrer une **adresse IP** distante pour interroger un autre système.  
- Si la connexion échoue, retour automatique aux données locales.  
- Rafraîchissement automatique toutes les 3 secondes.

### 🪟 Intégration Tkinter
- Une petite fenêtre Tkinter permet d’**ouvrir la version web** du dashboard.  
- Peut servir de mini-lanceur desktop de l’application Flask.

---

## 🧩 Structure du projet

diagnostic-systeme/
│
├── app.py # Point d’entrée Flask (routes, API, sessions)
├── users.json # Comptes utilisateurs
├── templates/
│ ├── login.html # Page de connexion
│ ├── dashboard.html # Interface principale
│ └── settings.html # Page des préférences
│
├── static/
│ ├── css/
│ │ └── style.css # Styles principaux + dark mode
│ ├── js/
│ │ └── dashboard.js # Logique du dashboard, API, mode dark/light
│ └── icons/ # Icônes CPU, RAM, Disk, etc.
│
├── tkinter_launcher.py # Lanceur Tkinter pour l’interface web
├── requirements.txt # Dépendances Python
└── README.md # (ce fichier)


---

## 🧠 Technologies utilisées

| Type              | Outils / Frameworks         |
|------------------|-----------------------------|
| Backend          | Flask (Python)              |
| Frontend         | HTML, CSS, JavaScript       |
| Graphiques       | Chart.js                    |
| UI desktop       | Tkinter                     |
| Monitoring        | psutil (CPU, RAM, disque)   |
| Authentification | Flask-Session               |
| Stockage local   | JSON                        |

---

## ⚙️ Installation & exécution

### 1️⃣ Installer les dépendances
Assure-toi d’avoir Python 3.10+ installé, puis exécute :

```bash
pip install -r requirements.txt

Lancer l’application Flask
python app.py
L’application sera accessible sur http://127.0.0.1:5000.
(Optionnel) Lancer la version Tkinter
python app_tkinter.py
Cette fenêtre propose un bouton pour ouvrir la version web.
Utilisation
Connecte-toi avec ton identifiant et mot de passe (users.json).
Visualise les performances de ton système local.
Entre une adresse IP distante pour surveiller une autre machine.
Modifie les préférences d’affichage dans la page Settings.
Bascule le thème clair/sombre à tout moment.

Développé par Ruth Kegmo — projet démonstratif Full Stack Python (Flask + Tkinter + JS).