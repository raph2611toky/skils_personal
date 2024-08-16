
---

# HAUTE DISPONIBILITÉ DE BASE DE DONNÉES

## 1. Réplication Master-Slave MySQL/MariaDB

### Configuration de la Haute Disponibilité avec Réplication Master-Slave

#### Topologie
- **Master** : 192.168.15.77
- **Slave** : 192.168.15.76

### Étape 1 : Configuration du Serveur Master (192.168.15.77)

1. **Installation de MySQL/MariaDB** :
   ```bash
   sudo apt update -y && apt install -y mysql-server
   ```

2. **Modification du fichier de configuration MySQL/MariaDB** :
   Éditez `/etc/mysql/my.cnf` ou `/etc/mysql/mariadb.conf.d/50-server.cnf` et ajoutez/modifiez les lignes suivantes :
   ```ini
   [mysqld]
   server-id = 1
   log_bin = /var/log/mysql/mysql-bin.log
   bind-address = 0.0.0.0
   max_allowed_packet = 64M
   ```

3. **Redémarrage du service MySQL** :
   ```bash
   sudo systemctl restart mysql
   ```

4. **Autoriser le trafic sur le port 3306** :
   ```bash
   sudo ufw allow 3306/tcp
   ```

5. **Créer un utilisateur pour la réplication** :
   Connectez-vous à MySQL en tant que root :
   ```sql
   mysql -u root -p
   CREATE USER 'replica'@'%' IDENTIFIED BY 'password';
   GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';
   FLUSH PRIVILEGES;
   ```

6. **Obtenir l'état du Master** :
   ```sql
   SHOW MASTER STATUS;
   ```
   Notez les valeurs `File` et `Position`.

### Étape 2 : Configuration du Serveur Slave (192.168.15.76)

1. **Modification du fichier de configuration MySQL/MariaDB** :
   Éditez `/etc/mysql/my.cnf` ou `/etc/mysql/mariadb.conf.d/50-server.cnf` et ajoutez/modifiez les lignes suivantes :
   ```ini
   [mysqld]
   server-id = 2
   max_allowed_packet = 64M
   ```

2. **Redémarrage du service MySQL/MariaDB** :
   ```bash
   sudo systemctl restart mysql
   ```

3. **Initialiser la réplication sur le Slave** :
   Connectez-vous à MySQL sur le Slave :
   ```sql
   CHANGE MASTER TO
       MASTER_HOST='192.168.15.77',
       MASTER_USER='replica',
       MASTER_PASSWORD='password',
       MASTER_LOG_FILE='mysql-bin.000001',
       MASTER_LOG_POS=753;
   START SLAVE;
   ```

4. **Vérifier la réplication** :
   ```sql
   SHOW SLAVE STATUS\G;
   ```

### Test de la Réplication

1. **Sur le Master (192.168.15.77)** :
   Créez une base de données et une table, puis insérez des données :
   ```sql
   CREATE DATABASE test_db;
   USE test_db;
   CREATE TABLE test_table (id INT PRIMARY KEY, data VARCHAR(100));
   INSERT INTO test_table (id, data) VALUES (1, 'Hello, replication!');
   ```

2. **Sur le Slave (192.168.15.76)** :
   Vérifiez que la base de données, la table et les données ont été répliquées.

---

# SITE DYNAMIQUE AVEC PHP ET MySQL

## 1. Configuration du Serveur Web avec PHP et MySQL

### Installation de PHP et MySQL

```bash
sudo apt update
sudo apt install php libapache2-mod-php php-mysql mysql-server
```

### Configuration de la Base de Données

1. **Connexion à MySQL** :
   ```bash
   sudo mysql -u root -p
   ```

2. **Création d'une base de données et d'un utilisateur** :
   ```sql
   CREATE DATABASE projet_clement;
   CREATE USER 'user_clement'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON projet_clement.* TO 'user_clement'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. **Création d'une table pour stocker les informations dynamiques** :
   ```sql
   USE projet_clement;
   CREATE TABLE sections (
       id INT AUTO_INCREMENT PRIMARY KEY,
       section_name VARCHAR(255) NOT NULL,
       content TEXT NOT NULL
   );
   ```

## 2. Modification des Fichiers HTML pour PHP

Renommez votre fichier `index.html` en `index.php` et modifiez-le pour inclure du PHP.

```php
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projet de Mr Clément</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }
        header { background-color: #005f73; color: white; text-align: center; padding: 2em 0; }
        nav { background-color: #0a9396; display: flex; justify-content: center; padding: 1em 0; }
        nav a { color: white; margin: 0 15px; text-decoration: none; font-weight: bold; }
        nav a:hover { text-decoration: underline; }
        .container { padding: 2em; }
        .section { margin: 2em 0; padding: 2em; background-color: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        footer { background-color: #005f73; color: white; text-align: center; padding: 1em 0; position: fixed; width: 100%; bottom: 0; }
    </style>
</head>
<body>
    <header>
        <h1>Projet d'Administration Reseau Linux</h1>
        <p>Solutions de Haute Disponibilité et Réseaux</p>
    </header>
    <nav>
        <a href="#ha">Haute Disponibilité</a>
        <a href="#web">Web server</a>
        <a href="#database">Base de Données</a>
        <a href="#lacp">LACP Cisco</a>
        <a href="#dualwan">Dual WAN</a>
    </nav>
    <div class="container">
        <?php
        $conn = new mysqli('localhost', 'user_clement', 'password', 'projet_clement');
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        $sql = "SELECT section_name, content FROM sections";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                echo "<div class='section' id='". strtolower($row["section_name"]) ."'>";
                echo "<h2>" . $row["section_name"] . "</h2>";
                echo "<p>" . $row["content"] . "</p>";
                echo "</div>";
            }
        } else {
            echo "0 results";
        }
        $conn->close();
        ?>
    </div>
    <footer>
        <p>&copy; 2024 Projet de Mr Clément. Tous droits réservés.</p>
    </footer>
</body>
</html>
```

## 3. Insertion des Données dans la Base de Données

Ajoutez du contenu dans votre base de données pour tester :

```sql
INSERT INTO sections (section_name, content) VALUES
('Haute Disponibilité', 'La haute disponibilité est essentielle pour garantir que les services restent disponibles en cas de panne. Nous utilisons des techniques de redondance et de basculement pour assurer une disponibilité continue.'),
('Web', 'Les applications web doivent être robustes et réactives. Nous implémentons des architectures évolutives et résilientes pour assurer une performance optimale et une disponibilité continue.'),
('Base de Données', 'Les bases de données sont le cœur de nombreuses applications. Nous utilisons des stratégies de réplication et de sauvegarde pour assurer la continuité des données et leur disponibilité.'),
('LACP Cisco', 'Le protocole LACP (Link Aggregation Control Protocol) permet d\'agréger plusieurs liaisons Ethernet en une seule, offrant une bande passante accrue et une redondance en cas de défaillance d\'un lien.'),
('Dual WAN', 'La configuration Dual WAN permet d\'utiliser deux connexions Internet simultanément, offrant une redondance et une répartition de la charge pour une meilleure performance réseau.');
```

## 4. Synchronisation des Serveurs Backend


### Synchronisation Automatisée des Fichiers sur les Serveurs

Pour assurer une cohérence parfaite entre vos serveurs et garantir que les fichiers de votre site web sont toujours à jour sur tous les nœuds, vous pouvez mettre en place une synchronisation régulière des fichiers en utilisant `rsync`. Cette méthode permet de répliquer les modifications effectuées sur le serveur principal vers les serveurs secondaires.

#### 1. Création du Script de Synchronisation

Commencez par créer un script `rsync` sur votre serveur principal. Ce script va synchroniser les fichiers de votre site web vers les serveurs secondaires :

```bash
#!/bin/bash
# Synchronisation des fichiers vers le premier serveur secondaire
rsync -avz /var/www/site-static/ 192.168.1.76:/var/www/site-static/

# Synchronisation des fichiers vers le second serveur secondaire
rsync -avz /var/www/site-static/ 192.168.1.78:/var/www/site-static/
```

Ce script utilise `rsync`, un outil puissant de synchronisation qui compare les fichiers locaux avec ceux présents sur les serveurs distants et ne transfère que les différences, optimisant ainsi l'utilisation de la bande passante et les performances.

#### 2. Rendre le Script Exécutable

Pour pouvoir exécuter ce script, il faut d'abord lui donner les droits d'exécution :

```bash
chmod +x /usr/local/bin/sync_files.sh
```

En plaçant le script dans `/usr/local/bin/`, vous le rendez accessible de manière globale sur le serveur.

#### 3. Planification Automatique avec Cron

Afin d'automatiser la synchronisation, vous allez configurer une tâche cron qui exécutera le script à des intervalles réguliers. Par exemple, pour une synchronisation toutes les 5 minutes :

1. Ouvrez l'éditeur cron :
   ```bash
   crontab -e
   ```

2. Ajoutez la ligne suivante au fichier cron pour exécuter le script toutes les 5 minutes :
   ```bash
   */5 * * * * /usr/local/bin/sync_files.sh
   ```

Cette planification garantit que toutes les modifications apportées aux fichiers sur le serveur principal sont répliquées rapidement sur les serveurs secondaires, minimisant ainsi le risque de désynchronisation.

#### 4. Tests et Vérifications

Une fois la configuration terminée, il est essentiel de vérifier le bon fonctionnement du processus :

- **Vérification de l'affichage des données dynamiques** : Accédez à votre site web via le navigateur pour vous assurer que les données dynamiques sont bien synchronisées et affichées correctement sur tous les serveurs.

- **Simulation de pannes de serveurs** : Déconnectez temporairement un serveur secondaire ou le serveur principal pour vérifier que le site reste disponible grâce à la redondance des fichiers.

Ces étapes permettent non seulement de transformer un site statique en site dynamique, mais aussi d'assurer une haute disponibilité en utilisant des mécanismes de synchronisation et de réplication automatiques avec `rsync` et `cron`.

--- 

```plaintext
---

Copyright © TOKY Nandrasana
Étudiant de l'École Nationale de l'Informatique
Date : 23 juillet 2024
```