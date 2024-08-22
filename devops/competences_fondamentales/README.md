
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
  - **Documentation** : [Adduser Command](https://man7.org/linux/man-pages/man8/adduser.8.html)

- **Contrôle d’Accès** :
  - **Permissions de Fichiers** : `chmod`, `chown`, `chgrp`.
  - **Exemple** : Modifiez les permissions d’un fichier :
    ```bash
    chmod 750 /path/to/file
    chown user:group /path/to/file
    ```
  - **Documentation** : [File Permissions](https://www.gnu.org/software/coreutils/manual/html_node/Changing-File-Attributes.html)

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
  - **Exemple** : Vérifiez le statut de SELinux et modifiez son mode :
    ```bash
    sestatus
    sudo setenforce 0
    ```
  - **Documentation** : [SELinux Project](https://selinuxproject.org/)

#### **Système**

- **Gestion des Processus** :
  - **Commandes** : `ps`, `top`, `htop`, `kill`, `nice`.
  - **Exemple** : Listez les processus et modifiez leur priorité :
    ```bash
    ps aux
    top
    sudo nice -n 10 command_to_run
    ```
  - **Documentation** : [ps Command](https://man7.org/linux/man-pages/man1/ps.1.html)

- **Gestion des Services** :
  - **Commandes** : `systemctl`, `service`.
  - **Exemple** : Démarrez, arrêtez et vérifiez l’état d’un service :
    ```bash
    sudo systemctl start nginx
    sudo systemctl status nginx
    sudo systemctl stop nginx
    ```
  - **Documentation** : [systemctl Manual](https://www.freedesktop.org/wiki/Software/systemd/man/systemctl/)

- **Gestion des Disques** :
  - **Commandes** : `fdisk`, `parted`, `mount`, `df`, `du`.
  - **Exemple** : Affichez l’utilisation du disque et montez un disque :
    ```bash
    df -h
    sudo mount /dev/sdX1 /mnt
    ```
  - **Documentation** : [fdisk Manual](https://man7.org/linux/man-pages/man8/fdisk.8.html)

#### **Réseaux**

- **Protocoles et Services** :
  - **TCP/IP, HTTP/HTTPS, DNS** : Comprendre le fonctionnement et la configuration de ces protocoles.
  - **Exemple** : Utilisez `netstat` pour vérifier les connexions réseau :
    ```bash
    netstat -tuln
    ```

- **Surveillance du Réseau** :
  - **Commandes** : `iftop`, `tcpdump`, `wireshark`.
  - **Exemple** : Capturez le trafic réseau avec `tcpdump` :
    ```bash
    sudo tcpdump -i eth0
    ```
  - **Documentation** : [tcpdump Manual](https://www.tcpdump.org/manpages/tcpdump.1.html)

- **Configuration de Réseau** :
  - **Commandes** : `ip`, `ifconfig`, `route`.
  - **Exemple** : Configurez une interface réseau :
    ```bash
    sudo ip addr add 192.168.1.100/24 dev eth0
    sudo ip route add default via 192.168.1.1
    ```
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

## 3. Gestion de Configuration

### 3.1 Ansible

- **Playbooks Avancés** :
  - **Exemples** : Déploiement multi-tier, gestion des rôles, utilisation de variables et templates.
  - **Exemple** : Configurez un serveur web avec des variables et des templates :
    ```yaml
    - name: Configure Web Server
      hosts: web
      vars:
        server_name: mywebsite.com
      tasks:
        - name: Install Nginx
          apt:
            name: nginx
            state: present
        - name: Configure Nginx
          template:
            src: /templates/nginx.conf.j2
            dest: /etc/nginx/nginx.conf
        - name: Start Nginx
          service:
            name: nginx
            state: started
            enabled: yes
    ```
  - **Documentation** : [Ansible Documentation](https://docs.ansible.com/ansible/latest/index.html)

### 3.2 Puppet

- **Manifests

 Avancés** :
  - **Exemples** : Gestion des dépendances, utilisation des modules, configuration des nœuds.
  - **Exemple** : Configurez un serveur avec Puppet et un module pour Nginx :
    ```puppet
    node 'web.example.com' {
      include nginx
    }

    class { 'nginx':
      manage_repo => true,
      package_ensure => 'latest',
      service_ensure => 'running',
    }
    ```
  - **Documentation** : [Puppet Documentation](https://puppet.com/docs/puppet/latest/puppet_index.html)

### 3.3 Chef

- **Recettes Avancées** :
  - **Exemples** : Utilisation de recettes personnalisées, gestion des environnements, intégration avec des services externes.
  - **Exemple** : Configurez un serveur MySQL avec Chef :
    ```ruby
    mysql_service 'default' do
      port '3306'
      version '5.7'
      initial_root_password 'my_password'
      action [:create, :start]
    end

    mysql_client 'default' do
      action :create
    end

    mysql_database 'my_database' do
      connection(
        :host => '127.0.0.1',
        :username => 'root',
        :password => 'my_password'
      )
      action :create
    end
    ```
  - **Documentation** : [Chef Documentation](https://docs.chef.io/)

---

## Ressources Complémentaires

- **Listes de Commandes Linux** :
  - [Linux Command Line Basics](https://www.digitalocean.com/community/tutorial_series/linux-command-line-basics)
  - [Linux Commands Cheat Sheet](https://www.tecmint.com/linux-commands-cheat-sheet/)

- **Documentation Générale** :
  - **Linux Security** : [Linux Security Cookbook](https://www.oreilly.com/library/view/linux-security/0596003910/)
  - **Python Programming** : [Python Official Documentation](https://docs.python.org/3/)
  - **PowerShell** : [Microsoft PowerShell Documentation](https://docs.microsoft.com/en-us/powershell/)

En développant une compréhension approfondie et en pratiquant ces compétences, vous serez bien préparé pour aborder des défis complexes dans le domaine du DevOps.