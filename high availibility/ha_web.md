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

#      upstream www.site-static.com {
#         server 192.168.1.3;
#         server 192.168.1.4;
#      }
# 
#      server {
#         listen 80;
#         server_name www.site-static.com;
# 
#         location / {
#             proxy_pass http://www.site-static.com;
#             proxy_set_header Host $host;
#             proxy_set_header X-Real-IP $remote_addr;
#             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#             proxy_set_header X-Forwarded-Proto $scheme;
#         }
#      }

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

#    <Directory /var/www/site-static >
#           Options Indexes FollowSymLinks MultiViews
#           AllowOverride None
#           Order allow,deny
#           Allow from all
#     </Directory>
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

PHASE DE TESTE:
Maintenant, on peut tester si ca marche, via le navigateur d'un client qui peut pinguer ou acceder au serveur en tapant  http://www.site-static.com sur le navigateur ou en faisant curl http://www.site-static.com dans terminale.


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

Pour implémenter une architecture de failover avec une priorité pour un serveur maître (principal) et des serveurs esclaves (secondaires) en utilisant Nginx, nous devons configurer Nginx de manière à ce qu'il donne la priorité au serveur principal tant qu'il est disponible.

Voici comment vous pouvez configurer cela :

1. Configuration de Nginx pour le Load Balancing avec Priorité de Serveur Maître

Sur le serveur Nginx (Load Balancer) -> 192.168.1.2
Configuration de Nginx :

Fichier de configuration : /etc/nginx/sites-available/site-static.conf
éditez le fichier :
# sudo vim /etc/nginx/sites-available/site-static.conf

et modifier l'ancien configuration à ceci:
# upstream backend {
#     server 192.168.1.3 weight=10 max_fails=3 fail_timeout=30s; # Serveur maître
#     server 192.168.1.4 weight=1 max_fails=3 fail_timeout=30s;  # Serveur esclave
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

weight=10 : Le serveur principal (192.168.1.3) a un poids plus élevé, ce qui signifie qu'il recevra plus de requêtes que le serveur secondaire (192.168.1.4).
max_fails=3 : Si le serveur échoue à répondre 3 fois de suite, il sera marqué comme défaillant.
fail_timeout=30s : Après avoir marqué le serveur comme défaillant, il sera exclu du pool pendant 30 secondes avant d'être réessayé.

 Fonctionnement du Failover
 --------------------------
Vérification de Disponibilité : Nginx surveille chaque serveur backend. Si le serveur principal ne répond pas correctement à 3 requêtes consécutives dans un délai de 30 secondes, il est considéré comme défaillant.
Redirection Automatique : Lorsqu'un serveur est marqué comme défaillant, Nginx cesse de lui envoyer des requêtes et redirige automatiquement tout le trafic vers les serveurs restants.
Rétablissement Automatique : Après le délai de 30 secondes, Nginx retente d'envoyer des requêtes au serveur défaillant. Si le serveur principal répond correctement, il est réintégré dans le pool de serveurs disponibles et commence à recevoir des requêtes à nouveau, reprenant son rôle prioritaire.

 Exécution et Tests
Pour tester le failover :

Démarrez les serveurs : Assurez-vous que les serveurs backend (192.168.1.3 et 192.168.1.4) sont opérationnels.

Simulez une panne : Arrêtez le serveur principal (192.168.1.3).

# sudo systemctl stop apache2 # sur le serveur principal
Observez le comportement : Accédez au site via le load balancer. Nginx redirigera automatiquement les requêtes vers le serveur secondaire (192.168.1.4).

Redémarrez le serveur en panne : Après avoir redémarré le serveur principal, observez que Nginx le réintègre dans le pool de serveurs disponibles après le délai de fail_timeout et commence à lui rediriger les requêtes.

# sudo systemctl start apache2 # sur le serveur principal



UTILISATION DE HA PROXY POUR LA CONFIGURATION DU LOAD BALANCER
--------------------------------------------------------------
installer haproxy
# sudo apt install haproxy

et puis editer la fichier de configuration /etc/haproxy/haproxy.conf

root@ubuntuserver16:/home/raph# cat /etc/haproxy/haproxy.cfg 
global
        log /dev/log    local0
        log /dev/log    local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin
        stats timeout 30s
        user haproxy
        group haproxy
        daemon

        # Default SSL material locations
        ca-base /etc/ssl/certs
        crt-base /etc/ssl/private

        # Default ciphers to use on SSL-enabled listening sockets.
        # For more information, see ciphers(1SSL). This list is from:
        #  https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/
        ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS      
        ssl-default-bind-options no-sslv3

defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        timeout connect 5000
        timeout client  50000
        timeout server  50000
        errorfile 400 /etc/haproxy/errors/400.http
        errorfile 403 /etc/haproxy/errors/403.http
        errorfile 408 /etc/haproxy/errors/408.http
        errorfile 500 /etc/haproxy/errors/500.http
        errorfile 502 /etc/haproxy/errors/502.http
        errorfile 503 /etc/haproxy/errors/503.http
        errorfile 504 /etc/haproxy/errors/504.http

frontend www.site-static.com
        bind *:80
        option httplog
        mode http
        default_backend servers

backend servers
        balance roundrobin
        server web1 192.168.15.77:80 check
        server web2 192.168.15.76:80 check
root@ubuntuserver16:/home/raph#

le www.site-static est juste une nom de configuration, 
web1 est le nom attribué au serveur ayant l'ip 192.168.15.77(qui est celle du premier server)


puis après, redemarrer le service haproxy
# sudo systemctl restart haproxy

ca marche!

AJOUTER LE FAILOVER AVEC HAPROXY
--------------------------------
reediter la fichier de configuration de haproxy
global
        log /dev/log    local0
        log /dev/log    local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin
        stats timeout 30s
        user haproxy
        group haproxy
        daemon

        # Default SSL material locations
        ca-base /etc/ssl/certs
        crt-base /etc/ssl/private

        # Default ciphers to use on SSL-enabled listening sockets.
        # For more information, see ciphers(1SSL). This list is from:
        #  https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/
        ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS
        ssl-default-bind-options no-sslv3

defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        timeout connect 5000
        timeout client  50000
        timeout server  50000
        errorfile 400 /etc/haproxy/errors/400.http
        errorfile 403 /etc/haproxy/errors/403.http
        errorfile 408 /etc/haproxy/errors/408.http
        errorfile 500 /etc/haproxy/errors/500.http
        errorfile 502 /etc/haproxy/errors/502.http
        errorfile 503 /etc/haproxy/errors/503.http
        errorfile 504 /etc/haproxy/errors/504.http

frontend www.site-static.com
        bind *:80
        option httplog
        mode http
        acl MAIN_not_enough_capacity nbsrv(bk_app_main) le 1
        use_backend bk_app_backup if MAIN_not_enough_capacity
        default_backend bk_app_main

backend bk_app_main
        balance roundrobin
        server web1 192.168.15.77:80 check
        server web2 192.168.15.76:80 check

backend bk_app_backup
        option allbackups
        server ldb 192.168.15.78:80 check


Pour synchroniser les trois serveurs web (web1, web2 et ldb) en temps réel et assurer la haute disponibilité, vous pouvez utiliser un outil de synchronisation de fichiers tel que rsync ou un système de fichiers distribués comme GlusterFS. Voici deux approches possibles :

Approche 1 : Utilisation de rsync pour la synchronisation périodique
rsync peut être utilisé pour synchroniser périodiquement les fichiers entre les serveurs web. Voici un exemple de script rsync et une configuration de cron pour la synchronisation.

Script rsync
Créez un script rsync pour synchroniser les fichiers de web1 et web2 vers ldb :

sh
Copier le code
#!/bin/bash

# Serveurs sources
SOURCE1="192.168.15.77:/path/to/webroot/"
SOURCE2="192.168.15.76:/path/to/webroot/"

# Serveur de destination
DESTINATION="192.168.15.78:/path/to/webroot/"

# Synchroniser depuis web1
rsync -avz --delete $SOURCE1 $DESTINATION

# Synchroniser depuis web2
rsync -avz --delete $SOURCE2 $DESTINATION
Remplacez /path/to/webroot/ par le chemin réel du répertoire web sur vos serveurs.

Configuration de cron
Ajoutez une tâche cron pour exécuter le script de synchronisation périodiquement :

sh
Copier le code
crontab -e
Ajoutez la ligne suivante pour exécuter le script toutes les 5 minutes (ajustez l'intervalle selon vos besoins) :

sh
Copier le code
*/5 * * * * /path/to/rsync_script.sh
Remplacez /path/to/rsync_script.sh par le chemin réel de votre script rsync.