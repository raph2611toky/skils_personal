# ############################################################################### #
#                                                                                 #
#                      CONFIGURATION DE VOIP AVEC ASTERISK                        #
#                                                                                 #
# ############################################################################### #

Tout d'abord, mettez à jour vos packages système vers la dernière version à l'aide de la commande suivante :
# apt-get update -y

Une fois votre système mis à jour, vous devrez installer d'autres dépendances requises par Asterisk. Vous pouvez tous les installer avec la commande suivante :
# apt-get install gnupg2 software-properties-common git curl wget libnewt-dev libssl-dev libncurses5-dev subversion libsqlite3-dev build-essential libjansson-dev libxml2-dev uuid-dev -y

Après avoir installé tous les packages, vous pouvez passer à l'étape suivante

## Installer l'astérisque
Par défaut, la dernière version d'Asterisk n'est pas disponible dans le référentiel par défaut d'Ubuntu 20.04. Vous devrez donc le télécharger et le compiler à partir de la source.
Tout d'abord, téléchargez la dernière version d'Asterisk avec la commande suivante :
# wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-17-current.tar.gz

Une fois téléchargé, extrayez le fichier téléchargé avec la commande suivante :
# tar -xvzf asterisk-20-current.tar.gz

Ensuite, changez le répertoire vers le répertoire extrait et installez tous les modules MP3 requis avec la commande suivante :
# cd asterisk-17.7.0
# contrib/scripts/get_mp3_source.sh

Ensuite, installez les autres dépendances avec la commande suivante :
# contrib/scripts/install_prereq install

Vous devriez voir la sortie suivante :

#############################################
## install completed successfully
#############################################

Ensuite, configurez l'astérisque avec la commande suivante :

# ./configure

Vous devriez obtenir la sortie suivante :

configure: Menuselect build configuration successfully completed

               .$$$$$$$$$$$$$$$=..      
            .$7$7..          .7$$7:.    
          .$$:.                 ,$7.7   
        .$7.     7$$$$           .$$77  
     ..$$.       $$$$$            .$$$7 
    ..7$   .?.   $$$$$   .?.       7$$$.
   $.$.   .$$$7. $$$$7 .7$$$.      .$$$.
 .777.   .$$$$$$77$$$77$$$$$7.      $$$,
 $$$~      .7$$$$$$$$$$$$$7.       .$$$.
.$$7          .7$$$$$$$7:          ?$$$.
$$$          ?7$$$$$$$$$$I        .$$$7 
$$$       .7$$$$$$$$$$$$$$$$      :$$$. 
$$$       $$$$$$7$$$$$$$$$$$$    .$$$.  
$$$        $$$   7$$$7  .$$$    .$$$.   
$$$$             $$$$7         .$$$.    
7$$$7            7$$$$        7$$$      
 $$$$$                        $$$       
  $$$$7.                       $$  (TM)     
   $$$$$$$.           .7$$$$$$  $$      
     $$$$$$$$$$$$7$$$$$$$$$.$$$$$$      
       $$$$$$$$$$$$$$$$.                

configure: Package configured for: 
configure: OS type  : linux-gnu
configure: Host CPU : x86_64
configure: build-cpu:vendor:os: x86_64 : pc : linux-gnu :
configure: host-cpu:vendor:os: x86_64 : pc : linux-gnu :
Ensuite, exécutez la commande suivante pour sélectionner et installer certains modules recommandés :
# make menuselect
1- configurer Add-ons (see README-addons.txt)
2- Configure AGI samples
3- configure Core sound Packages
4- Configure Music on Hold File Packages

Une fois que vous avez terminé, cliquez sur le bouton Enregistrer et quitter pour enregistrer les modifications et installer tous les addons.

Ensuite, vous devrez créer l'Asterisk. Vous pouvez le faire avec la commande suivante :
# make

Vous devriez voir la sortie suivante :

 +--------- Asterisk Build Complete ---------+
 + Asterisk has successfully been built, and +
 + can be installed by running:              +
 +                                           +
 +                make install               +
 +-------------------------------------------+

 Ensuite, installez Astersik, la  configuration et l'exemple en exécutant la commande suivante :

make install
make samples
make config
ldconfig
Une fois que vous avez terminé, vous pouvez passer à l'étape suivante.

## Créer un utilisateur Astersik (cette option est optionnelle mais c'est la bonne pratique)
--------------------------------

Ensuite, vous devrez créer un utilisateur Asterisk, un groupe et changer la propriété du répertoire de configuration Asterisk.

Commencez par créer un utilisateur et un groupe avec la commande suivante :

# groupadd asterisk
# useradd -r -d /var/lib/asterisk -g asterisk asterisk
Ensuite, ajoutez l'utilisateur audio et dialout au groupe Asterisk en exécutant la commande suivante :

# usermod -aG audio,dialout asterisk
Ensuite, changez le propriétaire du répertoire de configuration d'Asterisk avec la commande suivante :

# chown -R asterisk.asterisk /etc/asterisk
# chown -R asterisk.asterisk /var/{lib,log,spool}/asterisk
# chown -R asterisk.asterisk /usr/lib/asterisk
Une fois que vous avez terminé, vous pouvez passer à l'étape suivante.


##  Configurer l'astérisque
---------------------------
Ensuite, modifiez le fichier /etc/default/asterisk et définissez l'utilisateur par défaut sur Asterisk :
# nano /etc/default/asterisk

Décommentez les lignes suivantes :

AST_USER="asterisk"
AST_GROUP="asterisk"
Enregistrez et fermez le fichier lorsque vous avez terminé, puis modifiez le fichier de configuration par défaut Asterisk et définissez l'exécution en tant qu'utilisateur sur astérisque :

# nano /etc/asterisk/asterisk.conf
Décommentez les lignes suivantes :

runuser = asterisk ; The user to run as.
rungroup = asterisk ; The group to run as.

Enregistrez et fermez le fichier puis démarrez le service Asterisk et activez-le au redémarrage du système avec la commande suivante :

# systemctl restart asterisk
# systemctl enable asterisk
Vous pouvez maintenant vérifier l'état du service Asterisk avec la commande suivante :

# systemctl status asterisk
Vous devriez obtenir la sortie suivante :

? asterisk.service - LSB: Asterisk PBX
     Loaded: loaded (/etc/init.d/asterisk; generated)
     Active: active (running) since Mon 2020-10-19 12:39:41 UTC; 2min 49s ago
       Docs: man:systemd-sysv-generator(8)
    Process: 47946 ExecStart=/etc/init.d/asterisk start (code=exited, status=0/SUCCESS)
      Tasks: 71 (limit: 4691)
     Memory: 41.7M
     CGroup: /system.slice/asterisk.service
             ??47965 /usr/sbin/asterisk -U asterisk -G asterisk

Oct 19 12:39:41 ubunt4 systemd[1]: Starting LSB: Asterisk PBX...
Oct 19 12:39:41 ubunt4 asterisk[47946]:  * Starting Asterisk PBX: asterisk
Oct 19 12:39:41 ubunt4 asterisk[47946]:    ...done.

Ensuite, vérifiez la connexion Asterisk avec la commande suivante :
# asterisk -rvv

Vous devriez obtenir la sortie suivante :

Asterisk 20.8.1, Copyright (C) 1999 - 2022, Sangoma Technologies Corporation and others.
Created by Mark Spencer <markster@digium.com>
Asterisk comes with ABSOLUTELY NO WARRANTY; type 'core show warranty' for details.
This is free software, with components licensed under the GNU General Public
License version 2 and other licenses; you are welcome to redistribute it under
certain conditions. Type 'core show license' for details.
=========================================================================
Running as user 'asterisk'
Running under group 'asterisk'
Connected to Asterisk 20.8.1 currently running on ubuntuserver16 (pid = 608)
Unable to read or write history file '/root/.asterisk_history'
ubuntuserver16*CLI>

## CONFIGURATION ET CONTROL TEL IP 
----------------------------------
Desormais, toutes les configuration d'asterisk se trouve dans /etc/asterisk, mais les configuration principale qui nous interesse sont: cdr.conf, confbridge.conf, extensions.conf, meetme.conf, users.conf, voicemail.conf, sip.conf, moh.conf, features.conf

1- configuration des utilisateurs
---------------------------------
Pour la configuration des utilisateurs voip dans asterisk, on va editer /etc/asterisk/users.conf
# nano /etc/asterisk/users.conf
ajoutez y :

[default_template](!)
hasvoicemail = yes    ; peut avoir de messagerie vocale
hassip = yes          ; peut avoir les protocoles sip
hasiax = no           : pas de protocol de communication iax
hash323 = no
canpark = yes         ; peut mettre les appels dans un parking
transfer = yes        ; peut transferer les appels
callwaiting = yes     ; peut avoir une attente en cas de non reponse
cancallforward = yes
callreturn = yes
callgroup = 1         ; peut faire des appels de groupe
pickupgroup = 1
nat = never           ; peut etre derière une addresse ip privée
disallow = all
allow = ulaw

[6002](default_template)
fullname = nom complet
username = surnom
email = mon.addresse.email@gmail.com
mailbox = 6002      ; numero de boite mail vocale
vm_secret = 2623      ; mot de passe pour le boite mail vocale
context = etudiant    ; context auquel l'utilisateur appartient

2- configuration de boite mail vocal
------------------------------------
Veuillez bien verifier les configuration géral dans le context [general] s'il correspond à votre nécessité
on peut ajouter dans voicemail notre contexte et les utilisateurs qui y sont liées

[etudiant]
6002 => 2623, jlady  
6001 => 2479, rtoky, raphaeltokinandrasana@gmail.com

pour la sauvegarde de ces configurations
# asterisk --rvv
> reload

3- Configuration du DialPlan
----------------------------
# BUT DU DIAL PLAN
------------------
Passon à présent au coeur d'Asterisk: le Dial plan.
Le DialPlan est ce qui va définir le routage des appels à travers le serveur.
La configuration du DialPlan est contenue dans le fichier suivant: /etc/asterisk/extensions.conf

# nano /etc/asterisk/extensions.conf
Dans ce fichier, nous devrons définir le comportement d'Asterisk vis-à-vi des appels.
Ajouter y la configuration suivant(en se basant sur les exemples précedents)
[etudiant]
exten => _60[0-9]X, 1, Dial(SIP/${EXTEN},30)
exten => _60[0-9]X, 2, Voicemail(${EXTEN}@etudiant_vm)

exten => 6100, 1, Answer()
exten => 6100, 2, VoiceMailMain(${CALLERID(num)}@etudiant_vm)

# Les numéros
-------------
+ X : correspond aux chiffres de 0 à 9
+ Z : correspond aux nombres de 1 à 9
+ N : correspond aux nombres de 2 à 9
+ . : correspond à un ou plusieurs chiffres
+ ! : correspond à séro ou plusieurs chiffres

+ [a-b] : correspond aux nombres de a inclut à b inclut
+ [abc] : correspond exactement à a ou b ou c

# Les Applications
------------------
+ Answer() : permet de décroche l'appel
+ HangUp() : permet de raccrocher l'appel
+ Dial(type/identifier, timeout) : permet de composer un numéro, avec un timeout en cas de con-réponse
+ VoiceMail(user@context) : permet de joindre la messagerie de l'utilisateur spécifié
+ VoiceMailMain(user@context) : permet de consulter la messagerie de l'utilisateur spécifié
+ Playback(sound-file) : permet de jouer un son
+ SetMusicOnHold(class) : permet de jouer un son
+ Goto(contexte, extension, priorité): permet de se rendre à un contexte précis, à une certaine extension, à une certaine priorité

# Les variables
---------------
+ ${EXTEN} : Renvoie l'extension actuellement appelée
+ ${CONTEXT} : Renvoie le contexte actuel
+ ${CALLERID(name)} ! Renvoie le nom de la personne qui appel
+ ${CALLERID(num)} : Renvoie le numéro de la personne qui appel
+ ${DATETIME} : Renvoie la date actuelle au format DDMMYYYY-HH:MM:SS
+ ${PRIORITY} : Renvoie la priorité actuelle de l'extension


#  CONFIGURATION DE SIP ET DE SOFTPHONE
---------------------------------------
Tout d'abord, il faut configurer pjsip.conf(pour asterisk 20) ou sip.conf (pour asterisk<20), ajouter y la configuration suivante:
[transport-udp]
type = transport
protocol = udp
bind = 0.0.0.0

[6001]
type = endpoint
context = etudiant
disallow = all
allow = ulaw
auth = auth6001
aors = 6001

[auth6001]
type = auth
auth_type = userpass
password = 2479
username = 6001

[6001]
type = aor
max_contacts = 1

[6002]
type = endpoint
context = etudiant
disallow = all
allow = ulaw
auth = auth6002
aors = 6002

[auth6002]
type = auth
auth_type = userpass
password = 2623
username = 6002

[6002]
type = aor
max_contacts = 1

Ces utilisateurs sont les meme qui sont configurer dans users.conf
puis , reload pjsip
# asterisk -rvvv
>pjsip reload
>pjsip show endpoints
