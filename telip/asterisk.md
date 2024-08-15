# Configuration de VoIP avec Asterisk

## 1. Mise à jour des Packages

Mettez à jour vos packages système avec la commande suivante :
```bash
sudo apt-get update -y
```

## 2. Installation des Dépendances

Installez les dépendances nécessaires pour Asterisk :
```bash
sudo apt-get install -y gnupg2 software-properties-common git curl wget libnewt-dev libssl-dev libncurses5-dev subversion libsqlite3-dev build-essential libjansson-dev libxml2-dev uuid-dev
```

## 3. Installation d'Asterisk

### 3.1 Téléchargement et Extraction

Téléchargez la dernière version d'Asterisk :
```bash
wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-17-current.tar.gz
```

Extrayez le fichier téléchargé :
```bash
tar -xvzf asterisk-17-current.tar.gz
```

### 3.2 Compilation et Installation

Changez de répertoire et installez les modules MP3 requis :
```bash
cd asterisk-17.7.0
contrib/scripts/get_mp3_source.sh
```

Installez les autres dépendances nécessaires :
```bash
contrib/scripts/install_prereq install
```

Configurez Asterisk :
```bash
./configure
```

Sélectionnez et installez les modules recommandés :
```bash
make menuselect
```
- Configurer Add-ons
- Configurer AGI samples
- Configurer Core sound Packages
- Configurer Music on Hold File Packages

Compilez Asterisk :
```bash
make
```

Installez Asterisk, les fichiers d'exemple et la configuration :
```bash
sudo make install
sudo make samples
sudo make config
sudo ldconfig
```

## 4. Création d'un Utilisateur Asterisk (Optionnel mais Recommandé)

Créez un utilisateur et un groupe pour Asterisk :
```bash
sudo groupadd asterisk
sudo useradd -r -d /var/lib/asterisk -g asterisk asterisk
```

Ajoutez l'utilisateur `asterisk` aux groupes `audio` et `dialout` :
```bash
sudo usermod -aG audio,dialout asterisk
```

Changez le propriétaire des répertoires d'Asterisk :
```bash
sudo chown -R asterisk:asterisk /etc/asterisk
sudo chown -R asterisk:asterisk /var/{lib,log,spool}/asterisk
sudo chown -R asterisk:asterisk /usr/lib/asterisk
```

## 5. Configuration d'Asterisk

### 5.1 Modifier les Fichiers de Configuration

Définissez l'utilisateur par défaut dans `/etc/default/asterisk` :
```bash
sudo nano /etc/default/asterisk
```
Décommentez les lignes suivantes :
```ini
AST_USER="asterisk"
AST_GROUP="asterisk"
```

Modifiez le fichier de configuration d'Asterisk `/etc/asterisk/asterisk.conf` :
```bash
sudo nano /etc/asterisk/asterisk.conf
```
Décommentez les lignes suivantes :
```ini
runuser = asterisk
rungroup = asterisk
```

### 5.2 Démarrer et Activer le Service

Démarrez le service Asterisk et activez-le au démarrage :
```bash
sudo systemctl restart asterisk
sudo systemctl enable asterisk
```

Vérifiez l'état du service :
```bash
sudo systemctl status asterisk
```

### 5.3 Connexion à Asterisk

Vérifiez la connexion avec la commande suivante :
```bash
sudo asterisk -rvv
```

## 6. Configuration et Gestion des Extensions

Les configurations principales se trouvent dans `/etc/asterisk`, notamment :
- `cdr.conf`
- `confbridge.conf`
- `extensions.conf`
- `meetme.conf`
- `users.conf`
- `voicemail.conf`
- `sip.conf`
- `moh.conf`
- `features.conf`

### 6.1 Configuration des Utilisateurs

Éditez le fichier `/etc/asterisk/users.conf` :
```bash
sudo nano /etc/asterisk/users.conf
```
Ajoutez les configurations suivantes :
```ini
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

### 6.2 Configuration de la Messagerie Vocale

Éditez le fichier `/etc/asterisk/voicemail.conf` :
```bash
sudo nano /etc/asterisk/voicemail.conf
```
Assurez-vous que le contexte `[etudiant]` contient :
```ini
[etudiant]
6002 => 2623, jlady
6001 => 2479, rtoky, raphaeltokinandrasana@gmail.com
```

Rechargez la configuration d'Asterisk :
```bash
sudo asterisk -rvv
> reload
```

### 6.3 Configuration du Dial Plan

Éditez le fichier `/etc/asterisk/extensions.conf` :
```bash
sudo nano /etc/asterisk/extensions.conf
```
Ajoutez les configurations suivantes :
```ini
[etudiant]
exten => _60[0-9]X,1,Dial(SIP/${EXTEN},30)
exten => _60[0-9]X,2,Voicemail(${EXTEN}@etudiant_vm)

exten => 6100,1,Answer()
exten => 6100,2,VoiceMailMain(${CALLERID(num)}@etudiant_vm)
```

### 6.4 Explication des Variables et Applications

**Variables :**
- `${EXTEN}` : Extension appelée
- `${CONTEXT}` : Contexte actuel
- `${CALLERID(name)}` : Nom de l'appelant
- `${CALLERID(num)}` : Numéro de l'appelant
- `${DATETIME}` : Date et heure actuelles
- `${PRIORITY}` : Priorité actuelle de l'extension

**Applications :**
- `Answer()` : Répond à l'appel
- `HangUp()` : Raccroche l'appel
- `Dial(type/identifier, timeout)` : Compose un numéro avec un délai
- `VoiceMail(user@context)` : Accède à la messagerie vocale de l'utilisateur
- `VoiceMailMain(user@context)` : Consulte la messagerie vocale de l'utilisateur
- `Playback(sound-file)` : Joue un fichier sonore
- `SetMusicOnHold(class)` : Joue de la musique en attente
- `Goto(context, extension, priority)` : Passe à un contexte, une extension, une priorité spécifiques

---


### Configuration SIP pour Asterisk

#### Fichier `pjsip.conf` (pour Asterisk 20) ou `sip.conf` (pour Asterisk < 20)

**1. Configuration Générale**

```plaintext
[general]
; Général Configuration
bindaddr=0.0.0.0
bindport=5060
srvlookup=no
nat=never
disallow=all
allow=ulaw
allow=alaw
allow=gsm
```

- `bindaddr=0.0.0.0`: Spécifie que le serveur SIP doit écouter sur toutes les interfaces réseau disponibles.
- `bindport=5060`: Définit le port sur lequel le serveur SIP écoute, 5060 étant le port standard pour SIP.
- `srvlookup=no`: Désactive la recherche DNS SRV pour la résolution des adresses des serveurs SIP.
- `nat=never`: Indique que le serveur SIP ne doit pas modifier les adresses IP des paquets SIP, utile dans les environnements NAT (Network Address Translation).
- `disallow=all`: Refuse tous les codecs par défaut.
- `allow=ulaw`, `allow=alaw`, `allow=gsm`: Permet les codecs `ulaw` (G.711 mu-law), `alaw` (G.711 A-law), et `gsm` pour les appels.

**2. Templates de Configuration**

Les templates permettent de définir des configurations réutilisables pour les utilisateurs et les classes.

```plaintext
; Template utilisateur
[template-user](!)
type=endpoint
context=etudiant
disallow=all
allow=ulaw
language=fr
call_group=1
pickup_group=1
```

- `type=endpoint`: Définit le type de cette configuration comme un point de terminaison SIP.
- `context=etudiant`: Spécifie le contexte dans le plan de numérotation pour cet utilisateur.
- `disallow=all` et `allow=ulaw`: Permet uniquement le codec `ulaw` pour cet utilisateur.
- `language=fr`: Définit la langue par défaut pour les messages vocaux en français.
- `call_group=1` et `pickup_group=1`: Configure des groupes pour les appels et les prises d'appels.

Les templates pour les classes L1, L2, et L3 héritent du template `template-user` et définissent des contextes et des authentifications spécifiques :

```plaintext
; Template pour la classe L1
[template-L1](!,template-user)
context=L1_class
auth=L1_class_auth
```

**3. Authentification**

Les templates d'authentification définissent les informations d'identification pour les utilisateurs :

```plaintext
[template-auth](!)
type=auth
auth_type=userpass
```

- `auth_type=userpass`: Spécifie que l'authentification se fait par nom d'utilisateur et mot de passe.

**4. Adresses de Ressources (AOR)**

Les templates d'AOR (Address of Record) définissent les adresses pour les points de terminaison :

```plaintext
[template-aor](!)
type=aor
```

**5. Transport**

Définit le transport UDP pour la communication SIP :

```plaintext
[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:5060
```

- `protocol=udp`: Spécifie que le transport utilise UDP.
- `bind=0.0.0.0:5060`: Lie le transport UDP à toutes les interfaces sur le port 5060.

### Configuration des Utilisateurs

Les utilisateurs sont configurés en utilisant les templates définis précédemment et spécifient les informations d'authentification et les adresses :

```plaintext
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
```

- `auth=6001_auth`: Associe l'utilisateur à un template d'authentification spécifique.
- `aors=6001`: Associe l'utilisateur à un template AOR.
- `context=delegue`: Définit le contexte pour cet utilisateur.

### Configuration des Extensions

**Contexte [etudiant]**

```plaintext
[etudiant]
include => ivr_class_password

exten => _60XX,1,Dial(PJSIP/${EXTEN},20)
exten => _60XX,2,Voicemail(${EXTEN}@default)
exten => _60XX,3,Hangup()
```

- `Dial(PJSIP/${EXTEN},20)`: Compose l'extension spécifiée avec un délai de 20 secondes.
- `Voicemail(${EXTEN}@default)`: Dirige les appels vers la messagerie vocale si l'appel est manqué.

**Contexte [ivr_class_password]**

Gère les appels entrants en demandant un mot de passe pour accéder aux emplois du temps :

```plaintext
exten => 9001,1,Set(CHANNEL(language)=fr)
exten => 9001,2,Answer()
exten => 9001,3,agi(googletts.agi,"Veuillez saisir le mot de passe de votre classe.",fr)
exten => 9001,4,Read(CLASS_PASS,beep,5) 
exten => 9001,5,NoOp(Mot de passe saisi: ${CLASS_PASS})
```

- `agi(googletts.agi,"...")`: Utilise un AGI (Asterisk Gateway Interface) pour synthétiser la parole avec Google TTS.
- `Read(CLASS_PASS,beep,5)`: Lit le mot de passe saisi par l'utilisateur.

**Contexte [class_menu]**

Permet la consultation des emplois du temps en fonction de la classe :

```plaintext
exten => L1,1,Set(FILE_PATH=/var/lib/asterisk/sounds/custom/emploi_du_temps_L1.ulaw)
exten => L1,n,ExecIf($[${STAT(e,${FILE_PATH})}]?Playback(custom/emploi_du_temps_L1):agi(googletts.agi,"Vous n'avez pas encore d'emploi du temps enregistré pour la classe L1.",fr))
```

- `Set(FILE_PATH=...)`: Définit le chemin du fichier pour l'emploi du temps.
- `ExecIf($[${STAT(e,${FILE_PATH})}]?Playback(...))`: Vérifie si le fichier existe et le lit, sinon, informe l'utilisateur.

**Contexte [delegue]**

Gère les actions des délégués :

```plaintext
exten => 8888,1,Answer()
exten => 8888,2,agi(googletts.agi,"Pour la gestion de votre classe, veuillez taper 1 pour changer le mot de passe ou taper 2 pour enregistrer le nouveau emploi du temps de votre classe",fr)
exten => 8888,3,WaitExten(20)
```

- `agi(googletts.agi,"...")`: Fournit des instructions pour la gestion de la classe.
- `WaitExten(20)`: Attend que l'utilisateur saisisse une extension.

**Contexte [credential]**

Permet de changer le mot de passe de la classe :

```plaintext
exten => 700,1,Answer()
exten => 700,2,agi(googletts.agi,"Veuillez entrer le nouveau mot de passe de votre classe",fr)
exten => 700,3,Read(NEW_PASSWORD,,5)
```

- `Read(NEW_PASSWORD,,5)`: Lit le nouveau mot de passe saisi par l'utilisateur.
- `agi(update_password.py,${CALLERID(num)},${NEW_PASSWORD})`: Exécute un script Python pour mettre à jour le mot de passe.

**Contexte [emploi_du_temps]**

Permet d'enregistrer les emplois du temps :

```plaintext
exten => 1000,1,Answer()
exten => 1000,2,agi(getuserclass.py,${CALLERID(num)})
exten => 1000,3,agi(googletts.agi,"Enregistrement de l'emploi du temps pour la classe ${USER_CLASS}.",fr)
```

- `agi(getuserclass.py,${CALLERID(num)})`: Exécute un script Python pour obtenir la classe de l'utilisateur.
- `Record(${RECORD_FILE}.ulaw)`: Enregistre l'emploi du temps dans un fichier audio.

**Contexte [admission]**

Gère les demandes d'admission :

```plaintext
exten => 5020,1,Set(CHANNEL(language)=fr)
exten => 5020,2,agi(googletts.agi,"Bonjour, veuillez saisir la touche 1 pour le service d'orientation et le touche 2 pour le service d'inscription",fr)
```

- `agi(googletts.agi,"...")`: Fournit des instructions pour sélectionner le service d'orientation ou d'inscription.

**Contexte [orientation]**

Dirige les appels vers les services d'orientation selon le cycle :

```plaintext
exten => 1,1,Dial(PJSIP/5016,20)
exten => 1,2,Dial(PJSIP/5017,20)
exten => 2,1,Dial(PJSIP/5011&PJSIP

/5012,20)
```

- `Dial(PJSIP/5016,20)`: Compose les extensions de l'orientation.

**Contexte [inscription]**

Gère les appels pour l'inscription :

```plaintext
exten => 101,1,Dial(PJSIP/5021,20)
exten => 102,1,Dial(PJSIP/5022,20)
```

- `Dial(PJSIP/5021,20)`: Compose les extensions pour l'inscription.
