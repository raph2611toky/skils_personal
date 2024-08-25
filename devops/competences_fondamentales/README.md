
---

# Compétences Fondamentales en DevOps


## 1. Systèmes et Réseaux

### 1.1 Linux

#### **Sécurité**

- **Gestion des Utilisateurs et Groupes** :
  - **Commandes** : `useradd`, `usermod`, `groupadd`, `passwd`.
  - **Exemple** : Créez un nouvel utilisateur et ajoutez-le à un groupe :
    ```bash
    sudo useradd -m -s /bin/bash newuser
    sudo passwd newuser
    sudo usermod -aG sudo newuser
    ```
  - **Documentation** : [Manage user Commands](https://www.geeksforgeeks.org/7-linux-commands-for-managing-users/)

- **Contrôle d’Accès** :
  - **Permissions de Fichiers** : `chmod`, `chown`, `chgrp`.
  - **Exemple** : Modifiez les permissions d’un fichier :
    ```bash
    chmod 750 /path/to/file
    chown user:group /path/to/file
    ```
  - **Documentation** : [File Permissions](https://linuxhandbook.com/linux-file-permissions/)

- **Pare-feu** :
  - **UFW (Uncomplicated Firewall)** : `ufw enable`, `ufw allow`, `ufw deny`.
  - **Exemple** : Configurez UFW pour autoriser le trafic HTTP et SSH :
    ```bash
    sudo ufw allow 80/tcp
    sudo ufw allow 22/tcp
    sudo ufw enable
    ```
  - **Documentation** : [UFW Documentation](https://help.ubuntu.com/community/UFW)

- **SELinux** :
  - **Commandes** : `sestatus`, `setenforce`, `semanage`.
    SELinux (Security-Enhanced Linux) est un mécanisme de sécurité qui fournit un contrôle d'accès obligatoire (MAC) au sein du noyau Linux. Contrairement aux permissions classiques (DAC), où les utilisateurs définissent les permissions sur les fichiers et les processus, SELinux applique des politiques strictes définies par l'administrateur système, limitant ainsi ce que les utilisateurs ou les processus peuvent faire, indépendamment des permissions définies sur les fichiers.

  ### **Concepts Clés de SELinux**

  1. **Types d'Accès** :
    - **Type Enforcement (TE)** : La stratégie la plus courante de SELinux, qui applique des règles strictes pour contrôler l'accès aux fichiers, aux sockets, et aux ports réseau en se basant sur les types d'objets et de domaines.
    - **Role-Based Access Control (RBAC)** : Implémente une hiérarchie de rôles qui contrôle l'accès des utilisateurs aux différents domaines de SELinux.
    - **Multi-Level Security (MLS)** : Utilisé pour des environnements où les données sont classifiées, permettant le contrôle d'accès en fonction du niveau de sensibilité.

  2. **Contexte SELinux** :
    - Chaque processus, fichier, et ressource réseau a un contexte SELinux, composé de quatre champs : `user:role:type:level`.
      - **User** : L'utilisateur SELinux, distinct des utilisateurs du système.
      - **Role** : Le rôle SELinux assigné au processus ou à l'utilisateur.
      - **Type** : Détermine le domaine dans lequel un processus fonctionne ou le type d'un fichier.
      - **Level** : Utilisé principalement dans les systèmes avec MLS, indiquant le niveau de sécurité.

  3. **Modes de SELinux** :
    - **Enforcing** : SELinux applique les politiques de sécurité, bloquant et enregistrant les tentatives d'accès non autorisées.
    - **Permissive** : SELinux ne bloque pas les accès non autorisés, mais enregistre les violations pour audit.
    - **Disabled** : SELinux est désactivé et n'applique aucune politique de sécurité.

  ### **Commandes SELinux**

  #### **1. Vérification du Statut SELinux**

  - **Commande** : `sestatus`
    - **Utilisation** : Cette commande affiche le statut actuel de SELinux, y compris le mode (enforcing, permissive, ou disabled), la politique en cours d’utilisation, et d’autres détails essentiels.
    - **Exemple** :
      ```bash
      sestatus
      ```
    - **Sortie typique** :
      ```bash
      SELinux status:                 enabled
      SELinuxfs mount:                /sys/fs/selinux
      SELinux root directory:         /etc/selinux
      Loaded policy name:             targeted
      Current mode:                   enforcing
      Mode from config file:          enforcing
      Policy MLS status:              enabled
      Policy deny_unknown status:     allowed
      Max kernel policy version:      31
      ```

  #### **2. Changement du Mode SELinux**

  - **Commande** : `setenforce`
    - **Utilisation** : Cette commande permet de basculer entre le mode enforcing et permissive sans redémarrer le système.
    - **Syntaxe** : 
      ```bash
      sudo setenforce [0|1]
      ```
      - `0` : Passe en mode permissive.
      - `1` : Passe en mode enforcing.
    - **Exemple** : Passez en mode permissive :
      ```bash
      sudo setenforce 0
      ```
      Pour vérifier que le mode a bien changé, vous pouvez relancer `sestatus`.

  #### **3. Configuration et Gestion des Politiques**

  - **Commande** : `semanage`
    - **Utilisation** : `semanage` est un outil puissant utilisé pour configurer et gérer les différents aspects de SELinux, y compris les ports, les fichiers, les utilisateurs, et les contextes de sécurité.
    - **Exemples courants** :
      - **Ajouter une exception pour un port** :
        Si vous avez un service web sur un port non standard, comme 8080, vous pouvez autoriser ce port via SELinux :
        ```bash
        sudo semanage port -a -t http_port_t -p tcp 8080
        ```
      - **Afficher les ports autorisés pour un service** :
        ```bash
        sudo semanage port -l | grep http_port_t
        ```
      - **Modifier le contexte d'un fichier** :
        Pour changer le contexte SELinux d'un fichier :
        ```bash
        sudo semanage fcontext -a -t httpd_sys_content_t "/web(/.*)?"
        sudo restorecon -R -v /web
        ```

  ### **Utilisation Pratique de SELinux**

  #### **1. Résolution de Problèmes avec SELinux**

  Lorsque SELinux est en mode enforcing, il peut bloquer certaines opérations qui seraient autrement permises avec des permissions Linux classiques. Pour diagnostiquer et corriger ces problèmes :

  - **Audit des Violations SELinux** :
    - SELinux journalise les violations dans `/var/log/audit/audit.log`. Vous pouvez utiliser `ausearch` ou `audit2allow` pour analyser et créer des règles permettant les actions spécifiques.
    - **Installation** :
      ```bash
      sudo apt update
      sudo apt install auditd
      ```
    - **Exemple** :
      ```bash
      ausearch -m avc -ts recent
      ```
    - **Audit2Allow** :
      Cet outil convertit les messages d’audit en une règle SELinux que vous pouvez appliquer pour permettre l’action en question.
      ```bash
      sudo audit2allow -a -M mymodule
      sudo semodule -i mymodule.pp
      ```

  #### **2. Gestion des Contexte SELinux**

  - **Restauration du Contexte** :
    - Si vous avez modifié les fichiers ou réinstallé un service, vous pourriez avoir besoin de restaurer les contextes SELinux par défaut.
    - **Commande** :
      ```bash
      sudo restorecon -R /path/to/directory
      ```
      Cette commande récursive réinitialisera les contextes sur les fichiers dans le chemin spécifié.

  ### **Ressources Complémentaires**

  - **Guide Complet SELinux** : [Red Hat SELinux Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/using_selinux/index)
  - **Tutoriaux et Guides Pratiques** : [SELinux for Mere Mortals](https://wiki.centos.org/HowTos/SELinux)

  SELinux est un outil puissant pour renforcer la sécurité de vos systèmes Linux. Une bonne maîtrise de ses concepts et de ses commandes permet de déployer des serveurs avec une sécurité accrue tout en assurant que vos applications fonctionnent sans heurts.
  - **Documentation** : [SELinux Project](https://itslinuxfoss.com/all-basic-selinux-commands-you-need-to-know/)

#### **Système**

### **Gestion des Processus sous Linux**

  La gestion des processus est une compétence fondamentale pour administrer un système Linux. Un processus est une instance en cours d'exécution d'un programme. Comprendre comment lister, surveiller, modifier et terminer les processus est essentiel pour maintenir la stabilité et les performances du système.

  #### **1. `ps` - Afficher les processus**
  La commande `ps` affiche une liste des processus en cours d'exécution sur le système. Il existe plusieurs options pour personnaliser l'affichage des processus.

  - **`ps aux`** : Affiche tous les processus en cours avec des détails tels que l'utilisateur, le PID (identifiant du processus), l'utilisation CPU et mémoire.
    ```bash
    ps aux
    ```

  #### **2. `top` et `htop` - Surveiller les processus en temps réel**
  - **`top`** : Affiche les processus en temps réel, avec des informations sur l'utilisation du CPU, de la mémoire, et bien plus. C'est utile pour identifier rapidement les processus gourmands en ressources.
    ```bash
    top
    ```
    - **Navigation dans `top`** : Vous pouvez appuyer sur `k` pour tuer un processus en fournissant son PID, ou `r` pour renommer un processus.

  - **`htop`** : Une version améliorée de `top`, avec une interface plus conviviale et interactive. Il permet de visualiser facilement les processus et d'interagir avec eux.
    ```bash
    htop
    ```

  #### **3. `kill` - Terminer un processus**
  La commande `kill` envoie un signal à un processus pour le terminer. Le signal le plus couramment utilisé est `SIGTERM` (15), mais vous pouvez aussi envoyer un `SIGKILL` (9) pour forcer l'arrêt.

  - **`kill <PID>`** : Envoie un signal `SIGTERM` au processus avec le PID spécifié.
    ```bash
    kill 1234
    ```
  - **`kill -9 <PID>`** : Envoie un signal `SIGKILL` pour forcer l'arrêt du processus.
    ```bash
    kill -9 1234
    ```

  #### **4. `nice` et `renice` - Modifier la priorité d'un processus**
  Les commandes `nice` et `renice` permettent de modifier la priorité d'un processus, influençant la quantité de CPU qu'il peut utiliser. Les valeurs de `nice` vont de -20 (haute priorité) à 19 (basse priorité).

  - **Lancer un processus avec une priorité basse** :
    ```bash
    sudo nice -n 10 <commande>
    ```
  - **Modifier la priorité d'un processus existant** :
    ```bash
    sudo renice 5 -p <PID>
    ```

  #### **5. `ss` et `lsof` - Surveillance des connexions réseau et des fichiers ouverts**
  - **`ss`** : Remplace `netstat` pour surveiller les sockets réseau. Il est plus rapide et affiche des informations détaillées sur les connexions réseau et les ports utilisés.
    ```bash
    ss -tuln
    ```
  - **`lsof`** : Affiche les fichiers ouverts par les processus, ce qui inclut les connexions réseau.
    ```bash
    sudo lsof -i :80
    ```
  - **Documentation** : [process management Commands](https://www.digitalocean.com/community/tutorials/process-management-in-linux)

- **Gestion des Services** :
  - **Commandes** : `systemctl`, `service`.
  - **Exemple** : Démarrez, arrêtez et vérifiez l’état d’un service :
    ```bash
    sudo systemctl start nginx
    sudo systemctl status nginx
    sudo systemctl stop nginx
    ```
  - **Documentation** : [systemctl Manual](https://www.geeksforgeeks.org/systemctl-in-unix/), [create or remove services](https://www.baeldung.com/linux/create-remove-systemd-services)


### **Gestion des Disques sous Linux**

  La gestion des disques est cruciale pour administrer efficacement l'espace de stockage et garantir la bonne organisation des données sur un système Linux. Voici un aperçu des commandes essentielles pour gérer les disques.

  #### **1. `fdisk` - Gestion des partitions**
  `fdisk` est un utilitaire en ligne de commande pour manipuler la table de partition d'un disque dur.

  - **Lister les partitions** :
    ```bash
    sudo fdisk -l
    ```
    Cette commande affiche la table de partition de tous les disques disponibles sur le système.

  - **Modifier les partitions** :
    ```bash
    sudo fdisk /dev/sdX
    ```
    Cette commande ouvre une interface interactive pour créer, modifier ou supprimer des partitions sur le disque spécifié (`/dev/sdX`).

  #### **2. `parted` - Partitionnement avancé**
  `parted` est un outil plus moderne et puissant que `fdisk`, spécialement pour les grands disques (>2TB) ou les tables de partition GPT.

  - **Créer une nouvelle partition** :
    ```bash
    sudo parted /dev/sdX mkpart primary ext4 1MiB 100%
    ```
    Crée une nouvelle partition primaire en utilisant tout l'espace disponible.

  - **Vérifier la table de partition** :
    ```bash
    sudo parted /dev/sdX print
    ```

  #### **3. `mount` et `umount` - Monter et démonter des systèmes de fichiers**
  Ces commandes permettent de monter un système de fichiers dans un répertoire spécifique, rendant ainsi les données accessibles.

  - **Monter une partition** :
    ```bash
    sudo mount /dev/sdX1 /mnt
    ```
    Cette commande monte la partition `/dev/sdX1` sur le répertoire `/mnt`.

  - **Démonter une partition** :
    ```bash
    sudo umount /mnt
    ```

  #### **4. `df` - Afficher l’utilisation des systèmes de fichiers**
  La commande `df` fournit un aperçu de l'utilisation de l'espace disque sur tous les systèmes de fichiers montés.

  - **Utilisation du disque avec formatage lisible** :
    ```bash
    df -h
    ```
    Le `-h` affiche les informations en format "lisible par l'homme" (en GB, MB, etc.).

  #### **5. `du` - Estimation de l’utilisation de l’espace disque**
  `du` est utilisé pour estimer l'espace disque utilisé par des fichiers et des répertoires.

  - **Afficher l'utilisation de l'espace par répertoire** :
    ```bash
    du -sh /var/log
    ```
    Le `-s` résume l'utilisation pour chaque répertoire, et le `-h` affiche les résultats dans un format lisible.

  - **Documentation** : [fdisk Manual](https://man7.org/linux/man-pages/man8/fdisk.8.html)

### **Réseaux sous Linux**

#### **Protocoles et Services**

- **TCP/IP, HTTP/HTTPS, DNS** :
  - **TCP/IP** : Le protocole de base pour la communication sur Internet. TCP assure une transmission fiable des données, tandis que IP s'occupe de l'adressage des paquets.
  - **HTTP/HTTPS** : Protocoles utilisés pour la navigation sur le web. HTTP est non sécurisé, tandis que HTTPS chiffre les données échangées via SSL/TLS.
  - **DNS** : Service qui traduit les noms de domaine en adresses IP. Comprendre comment configurer les serveurs DNS et utiliser `dig` ou `nslookup` pour les diagnostics DNS.

  - **Exemple** : Utilisez `netstat` pour vérifier les connexions réseau :
    ```bash
    netstat -tuln
    ```
    Cette commande liste les connexions réseau actives, en montrant les ports ouverts (-t pour TCP, -u pour UDP, -l pour les ports en écoute, et -n pour ne pas résoudre les noms d'hôte).

#### **Surveillance du Réseau**

- **iftop** : Montre l'utilisation de la bande passante en temps réel pour chaque connexion.
- **tcpdump** : Capture et analyse le trafic réseau brut. Il est puissant pour le diagnostic réseau et la capture de paquets pour une analyse ultérieure.
- **Wireshark** : Un outil graphique pour analyser le trafic réseau de manière plus détaillée et conviviale.

  - **Exemple** : Capturez le trafic réseau avec `tcpdump` :
    ```bash
    sudo tcpdump -i eth0
    ```
    Cette commande capture tout le trafic sur l'interface `eth0`. Vous pouvez filtrer par protocole, port, ou adresse IP pour affiner les captures.

  - **Documentation** : [tcpdump Manual](https://www.tcpdump.org/manpages/tcpdump.1.html)

#### **Configuration de Réseau**

- **ip** : Commande moderne pour la gestion des interfaces réseau, remplaçant `ifconfig`.
- **ifconfig** : Ancienne commande pour configurer les interfaces réseau, encore utile sur certains systèmes.
- **route** : Utilisée pour afficher et manipuler la table de routage IP.

  - **Exemple** : Configurez une interface réseau avec `ip` :
    ```bash
    sudo ip addr add 192.168.1.100/24 dev eth0
    sudo ip route add default via 192.168.1.1
    ```
    - La première commande assigne l'adresse IP `192.168.1.100` avec un masque de sous-réseau `/24` à l'interface `eth0`.
    - La seconde commande ajoute une route par défaut via le routeur `192.168.1.1`.

  - **Documentation** : [ip Command](https://man7.org/linux/man-pages/man8/ip.8.html)

### 1.2 Windows

#### **Sécurité**

- **Gestion des Utilisateurs et Groupes** :
  - **Commandes** : `net user`, `net localgroup`.
  - **Exemple** : Créez un nouvel utilisateur et ajoutez-le à un groupe :
    ```powershell
    net user newuser /add
    net localgroup administrators newuser /add
    ```

- **Pare-feu** :
  - **Commandes** : `netsh advfirewall`.
  - **Exemple** : Configurez le pare-feu pour autoriser le trafic HTTP :
    ```powershell
    netsh advfirewall firewall add rule name="Allow HTTP" protocol=TCP dir=in localport=80 action=allow
    ```

#### **Système**

- **Gestion des Processus** :
  - **Commandes** : `tasklist`, `taskkill`.
  - **Exemple** : Listez les processus et arrêtez un processus :
    ```powershell
    tasklist
    taskkill /PID 1234
    ```

- **Gestion des Services** :
  - **Commandes** : `sc`, `Get-Service`, `Start-Service`.
  - **Exemple** : Démarrez et arrêtez un service :
    ```powershell
    Start-Service -Name "wuauserv"
    Stop-Service -Name "wuauserv"
    ```

## 2. Programmation

### 2.1 Bash

- **Scripts Avancés** :
  - **Exemples** : Création de scripts pour des sauvegardes automatisées, gestion de configurations complexes.
  - **Exemple** : Créez un script de sauvegarde avec compression et notifications :
    ```bash
    #!/bin/bash
    BACKUP_DIR="/backup"
    TIMESTAMP=$(date +%F_%T)
    tar -czf $BACKUP_DIR/backup_$TIMESTAMP.tar.gz /important/data
    echo "Backup completed at $TIMESTAMP" | mail -s "Backup Report" user@example.com
    ```
  - **Documentation** : [Bash Scripting Guide](https://tldp.org/LDP/abs/html/)

### 2.2 Python

- **Scripting et Automation** :
  - **Exemples** : Automatisation des tâches, intégration avec des API, manipulation des données.
  - **Exemple** : Utilisez Python pour interagir avec une API et traiter les données :
    ```python
    import requests

    response = requests.get('https://api.example.com/data')
    data = response.json()

    for item in data['items']:
        print(item['name'])
    ```
  - **Documentation** : [Python Requests Library](https://docs.python-requests.org/en/latest/)

### 2.3 PowerShell

- **Scripts Avancés** :
  - **Exemples** : Automatisation des tâches d’administration système, gestion des configurations.
  - **Exemple** : Créez un script pour surveiller l’espace disque et envoyer une alerte :
    ```powershell
    $disk = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Used / $_.UsedSpace -lt 0.1}
    if ($disk) {
        $message = "Disk space low on $($disk.Name)"
        Send-MailMessage -To 'admin@example.com' -Subject 'Disk Space Alert' -Body $message -SmtpServer 'smtp.example.com'
    }
    ```
  - **Documentation** : [PowerShell Documentation](https://docs.microsoft.com/en-us/powershell/)

### **3. Gestion de Configuration**

### **3.1 Ansible : Gestion des Rôles et Templates Avancés**

#### **Gestion des Rôles**

Les rôles dans Ansible permettent de structurer des playbooks en modules réutilisables. Chaque rôle est conçu pour accomplir une tâche spécifique ou un ensemble de tâches liées. Voici une explication détaillée avec un exemple complet pour configurer un serveur web et une base de données avec Ansible.

#### **Structure des Rôles**

La structure des rôles facilite l'organisation et la réutilisation du code. Chaque rôle est généralement constitué des répertoires et fichiers suivants :
- **tasks/** : Contient les tâches à exécuter, définies dans des fichiers YAML.
- **handlers/** : Contient les handlers, des tâches spéciales déclenchées par d'autres tâches (par exemple, redémarrer un service).
- **templates/** : Contient des templates Jinja2 pour générer des fichiers de configuration dynamiques.
- **vars/** : Contient les variables spécifiques au rôle.
- **defaults/** : Contient les valeurs par défaut pour les variables du rôle.

#### **Exemple Complet**

Supposons que nous voulons déployer une application web et une base de données MySQL en utilisant Ansible. Nous allons créer deux rôles : `webserver` et `database`.

##### **1. Structure du Projet**

```
ansible/
├── roles/
│   ├── webserver/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   └── nginx.conf.j2
│   │   └── vars/
│   │       └── main.yml
│   └── database/
│       ├── tasks/
│       │   └── main.yml
│       ├── templates/
│       │   └── my.cnf.j2
│       └── vars/
│           └── main.yml
└── site.yml
```

##### **2. Rôle `webserver`**

- **roles/webserver/tasks/main.yml** :
  ```yaml
  - name: Install Nginx
    apt:
      name: nginx
      state: present

  - name: Configure Nginx
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf

  - name: Ensure Nginx is running
    service:
      name: nginx
      state: started
      enabled: yes
  ```

- **roles/webserver/templates/nginx.conf.j2** :
  ```jinja
  server {
      listen 80;
      server_name {{ server_name }};
      location / {
          proxy_pass http://127.0.0.1:8080;
      }
  }
  ```

- **roles/webserver/vars/main.yml** :
  ```yaml
  server_name: mywebsite.com
  ```

##### **3. Rôle `database`**

- **roles/database/tasks/main.yml** :
  ```yaml
  - name: Install MySQL
    apt:
      name: mysql-server
      state: present

  - name: Configure MySQL
    template:
      src: my.cnf.j2
      dest: /etc/mysql/my.cnf

  - name: Ensure MySQL is running
    service:
      name: mysql
      state: started
      enabled: yes
  ```

- **roles/database/templates/my.cnf.j2** :
  ```jinja
  [mysqld]
  bind-address = 0.0.0.0
  max_connections = {{ max_connections }}
  ```

- **roles/database/vars/main.yml** :
  ```yaml
  max_connections: 200
  ```

##### **4. Playbook Principal**

- **site.yml** :
  ```yaml
  - name: Deploy Web Server and Database
    hosts: all
    become: yes
    roles:
      - webserver
      - database
  ```

#### **Explication**

- **Structure des Rôles** : Chaque rôle est isolé dans son propre répertoire avec des fichiers dédiés pour les tâches, templates, et variables. Cela rend le code modulaire et facile à gérer.
  
- **Templates** : Les fichiers Jinja2 permettent de générer des configurations dynamiques. Par exemple, le fichier `nginx.conf.j2` utilise la variable `server_name` pour personnaliser la configuration de Nginx.

- **Variables** : Les variables définies dans `vars/main.yml` peuvent être utilisées dans les templates et tâches pour adapter les configurations aux besoins spécifiques de l’environnement.

- **Playbook Principal** : Le fichier `site.yml` coordonne l'exécution des rôles. Il applique les rôles `webserver` et `database` sur tous les hôtes ciblés.

#### **Documentation Complémentaire**

- [Ansible Rôles Documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_roles.html)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/)

En suivant cet exemple et en utilisant les fonctionnalités avancées des rôles et des templates d'Ansible, vous pouvez structurer des déploiements complexes de manière modulaire et maintenable.

#### **3.2 Puppet**

- **Manifests Avancés** :
  - **Gestion des Dépendances** : Puppet permet de spécifier les relations entre ressources pour s'assurer que certaines actions se produisent avant ou après d'autres. Par exemple, vous pouvez assurer qu'un service est démarré seulement après l'installation d'un package.
    ```puppet
    package { 'nginx':
      ensure => installed,
    }

    file { '/etc/nginx/nginx.conf':
      ensure  => file,
      content => template('nginx/nginx.conf.erb'),
      require => Package['nginx'],
    }

    service { 'nginx':
      ensure    => running,
      enable    => true,
      subscribe => File['/etc/nginx/nginx.conf'],
    }
    ```
    - Ici, le fichier de configuration de Nginx est généré après l’installation du package, et le service Nginx est redémarré automatiquement si le fichier de configuration change.

  - **Modules** : Les modules Puppet sont des collections de manifests, de templates, de fichiers, et d'autres éléments permettant de gérer des configurations spécifiques. Ils peuvent être téléchargés depuis Puppet Forge ou créés manuellement.
    - **Exemple de Module pour Nginx** :
      ```puppet
      class nginx {
        package { 'nginx':
          ensure => installed,
        }

        file { '/etc/nginx/nginx.conf':
          ensure  => file,
          content => template('nginx/nginx.conf.erb'),
        }

        service { 'nginx':
          ensure => running,
          enable => true,
        }
      }
      ```

#### **3.3 Chef**

- **Recettes Avancées** :
  - **Recettes et Cookbooks** : Les recettes (recipes) sont des instructions de configuration regroupées dans des cookbooks. Un cookbook peut gérer une application complète, incluant l'installation, la configuration, et la gestion du service.
  - **Exemple de Cookbook pour une Application Web** :
    - **recipes/default.rb** :
      ```ruby
      include_recipe 'nginx::default'

      template '/etc/nginx/sites-available/my_site' do
        source 'my_site.erb'
        notifies :reload, 'service[nginx]'
      end

      service 'nginx' do
        action [:enable, :start]
      end
      ```
      - **templates/default/my_site.erb** :
        ```erb
        server {
          listen 80;
          server_name <%= node['my_site']['server_name'] %>;
          location / {
            proxy_pass http://127.0.0.1:8080;
          }
        }
        ```
      - **attributes/default.rb** :
        ```ruby
        default['my_site']['server_name'] = 'mywebsite.com'
        ```

      Ce cookbook installe et configure Nginx, puis déploie un site web dont le nom de serveur est défini dans les attributs.

  - **Environnements** : Chef permet de gérer différents environnements (production, staging, développement) avec des configurations spécifiques pour chaque environnement.
    - **Exemple d'Environnement** (environments/production.rb) :
      ```ruby
      name 'production'
      description 'Production Environment'
      cookbook_versions({
        'nginx' => '>= 1.2.0',
      })
      default_attributes({
        'my_site' => {
          'server_name' => 'www.production-site.com'
        }
      })
      ```
      Ce fichier d'environnement spécifie que le site en production doit utiliser un nom de domaine spécifique et une version donnée du cookbook Nginx.

Chaque outil de gestion de configuration offre des possibilités avancées pour automatiser, standardiser, et maintenir des environnements complexes, facilitant ainsi la gestion de l'infrastructure.