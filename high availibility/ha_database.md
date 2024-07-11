HAUTE DISPONIBILITE DE BASE DE DONNE

Pour implémenter une haute disponibilité pour votre base de données, vous pouvez utiliser différentes solutions en fonction de votre système de gestion de bases de données (SGBD) et de vos besoins spécifiques. Voici une vue d'ensemble des méthodes couramment utilisées pour MySQL/MariaDB et PostgreSQL.

MySQL/MariaDB
Option 1 : Réplication Master-Slave
La réplication Master-Slave est une méthode courante pour assurer la haute disponibilité et la tolérance aux pannes.

Option 1 : Réplication Master-Slave
La réplication Master-Slave est une méthode courante pour assurer la haute disponibilité et la tolérance aux pannes.

Configuration de Haute Disponibilité MySQL/MariaDB avec Réplication Master-Slave
--------------------------------------------------------------------------------
Nous allons configurer une topologie de réplication Master-Slave avec MySQL/MariaDB sur deux serveurs :

Master : 192.168.15.77
Slave : 192.168.15.76

Étape 1 : Configuration du Serveur Master (192.168.15.77)
----------------------------------------------------------
Modifier le fichier de configuration MySQL/MariaDB :

installer mysql-server
# sudo apt update -y && apt install -y mysql-server

Éditez le fichier /etc/mysql/my.cnf ou /etc/mysql/mariadb.conf.d/50-server.cnf et ajoutez/modifiez les lignes suivantes :
# nano /etc/mysql/my.cnf

ajoutez/modifiez les lignes suivantes :

# [mysqld]
# server-id = 1
# log_bin = /var/log/mysql/mysql-bin.log
# bind-address = 0.0.0.0
# max_allowed_packet = 64M

puis redemarer le service mysql
# sudo systemctl restart mysql

Autorisez le trafic sur le port 3306 :
# sudo ufw allow 3306/tcp

Créer un utilisateur pour la réplication :
Connectez-vous à MySQL/MariaDB en tant qu'utilisateur root et exécutez les commandes suivantes : 
# mysql -u root -p
CREATE USER 'replica'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'replica'@'%';
FLUSH PRIVILEGES;

Obtenir l'état du Master :
Toujours dans MySQL/MariaDB, exécutez la commande suivante et notez les valeurs de File et Position :
mysql> SHOW MASTER STATUS;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |      753 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)


Étape 2 : Configuration du Serveur Slave (192.168.15.76)
-------------------------------------------------------

Modifier le fichier de configuration MySQL/MariaDB :
Éditez le fichier /etc/mysql/my.cnf ou /etc/mysql/mariadb.conf.d/50-server.cnf et ajoutez/modifiez les lignes suivantes :
# [mysqld]
# server-id = 2
# max_allowed_packet = 64M

Redémarrer le service MySQL/MariaDB :
# sudo systemctl restart mysql

Initialiser la réplication sur le Slave :

Connectez-vous à MySQL/MariaDB en tant qu'utilisateur root sur le Slave et exécutez les commandes suivantes en remplaçant les valeurs MASTER_LOG_FILE et MASTER_LOG_POS par celles obtenues à partir du Master :

CHANGE MASTER TO
    MASTER_HOST='192.168.15.77',
    MASTER_USER='replica',
    MASTER_PASSWORD='password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=753;
START SLAVE;

Vérifier la réplication :
Exécutez la commande suivante pour vérifier l'état de la réplication :
mysql> SHOW SLAVE STATUS\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 192.168.15.73
                  Master_User: replica
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000004
          Read_Master_Log_Pos: 1818
               Relay_Log_File: ubuntuserver16-relay-bin.000002
                Relay_Log_Pos: 986
        Relay_Master_Log_File: mysql-bin.000004
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 1818
              Relay_Log_Space: 1202
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 1
                  Master_UUID: c3f9f797-3ead-11ef-986d-0800278b5601
             Master_Info_File: /var/lib/mysql/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
1 row in set (0.00 sec)


ERROR:
No query specified


Test de la Réplication
Sur le Master (192.168.15.77) :

Créez une base de données et une table, puis insérez des données :
CREATE DATABASE test_db;
USE test_db;
CREATE TABLE test_table (id INT PRIMARY KEY, data VARCHAR(100));
INSERT INTO test_table (id, data) VALUES (1, 'Hello, replication!');

Sur le Slave (192.168.15.76) :
Vérifiez que la base de données, la table et les données ont été répliquées :

STOP SLAVE;
RESET SLAVE;

ca marche!


Pour rendre le site dynamique en utilisant PHP et MySQL, vous devez effectuer plusieurs modifications et ajouts. Voici les étapes détaillées pour transformer le site statique en un site dynamique :

1. Configurer le Serveur Web avec PHP et MySQL
Installation de PHP et MySQL
Sur vos serveurs backend, installez PHP et MySQL :

bash
Copier le code
sudo apt update
sudo apt install php libapache2-mod-php php-mysql mysql-server
Configuration de la Base de Données
Connectez-vous à MySQL et configurez la base de données :

bash
Copier le code
sudo mysql -u root -p
Créez une base de données et un utilisateur :

sql
Copier le code
CREATE DATABASE projet_clement;
CREATE USER 'user_clement'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON projet_clement.* TO 'user_clement'@'localhost';
FLUSH PRIVILEGES;
EXIT;
Créez une table pour stocker les informations dynamiques :

sql
Copier le code
USE projet_clement;
CREATE TABLE sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL
);
2. Modifier les Fichiers HTML pour PHP
Renommez votre fichier index.html en index.php et modifiez-le pour inclure du PHP afin de charger les données dynamiquement.

php
Copier le code
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
3. Insérer des Données dans la Base de Données
Ajoutez du contenu dans votre base de données pour tester :

sql
Copier le code
INSERT INTO sections (section_name, content) VALUES
('Haute Disponibilité', 'La haute disponibilité est essentielle pour garantir que les services restent disponibles en cas de panne. Nous utilisons des techniques de redondance et de basculement pour assurer une disponibilité continue.'),
('Web', 'Les applications web doivent être robustes et réactives. Nous implémentons des architectures évolutives et résilientes pour assurer une performance optimale et une disponibilité continue.'),
('Base de Données', 'Les bases de données sont le cœur de nombreuses applications. Nous utilisons des stratégies de réplication et de sauvegarde pour assurer la continuité des données et leur disponibilité.'),
('LACP Cisco', 'Le protocole LACP (Link Aggregation Control Protocol) permet d\'agréger plusieurs liaisons Ethernet en une seule, offrant une bande passante accrue et une redondance en cas de défaillance d\'un lien.'),
('Dual WAN', 'La configuration Dual WAN permet d\'utiliser deux connexions Internet simultanément, offrant une redondance et une répartition de la charge pour une meilleure performance réseau.');
4. Synchronisation des Serveurs Backend
Utilisez rsync pour synchroniser les fichiers PHP et les configurations sur les serveurs backend :

Créez un script rsync sur chaque serveur pour synchroniser les fichiers depuis le serveur principal :

bash
Copier le code
#!/bin/bash
rsync -avz /var/www/site-static/ 192.168.1.76:/var/www/site-static/
rsync -avz /var/www/site-static/ 192.168.1.78:/var/www/site-static/
Rendre le script exécutable et ajouter une tâche cron pour exécuter le script régulièrement :

bash
Copier le code
chmod +x /usr/local/bin/sync_files.sh
crontab -e
Ajoutez la ligne suivante dans cron pour exécuter le script toutes les 5 minutes :

bash
Copier le code
*/5 * * * * /usr/local/bin/sync_files.sh
5. Tests et Vérifications
Accédez à votre site web via le navigateur pour vérifier que les données dynamiques s'affichent correctement.
Simulez des pannes de serveurs pour tester la haute disponibilité et la redondance.
Ces étapes vous permettront de transformer votre site statique en un site dynamique avec une haute disponibilité en utilisant PHP et MySQL.


