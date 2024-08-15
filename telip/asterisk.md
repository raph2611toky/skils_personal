```markdown
# ############################################################################### #
#                                                                                 #
#                      CONFIGURATION DE VOIP AVEC ASTERISK                        #
#                                                                                 #
# ############################################################################### #

## Mise à jour des packages système

Tout d'abord, mettez à jour vos packages système vers la dernière version :

```bash
sudo apt-get update -y
```

## Installation des dépendances requises

Installez les dépendances nécessaires pour Asterisk :

```bash
sudo apt-get install gnupg2 software-properties-common git curl wget \
libnewt-dev libssl-dev libncurses5-dev subversion libsqlite3-dev \
build-essential libjansson-dev libxml2-dev uuid-dev -y
```

## Installation d'Asterisk

La dernière version d'Asterisk n'est pas disponible dans les référentiels par défaut d'Ubuntu 20.04. Vous devrez donc le télécharger et le compiler à partir de la source.

1. Téléchargez la dernière version d'Asterisk :

    ```bash
    wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-17-current.tar.gz
    ```

2. Extrayez le fichier téléchargé :

    ```bash
    tar -xvzf asterisk-17-current.tar.gz
    ```

3. Changez le répertoire vers le répertoire extrait :

    ```bash
    cd asterisk-17.7.0
    ```

4. Installez les modules MP3 requis :

    ```bash
    contrib/scripts/get_mp3_source.sh
    ```

5. Installez les autres dépendances :

    ```bash
    contrib/scripts/install_prereq install
    ```

    Vous devriez voir :

    ```
    #############################################
    ## install completed successfully
    #############################################
    ```

6. Configurez Asterisk :

    ```bash
    ./configure
    ```

    Vous devriez obtenir :

    ```
    configure: Menuselect build configuration successfully completed
    ```

7. Sélectionnez et installez les modules recommandés :

    ```bash
    make menuselect
    ```

    Configurez les options suivantes :
    - Add-ons
    - AGI samples
    - Core sound Packages
    - Music on Hold File Packages

    Enregistrez et quittez.

8. Compilez Asterisk :

    ```bash
    make
    ```

    Vous devriez voir :

    ```
    +--------- Asterisk Build Complete ---------+
    + Asterisk has successfully been built, and +
    + can be installed by running:              +
    +                                           +
    +                make install               +
    +-------------------------------------------+
    ```

9. Installez Asterisk et les fichiers de configuration :

    ```bash
    sudo make install
    sudo make samples
    sudo make config
    sudo ldconfig
    ```

## Création d'un utilisateur Asterisk (optionnel mais recommandé)

Créez un utilisateur et un groupe pour Asterisk :

```bash
sudo groupadd asterisk
sudo useradd -r -d /var/lib/asterisk -g asterisk asterisk
```

Ajoutez les utilisateurs `audio` et `dialout` au groupe Asterisk :

```bash
sudo usermod -aG audio,dialout asterisk
```

Changez la propriété des répertoires de configuration Asterisk :

```bash
sudo chown -R asterisk:asterisk /etc/asterisk
sudo chown -R asterisk:asterisk /var/{lib,log,spool}/asterisk
sudo chown -R asterisk:asterisk /usr/lib/asterisk
```

## Configuration d'Asterisk

1. Modifiez le fichier `/etc/default/asterisk` pour définir l'utilisateur par défaut sur Asterisk :

    ```bash
    sudo nano /etc/default/asterisk
    ```

    Décommentez les lignes suivantes :

    ```plaintext
    AST_USER="asterisk"
    AST_GROUP="asterisk"
    ```

2. Modifiez le fichier de configuration par défaut d'Asterisk :

    ```bash
    sudo nano /etc/asterisk/asterisk.conf
    ```

    Décommentez les lignes suivantes :

    ```plaintext
    runuser = asterisk ; The user to run as.
    rungroup = asterisk ; The group to run as.
    ```

3. Redémarrez et activez le service Asterisk au démarrage :

    ```bash
    sudo systemctl restart asterisk
    sudo systemctl enable asterisk
    ```

4. Vérifiez l'état du service Asterisk :

    ```bash
    sudo systemctl status asterisk
    ```

    Vous devriez obtenir :

    ```plaintext
    ? asterisk.service - LSB: Asterisk PBX
         Loaded: loaded (/etc/init.d/asterisk; generated)
         Active: active (running) since Mon 2020-10-19 12:39:41 UTC; 2min 49s ago
           Docs: man:systemd-sysv-generator(8)
        Process: 47946 ExecStart=/etc/init.d/asterisk start (code=exited, status=0/SUCCESS)
          Tasks: 71 (limit: 4691)
         Memory: 41.7M
         CGroup: /system.slice/asterisk.service
                 ??47965 /usr/sbin/asterisk -U asterisk -G asterisk
    ```

5. Vérifiez la connexion à Asterisk :

    ```bash
    sudo asterisk -rvv
    ```

    Vous devriez voir :

    ```plaintext
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
    ```

## Configuration et contrôle IP

Les configurations d'Asterisk se trouvent dans `/etc/asterisk`. Les fichiers principaux à configurer sont :
- `cdr.conf`
- `confbridge.conf`
- `extensions.conf`
- `meetme.conf`
- `users.conf`
- `voicemail.conf`
- `sip.conf`
- `moh.conf`
- `features.conf`

### 1. Configuration des utilisateurs

Pour configurer les utilisateurs VoIP dans Asterisk, éditez le fichier `/etc/asterisk/users.conf` :

```bash
sudo nano /etc/asterisk/users.conf
```

Ajoutez les configurations suivantes :

```plaintext
[default_template](!)
hasvoicemail = yes
hassip = yes
hasiax = no
hash323 = no
canpark = yes
transfer = yes
callwaiting = yes
cancallforward = yes
callreturn = yes
callgroup = 1
pickupgroup = 1
nat = never
disallow = all
allow = ulaw

[6002](default_template)
fullname = nom complet
username = surnom
email = mon.addresse.email@gmail.com
mailbox = 6002
vm_secret = 2623
context = etudiant
```

### 2. Configuration de la boîte vocale

Vérifiez les paramètres généraux dans le contexte `[general]`. Ajoutez les configurations suivantes pour les utilisateurs dans `voicemail.conf` :

```plaintext
[etudiant]
6002 => 2623, jlady
6001 => 2479, rtoky, raphaeltokinandrasana@gmail.com
```

Sauvegardez et rechargez les configurations :

```bash
sudo asterisk -rvv
> reload
```

### 3. Configuration du DialPlan

Le DialPlan définit le routage des appels. Modifiez le fichier `/etc/asterisk/extensions.conf` :

```bash
sudo nano /etc/asterisk/extensions.conf
```

Ajoutez la configuration suivante :

```plaintext
[etudiant]
exten => _60[0-9]X,1,Dial(SIP/${EXTEN},30)
exten => _60[0-9]X,2,Voicemail(${EXTEN}@etudiant_vm)

exten => 6100,1,Answer()
exten => 6100,2,VoiceMailMain(${CALLERID(num)}@etudiant_vm)
```

### Notes sur les expressions et les applications

**Les numéros :**
- `X` : chiffre de 0 à 9
- `Z` : chiffre de 1 à 9
- `N` : chiffre de 2 à 9
- `.` : un ou plusieurs chiffres
- `!` : zéro ou plusieurs chiffres
- `[a-b]` : chiffre de a à b
- `[abc]` : a, b ou c

**Les applications :**
- `Answer()`: décroche l'appel
- `HangUp()`: raccroche l'appel
- `Dial(type/identifier, timeout)`: compose un numéro avec un timeout
- `

Voici le fichier `pjsip.conf` et le `extensions.conf` configurés pour votre scénario, avec une organisation et une mise en forme plus claire :

### pjsip.conf

```ini
# CONFIGURATION DE SIP ET DE SOFTPHONE
---------------------------------------
; Général Configuration
[general]
bindaddr=0.0.0.0
bindport=5060
srvlookup=no
nat=never
disallow=all
allow=ulaw
allow=alaw
allow=gsm

;========================== TEMPLATES CONFIGURATIONS ============================

; Template utilisateur
[template-user](!)
type=endpoint
context=etudiant
disallow=all
allow=ulaw
language=fr
call_group=1
pickup_group=1

; Template pour la classe L1
[template-L1](!,template-user)
context=L1_class
auth=L1_class_auth

; Template pour la classe L2
[template-L2](!,template-user)
context=L2_class
auth=L2_class_auth

; Template pour la classe L3
[template-L3](!,template-user)
context=L3_class
auth=L3_class_auth

[template-auth](!)
type=auth
auth_type=userpass

[template-aor](!)
type=aor

[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:5060

;========================= CLASS AUTHENTICATION ===========================

[L1_class_auth](template-auth)
password=1111
username=l1

[L2_class_auth](template-auth)
password=2222
username=l2

[L3_class_auth](template-auth)
password=4712
username=l3

;========================= USERS CONFIGURATIONS ===========================
;------------------------ exercie 02 ---------------------------
; Utilisateur 6001
[6001](template-L1)
auth=6001_auth
aors=6001
transport=transport-udp
context=delegue

[6001_auth](template-auth)
username=6001
password=1234

[6001](template-aor)
max_contacts=10

; Utilisateur 6002
[6002](template-L1)
auth=6002_auth
aors=6002
transport=transport-udp
context=etudiant

[6002_auth](template-auth)
username=6002
password=2345

[6002](template-aor)
max_contacts=10

; Utilisateur 6003
[6003](template-L2)
auth=6003_auth
aors=6003
transport=transport-udp
context=delegue

[6003_auth](template-auth)
username=6003
password=1234

[6003](template-aor)
max_contacts=10

; Utilisateur 6004
[6004](template-L3)
auth=6004_auth
aors=6004
transport=transport-udp
context=delegue

[6004_auth](template-auth)
username=6004
password=1234

[6004](template-aor)
max_contacts=10
```

### extensions.conf

```ini
; Extensions Configuration
;=========================
[etudiant]
include => ivr_class_password

exten => _60XX,1,Dial(PJSIP/${EXTEN},20)
exten => _60XX,2,Voicemail(${EXTEN}@default)
exten => _60XX,3,Hangup()

exten => 5020,1,Goto(admission,5020,1)

exten => 6100,1,Answer()
exten => 6100,2,VoiceMailMain(${CALLERID(num)}@default)
exten => 6100,3,Hangup()

;=================== IVR CLASS EMPLOI DU TEMPS ==================
[ivr_class_password]

exten => 9001,1,Set(CHANNEL(language)=fr)
exten => 9001,2,Answer()
exten => 9001,3,agi(googletts.agi,"Veuillez saisir le mot de passe de votre classe.",fr)
exten => 9001,4,Read(CLASS_PASS,beep,5)
exten => 9001,5,NoOp(Mot de passe saisi: ${CLASS_PASS})
exten => 9001,6,Wait(1)
exten => 9001,n,GotoIf($["${CLASS_PASS}" = ""]?t,1)
exten => 9001,n,agi(check_password.py,${CALLERID(num)},${CLASS_PASS})
exten => 9001,n,NoOp(CLASS_AUTH_RESULT: ${CLASS_AUTH_RESULT}, CLASS_NAME: ${CLASS_NAME})
exten => 9001,n,GotoIf($["${CLASS_AUTH_RESULT}" = "valid"]?class_menu,${CLASS_NAME},1)
exten => 9001,n,Goto(ivr_class_password,i,1)

exten => i,1,Goto(class_menu,i,1)
exten => t,1,Goto(ivr_class_password,9001,3)

[class_menu]

exten => L1,1,Set(FILE_PATH=/var/lib/asterisk/sounds/custom/emploi_du_temps_L1.ulaw)
exten => L1,n,ExecIf($[${STAT(e,${FILE_PATH})}]?Playback(custom/emploi_du_temps_L1):agi(googletts.agi,"Vous n'avez pas encore d'emploi du temps enregistré pour la classe L1.",fr))
exten => L1,n,Hangup()

exten => L2,1,Set(FILE_PATH=/var/lib/asterisk/sounds/custom/emploi_du_temps_L2.ulaw)
exten => L2,n,ExecIf($[${STAT(e,${FILE_PATH})}]?Playback(custom/emploi_du_temps_L2):agi(googletts.agi,"Vous n'avez pas encore d'emploi du temps enregistré pour la classe L2.",fr))
exten => L2,n,Hangup()

exten => L3,1,Set(FILE_PATH=/var/lib/asterisk/sounds/custom/emploi_du_temps_L3.ulaw)
exten => L3,n,ExecIf($[${STAT(e,${FILE_PATH})}]?Playback(custom/emploi_du_temps_L3):agi(googletts.agi,"Vous n'avez pas encore d'emploi du temps enregistré pour la classe L3.",fr))
exten => L3,n,Hangup()

exten => i,1,agi(googletts.agi,"Le mot de passe que vous avez saisi est incorrect. Tapez 1 pour réessayer ou 2 pour terminer.",fr)
exten => i,2,WaitExten(20)
exten => 1,1,Goto(ivr_class_password,9001,1)
exten => 2,1,agi(googletts.agi,"Au revoir, merci de nous avoir contacté.",fr)
exten => 2,n,Hangup()
exten => t,1,Goto(i,1)

;------------------------- delegue gestionnaire -----------------------

[delegue]
include => etudiant

exten => 8888,1,Answer()
exten => 8888,2,agi(googletts.agi,"Pour la gestion de votre classe, veuillez taper 1 pour changer le mot de passe ou taper 2 pour enregistrer le nouveau emploi du temps de votre classe",fr)
exten => 8888,3,WaitExten(20)

exten => 1,1,Goto(credential,700,1)
exten => 2,1,Goto(emploi_du_temps,1000,1)

exten => i,1,Goto(8888,2)
exten => t,1,Goto(8888,2)

[credential]
exten => 700,1,Answer()
exten => 700,2,agi(googletts.agi,"Veuillez entrer le nouveau mot de passe de votre classe",fr)
exten => 700,3,Read(NEW_PASSWORD,,5)
exten => 700,4,Wait(1)
exten => 700,5,agi(googletts.agi,"Re entrer le mot de passe",fr)
exten => 700,6,Read(CONFIRM_PASSWORD,,5)
exten => 700,7,Wait(1)
exten => 700,8,GotoIf($["${NEW_PASSWORD}" != "${CONFIRM_PASSWORD}"]?i,1)
exten => 700,9,agi(update_password.py,${CALLERID(num)},${NEW_PASSWORD})
exten => 700,n,agi(googletts.agi,"Le mot de passe de votre classe a bien été changé, merci de consulter notre service",fr)
exten => 700,n,Hangup()

exten => i,1,agi(googletts.agi, "Les mots de passe que vous avez fournie ne sont pas identiques",fr)
exten => i,2,Goto(credential,700,2)

exten => t,1,Goto(700,2)

[emploi_du_temps]
exten => 1000,1,Answer()
exten => 1000,2,agi(getuserclass.py,${CALLERID(num)})
exten => 1000,3,agi(googletts.agi,"Enregistrement de l'emploi du temps pour la classe ${USER_CLASS}.",fr)
exten => 1000,4,Set(RECORD_FILE=/var/lib/asterisk/sounds/custom/emploi_du_temps_${USER_CLASS})
exten => 1000,5,Record(${RECORD_FILE}.ulaw)
exten => 