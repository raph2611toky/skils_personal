# =========================================================================== #
#                                                                             #
#                 HAUTE DISPONIBILITE DE SERVEUR WEB                          #
#                                                                             #
# =========================================================================== #

Pour mettre en place un système de load balancing et de fail-over avec Nginx et Apache, et assurer la synchronisation des serveurs backend pour que les changements soient visibles après le redémarrage d'un serveur en panne, vous pouvez suivre les étapes décrites ci-dessous :

I. Présentation
Mettre en place une architecture web avec load balancing et fail-over permet de garantir la disponibilité et la performance des services web. Dans cette configuration, Nginx agira comme un reverse proxy pour équilibrer la charge entre plusieurs serveurs Apache et assurer la continuité du service en cas de panne de l'un des serveurs backend.

II. Pré-requis
Serveur Load Balancer Nginx (par exemple avec l'IP 192.168.1.2)
Deux serveurs backend Apache (par exemple, srv1 avec l'IP 192.168.1.3 et srv2 avec l'IP 192.168.1.4)

---------------------------------------------------------------------------
Pour un site web statique avec une haute disponibilité de service, l'architecture peut utiliser des serveurs backend pour gérer des tâches comme la distribution de contenu, la mise en cache et la réplication de fichiers. Voici un exemple détaillé de fonctionnement pour un site web statique avec Nginx en tant que reverse proxy et deux serveurs backend pour assurer la haute disponibilité :

Architecture
Serveur Nginx (Load Balancer)
IP: 192.168.1.2

Serveur Backend 1 (Serveur Web Apache)
IP: 192.168.1.3

Serveur Backend 2 (Serveur Web Apache)
IP: 192.168.1.4

TOPOLOGIE PHYSIQUE                                               |                                 TOPOLOGIE LOGIQUE

                        ----------------                                                    ----------------
                        |    ROUTER    |                                                    |    CLIENT    |
                        ----------------                                                    ----------------
                                |                                                                   |
                                |                                                                   |
                                |                                                          ---------------------
                        ----------------                                                   |   LOAD BALANCER   |
                        |    swicth    |                                                   |    192.168.1.2    |
                        ----------------                                                   ---------------------
                       /        |       \                                                       /         \
                      /         |        \                                                     /           \
                     /          |         \                                            ---------------  --------------
                    /     --------------   \                                           |  server 1   |  |  server 2  |
            ------------  |    LOAD    | ------------                                  ---------------  --------------
            | server 1 |  |  BALANCER  | | server 2 |
            ------------  -------------- ------------
        192.168.1.3       192.168.1.2        192.168.1.4

===================================================================
#                                                                 #
#                   Étapes de Configuration                       #
#                                                                 #
===================================================================

  1 --  CONFIGURATION DU LOAD BALANCER 192.168.1.2
  ------------------------------------------------
les pre-requis
--------------
   => Installation de Nginx et de openssh (pour la connexion ssh au serveur facultatif)
# sudo apt-get update
# sudo apt-get install nginx
# sudo apt-get install openssh-server

Configuration de Nginx :
------------------------
Création d'une fichier configuration de site pour le load balancing :
# sudo vim /etc/nginx/sites-available/site-static.conf

Maintenant configurons ce fichier en y ajoutant ces ligne de code
# upstream backend {
#     server 192.168.1.3;
#     server 192.168.1.4;
# }
# 
# server {
#     listen 80;
#     server_name www.site-static.com;
# 
#     location / {
#         proxy_pass http://backend;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#     }
# }
upstream backend : Ce bloc définit un groupe de serveurs backend qui vont gérer les requêtes. Les serveurs dans ce groupe seront utilisés pour le load balancing.
server 192.168.1.3 et server 192.168.1.4 : Ce sont les adresses IP des serveurs backend. Nginx distribuera les requêtes entre ces serveurs.
server : Ce bloc définit un serveur virtuel dans Nginx.
listen 80 : Nginx écoutera sur le port 80 pour les requêtes HTTP.
server_name www.site-static.com : Ce serveur virtuel répondra aux requêtes envoyées au domaine www.site-static.com.
location / : Ce bloc définit les règles pour le chemin racine (/). Toute requête correspondant à ce chemin sera traitée selon les directives à l'intérieur de ce bloc.

proxy_pass http://backend : Cette directive indique à Nginx de transmettre les requêtes au groupe de serveurs backend défini plus tôt. http://backend fait référence au bloc upstream backend.

proxy_set_header : Ces directives ajoutent des en-têtes HTTP aux requêtes envoyées aux serveurs backend.

proxy_set_header Host $host : Définit l'en-tête Host avec la valeur de la variable $host (le domaine de la requête).
proxy_set_header X-Real-IP $remote_addr : Ajoute l'en-tête X-Real-IP avec l'adresse IP du client qui a fait la requête.
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for : Ajoute l'en-tête X-Forwarded-For avec la chaîne d'adresses IP, permettant de garder une trace des adresses IP des clients.
proxy_set_header X-Forwarded-Proto $scheme : Ajoute l'en-tête X-Forwarded-Proto avec le schéma (HTTP ou HTTPS) de la requête d'origine.

Activer la configuration :
--------------------------
# sudo ln -s /etc/nginx/sites-available/site-static.conf /etc/nginx/sites-enabled/
# sudo systemctl restart nginx


  2 -- CONFIGURATION DE SERVEUR BACKEND (192.168.1.3 et 192.168.1.4)
  ------------------------------------------------------------------

les pre-requis:

Installer Apache :
------------------
# sudo apt-get update
# sudo apt-get install apache2

Configuration des vHosts Apache :
-------------------------------
Fichier de configuration : /etc/apache2/sites-available/000-default.conf
Éditez ce fichier 
# sudo vim /etc/apache2/sites-available/000-default.conf

Ajoutez y la configuration suivante :
# <VirtualHost *:80>
#     ServerName www.site-static.com
#     DocumentRoot /var/www/site-static
#     ErrorLog ${APACHE_LOG_DIR}/error.log
#     CustomLog ${APACHE_LOG_DIR}/access.log combined
# </VirtualHost>

Créer le répertoire pour le site web et placer les fichiers statiques :
-----------------------------------------------------------------------
# sudo mkdir -p /var/www/site-static
# sudo chown -R www-data:www-data /var/www/site-static
# echo "<html><body><h1>Welcome to www.site-static.com</h1></body></html>" | sudo tee /var/www/site-static/index.html

Activer le site et redémarrer Apache :
--------------------------------------
# sudo a2ensite 000-default
# sudo systemctl restart apache2


  3 -- ETAPE DE SYNCHRONISATION DES DEUX SERVEURS BACKEND
  -------------------------------------------------------
Pour garantir que les fichiers statiques sont synchronisés entre les serveurs backend, utilisez rsync.

configuration du serveur backend principale
-------------------------------------------
Sur le serveur backend principal (192.168.1.3)
Créer un script de synchronisation :
Fichier de script : /usr/local/bin/sync_files.sh
Créez et éditez le fichier :
# sudo vim /usr/local/bin/sync_files.sh

Ajoutez le contenu suivant :
# #!/bin/bash
# rsync -avz /var/www/site-static/ 192.168.1.4:/var/www/site-static/

Rendre le script exécutable :
# sudo chmod +x /usr/local/bin/sync_files.sh

Ajouter une tâche cron pour exécuter le script régulièrement :
# crontab -e
Ajoutez la ligne suivante pour synchroniser toutes les 2 minutes :
# */2 * * * * /usr/local/bin/sync_files.sh


Fonctionnement de l'Architecture en Haute Disponibilité
------------------------------------------------------
Distribution de la Charge :

Le serveur Nginx reçoit les requêtes des utilisateurs et les distribue de manière égale (ou selon les poids configurés) entre les serveurs backend 192.168.1.3 et 192.168.1.4.
Redondance :

Si un des serveurs backend tombe en panne, Nginx redirige automatiquement tout le trafic vers le serveur restant, assurant ainsi la continuité du service.
Synchronisation :

Grâce au script rsync, les fichiers statiques sont régulièrement synchronisés entre les serveurs backend. Ainsi, toute modification apportée à l'un des serveurs est répliquée sur l'autre, garantissant que les utilisateurs voient toujours le contenu à jour, même après une panne et un redémarrage.
Logs et Monitoring :

Les journaux d'accès et d'erreur sont conservés sur chaque serveur backend pour faciliter le débogage et le monitoring. Vous pouvez utiliser des outils comme Nagios ou Prometheus pour surveiller l'état des serveurs et recevoir des alertes en cas de problème.