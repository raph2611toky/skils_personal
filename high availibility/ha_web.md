
---

# **Haute Disponibilité de Serveur Web avec HAProxy et Apache**

Ce guide vous explique comment configurer un système de haute disponibilité en utilisant HAProxy comme load balancer pour distribuer les requêtes entre plusieurs serveurs Apache. Cela permet de garantir une disponibilité constante du service web, même en cas de panne d'un des serveurs.

## **I. Présentation**
L'objectif est de créer une architecture web où HAProxy distribue intelligemment les requêtes HTTP entre plusieurs serveurs Apache. Cette configuration assure la résilience et l'efficacité du service web.

## **II. Pré-requis**
- **Serveur HAProxy (Load Balancer)**
  - Exemple d'IP : 192.168.1.2
- **Serveurs Backend Apache**
  - Serveur 1 : 192.168.1.3
  - Serveur 2 : 192.168.1.4

## **Architecture**

### **Topologie Physique :**

```
        ROUTER 
           |
        SWITCH
           |
        HAProxy (192.168.1.2)
        /            \
       /              \
Apache Server 1      Apache Server 2
(192.168.1.3)        (192.168.1.4)
```

Cette topologie montre comment HAProxy, en tant que point d'entrée unique, distribue les requêtes entre les serveurs backend Apache.

## **III. Étapes de Configuration**

### 1. **Configuration du Load Balancer HAProxy (192.168.1.2)**

#### **Installation :**
- Installez HAProxy et OpenSSH :
  ```bash
  sudo apt-get update
  sudo apt-get install haproxy openssh-server
  ```

#### **Configuration HAProxy :**
- Ouvrez le fichier de configuration HAProxy :
  ```bash
  sudo vim /etc/haproxy/haproxy.cfg
  ```
- Ajoutez la configuration suivante pour définir les serveurs backend et les paramètres de load balancing :
  ```haproxy
  global
      log /dev/log    local0
      log /dev/log    local1 notice
      chroot /var/lib/haproxy
      stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
      stats timeout 30s
      user haproxy
      group haproxy
      daemon

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

  frontend http-in
      bind *:80
      default_backend servers

  backend servers
      balance roundrobin
      server server1 192.168.1.3:80 check
      server server2 192.168.1.4:80 check
  ```

#### **Activation et redémarrage HAProxy :**
- Activez HAProxy au démarrage et redémarrez le service :
  ```bash
  sudo systemctl enable haproxy
  sudo systemctl restart haproxy
  ```

### 2. **Configuration des Serveurs Backend (192.168.1.3 et 192.168.1.4)**

#### **Installation Apache :**
- Installez Apache sur chaque serveur backend :
  ```bash
  sudo apt-get update
  sudo apt-get install apache2
  ```

#### **Configuration des vHosts :**
- Modifiez le fichier de configuration Apache pour chaque serveur :
  ```bash
  sudo vim /etc/apache2/sites-available/000-default.conf
  ```
- Ajoutez cette configuration :
  ```apache
  <VirtualHost *:80>
      ServerName www.site-static.com
      DocumentRoot /var/www/site-static
      ErrorLog ${APACHE_LOG_DIR}/error.log
      CustomLog ${APACHE_LOG_DIR}/access.log combined

      <Directory /var/www/site-static >
          Options Indexes FollowSymLinks MultiViews
          AllowOverride None
          Order allow,deny
          Allow from all
      </Directory>
  </VirtualHost>
  ```

#### **Création du Répertoire du Site Web :**
- Créez le répertoire et placez-y un fichier HTML :
  ```bash
  sudo mkdir -p /var/www/site-static
  sudo chown -R www-data:www-data /var/www/site-static
  echo "<html><body><h1>Welcome to www.site-static.com</h1></body></html>" | sudo tee /var/www/site-static/index.html
  ```

#### **Activation et redémarrage Apache :**
- Activez le site et redémarrez Apache :
  ```bash
  sudo a2ensite 000-default
  sudo systemctl restart apache2
  ```

### 3. **Synchronisation des Serveurs Backend**

Pour assurer la cohérence des fichiers entre les serveurs backend, utilisez `rsync`.

#### **Configuration sur le Serveur Principal :**
- Créez un script de synchronisation sur le serveur 192.168.1.3 :
  ```bash
  sudo vim /usr/local/bin/sync_files.sh
  ```
- Ajoutez ce script :
  ```bash
  #!/bin/bash
  rsync -avz /var/www/site-static/ 192.168.1.4:/var/www/site-static/
  ```
- Rendez le script exécutable :
  ```bash
  sudo chmod +x /usr/local/bin/sync_files.sh
  ```
- Ajoutez une tâche cron pour synchroniser toutes les 2 minutes :
  ```bash
  crontab -e
  ```
  Ajoutez la ligne suivante :
  ```bash
  */2 * * * * /usr/local/bin/sync_files.sh
  ```

### **Fonctionnement de l'Architecture en Haute Disponibilité**

- **Équilibrage de Charge :** HAProxy distribue les requêtes entre les serveurs backend Apache selon l'algorithme de round-robin.
- **Redondance :** Si un serveur tombe en panne, HAProxy redirige automatiquement le trafic vers l'autre serveur.
- **Synchronisation :** Le script `rsync` garantit que les fichiers sont synchronisés entre les serveurs.
- **Logs et Monitoring :** HAProxy et Apache enregistrent les journaux des activités. Des outils comme Nagios ou Prometheus peuvent être utilisés pour surveiller l'état des serveurs.

### **Priorité au Serveur Maître**

Si vous souhaitez donner la priorité à un serveur spécifique, modifiez la configuration HAProxy comme suit :

```haproxy
backend servers
    balance roundrobin
    server server1 192.168.1.3:80 check weight=10
    server server2 192.168.1.4:80 check weight=1
```

### **Test du Failover**

- Démarrez les serveurs et simulez une panne en arrêtant le serveur principal :
  ```bash
  sudo systemctl stop apache2 # sur 192.168.1.3
  ```
- Vérifiez que le trafic est redirigé vers l'autre serveur.

---

```plaintext
---

Copyright © TOKY Nandrasana
Étudiant de l'École Nationale de l'Informatique
Date : 20 juillet 2024
```