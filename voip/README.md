
---

# Configuration Basique d’Asterisk

Pour débuter avec la configuration de votre serveur Asterisk, nous allons aborder les étapes suivantes : création des utilisateurs, configuration du DialPlan pour permettre les appels, et la gestion des messages vocaux. À la fin de ce guide, vous disposerez d'un système de base opérationnel.

## 1. Administration d’Asterisk

### Console

La console d’Asterisk permet de surveiller et de déboguer le serveur. Vous pouvez également redémarrer Asterisk et charger des modules à partir de cette interface.

Pour lancer la console, utilisez la commande :
```bash
asterisk -r
```
Vous pouvez ajouter l'option `-v` pour un mode verbeux, offrant plus de détails sur les actions :
```bash
asterisk -rv
```
Augmentez le niveau de verbosité en ajoutant plusieurs `v` :
```bash
asterisk -rvv
```

### Fichiers de Configuration

Les fichiers de configuration se trouvent dans le répertoire `/etc/asterisk/`. Après toute modification, redémarrez Asterisk ou rechargez les modules concernés avec :
```bash
asterisk -rv
reload
```

## 2. Création d’Utilisateurs

Les utilisateurs sont configurés dans le fichier `users.conf` situé dans `/etc/asterisk/`. Avant d’éditer, vous pouvez vider le fichier avec :
```bash
echo "" > users.conf
```

Définissez les utilisateurs en utilisant un modèle (Template) pour simplifier la gestion :

```ini
[default_template](!)
type=friend
host=dynamic
dtmfmode=rfc2833
disallow=all
allow=ulaw
nat=never
hassip=yes
hasiax=no
callwaiting=yes
transfer=yes
canpark=yes
hasvoicemail=yes
deny=0.0.0.0/0.0.0.0
permit=192.168.1.0/255.255.255.0
qualify=yes
```

Créez les utilisateurs en vous basant sur ce modèle :

```ini
[100](default_template)
fullname = Marc Aubert
username = maubert
secret = password
mailbox = 100
context = dept_1

[101](default_template)
fullname = Alain Aldric
username = aaldric
secret = password
mailbox = 101
context = dept_1

[200](default_template)
fullname = Leon Morgan
username = lmorgan
secret = password
mailbox = 200
context = dept_2
```

Après modification, redémarrez Asterisk pour appliquer les changements :
```bash
asterisk -rvv
reload
```

## 3. Configuration des Voicemails

Les voicemails permettent aux utilisateurs de laisser des messages lorsqu'ils sont absents. Les utilisateurs accèdent à leur messagerie en composant un numéro et en entrant un mot de passe.

Éditez le fichier `voicemail.conf` avec :
```bash
nano /etc/asterisk/voicemail.conf
```
Videz le fichier si nécessaire :
```bash
echo "" > voicemail.conf
```

Configurez les paramètres généraux et les boîtes vocales des utilisateurs :

```ini
[general]
maxmsg=100
maxsecs=0
minsecs=2
maxlogins=3
review=no
saycid=no

[dept_1_vm]
100 => 1234, Marc Aubert
101 => 1234, Alain Aldric

[dept_2_vm]
200 => 1234, Leon Morgan
```

Redémarrez Asterisk ou rechargez la configuration des voicemails :
```bash
asterisk -rv
reload
```
ou
```bash
asterisk -rv
voicemail reload
```

## 4. Le DialPlan

Le DialPlan définit le routage des appels à travers le serveur. Configurez-le dans le fichier `/etc/asterisk/extensions.conf`.

Exemple de configuration pour les contextes `dept_1` et `dept_2` :

```ini
[dept_1]
exten => _1[0-8]X,1,Dial(SIP/${EXTEN},30)
exten => _1[0-8]X,2,Voicemail(${EXTEN}@dept_1_vm)

[dept_2]
exten => _2[0-8]X,1,Dial(SIP/${EXTEN},30)
exten => _2[0-8]X,2,Voicemail(${EXTEN}@dept_2_vm)
```

## 5. Les Contextes

Les contextes organisent les règles du DialPlan. Chaque utilisateur appartient à un contexte défini dans `users.conf`. Asterisk recherche les actions à effectuer dans le contexte associé.

Voici des exemples de contextes :

```ini
[dept_1]
exten => _1[0-8]X,1,Dial(SIP/${EXTEN},30)
exten => _1[0-8]X,2,Voicemail(${EXTEN}@dept_1_vm)

[dept_2]
exten => _2[0-8]X,1,Dial(SIP/${EXTEN},30)
exten => _2[0-8]X,2,Voicemail(${EXTEN}@dept_2_vm)
```

## 6. Les Extensions

Les extensions spécifient les règles pour le routage des appels. Leur format est :

```ini
exten => Numéro,Priorité,Application()
```

### Numéros et Patterns

Les numéros peuvent être précis ou sous forme de patterns pour couvrir plusieurs numéros :

- `exten => 199,1,Answer()`
- `exten => _[123].[7-9],1,Answer()`
- `exten => _0XXXXXXXXX,1,Answer()`
- `exten => _1[0-8]X,1,Answer()`

### Applications

Les applications définissent les actions du serveur. Voici quelques exemples :

- `Answer()` : décroche l'appel
- `HangUp()` : raccroche l'appel
- `Dial(type/identifier,timeout)` : compose un numéro avec un délai
- `VoiceMail(user@context)` : accède à la messagerie de l'utilisateur
- `Playback(sound-file)` : joue un fichier audio

### Variables

Les variables permettent de personnaliser les actions :

- `${EXTEN}` : numéro appelé
- `${CONTEXT}` : contexte actuel
- `${CALLERID(num)}` : numéro de l'appelant
- `${DATETIME}` : date et heure actuelles

## 7. Extensions Spéciales

Certaines extensions ont des fonctions particulières :

- **I** : appel lorsque l'extension n'existe pas
- **t** : appel en cas de timeout
- **h** : appel lorsque l'utilisateur raccroche
- **s** : appel lorsque le numéro est inconnu

Exemples :

```ini
exten => t,1,Hangup()
exten => i,1,Playback(invalid)
```

## 8. Configuration du DialPlan

Configurez votre DialPlan pour permettre aux utilisateurs de se contacter et gérer les appels. Exemple de configuration :

```ini
[dept_1]
exten => _1[0-8]X,1,Dial(SIP/${EXTEN},40)
exten => _1[0-8]X,2,Voicemail(${EXTEN}@dept_1_vm)
exten => 199,1,Answer()
exten => 199,2,VoiceMailMain(${CALLERID(num)}@dept_1_vm)

[dept_2]
exten => _2[0-8]X,1,Dial(SIP/${EXTEN},40)
exten => _2[0-8]X,2,Voicemail(${EXTEN}@dept_2_vm)
exten => 299,1,Answer()
exten => 299,2,VoiceMailMain(${CALLERID(num)}@dept_2_vm)
```

---

---

# -------------------------------------------------------------- #
#                                                                #
#           Asterisk – CDR (Call Detail Record)                  #
#                                                                #
# -------------------------------------------------------------- #

Le CDR (Call Detail Record) est une fonctionnalité d’Asterisk qui permet de collecter des informations détaillées sur les appels transitant par le serveur. Ces données peuvent être utilisées pour la facturation des appels surtaxés ou à des fins d’analyse.

## 1) Fonctionnement

Le CDR recueille diverses informations sur les appels, telles que :

- La source de l’appel
- La destination de l’appel
- La date et l’heure de l’appel
- La durée de l’appel

Ces données peuvent être exportées sous forme de fichier CSV ou stockées dans une base de données MySQL. Par défaut, Asterisk est configuré pour enregistrer les données dans un fichier CSV.

Le CDR est principalement utilisé pour la facturation des appels surtaxés, mais il existe également de nombreux outils d’analyse qui permettent de générer des rapports détaillés avec des graphiques et autres visualisations.

## 2) Configuration

La configuration du CDR se fait dans le fichier `cdr.conf`. Voici la configuration de base habituellement présente :

```ini
[csv]
usegmtime=yes    ; Enregistre la date/heure en GMT. Par défaut : "no"
loguniqueid=yes  ; Enregistre l'identifiant unique. Par défaut : "no"
loguserfield=yes ; Enregistre le champ utilisateur. Par défaut : "no"
accountlogs=yes  ; Crée un fichier journal distinct pour chaque code compte. Par défaut : "oui"
```

Il est également nécessaire de modifier le fichier `cdr_manager.conf` comme suit :

```ini
[general]
enabled = yes
```

# -------------------------------------------------------------- #
#                                                                #
#                Asterisk – IVR (Interactive Voice Response)     #
#           (Configuration d'un Standard Automatique)            #
#                                                                #
# -------------------------------------------------------------- #

Les IVR (Interactive Voice Response) ou standards automatiques sont très utiles pour les entreprises. Ils permettent à l’appelant de faire des choix via un menu après avoir entendu un message préenregistré, facilitant ainsi la mise en relation avec le bon interlocuteur.

## 1) Fonctionnement d’un IVR

Un IVR fonctionne de la manière suivante :

1. L’appelant compose le numéro de l’IVR.
2. L’appel est pris en charge par le système IVR.
3. Un message préenregistré est joué (par exemple : "Pour joindre Marc Aubert, tapez 1 ; pour Alain Aldric, tapez 2").
4. L’appelant choisit une option en appuyant sur une touche.
5. Si le choix est valide, Asterisk redirige l’appelant vers le bon utilisateur ou service.

Le même principe peut être appliqué pour diriger l’utilisateur vers différents services (par exemple : 1 pour l’accueil, 2 pour le SAV, 3 pour le service commercial). Chaque service peut ensuite référer à un groupe de sonneries.

Pour configurer un IVR, vous devez modifier le fichier `extensions.conf`. Deux options sont disponibles pour le message à diffuser :

- Jouer un fichier audio préenregistré (recommandé pour une qualité professionnelle).
- Utiliser la synthèse vocale (facile à mettre en place pour des tests ou en dépannage).

Nous allons commencer par configurer un IVR simple et ensuite explorer l’utilisation de la synthèse vocale.

## 2) Configuration de l’IVR

Pour configurer un IVR, ajoutez les lignes suivantes au fichier `extensions.conf` :

Créez d'abord un contexte global pour rendre l’IVR accessible depuis tous les contextes :

```ini
[global]
exten => 900,1,Goto(ivr_1,s,1)
```

Ensuite, ajoutez un contexte spécifique pour l’IVR :

```ini
[ivr_1]
exten => s,1,Answer()
exten => s,2,Set(TIMEOUT(response)=10)                 ; Temps maximum pour choisir une option
exten => s,3,Playback(custom/IVR1-message)             ; Fichier audio à jouer
exten => s,4,WaitExten()                               ; Attend le choix de l'utilisateur

exten => 1,1,Dial(SIP/100)                             ; Si le choix est '1', appeler le 100
exten => 2,1,Dial(SIP/101)                             ; Si le choix est '2', appeler le 101
exten => 3,1,Dial(SIP/200)                             ; Si le choix est '3', appeler le 200
exten => _[04-9*#],1,Goto(ivr_1,s,1)                   ; Pour tout autre choix, renvoyer au début

exten => t,1,Goto(ivr_1,s,3)                           ; Redirige vers le message en cas de timeout
```

Placez le fichier audio à jouer dans le répertoire `/var/lib/asterisk/sounds/custom` :

```bash
mkdir /var/lib/asterisk/sounds/custom
```

Après un redémarrage, l’IVR devrait fonctionner correctement. Vous pouvez améliorer l’IVR en permettant à l’utilisateur d’interrompre le message en cours en choisissant une option avant la fin du message. Utilisez `Background` au lieu de `Playback` pour cela.

Pour gérer les choix invalides, jouez un message d’erreur avant de relancer le message principal :

```ini
exten => _[04-9*#],1,Playback(custom/IVR1-invalide)
exten => _[04-9*#],2,Goto(ivr_1,s,1)
```

Si vous souhaitez rediriger vers des utilisateurs spécifiques ou des groupes de sonneries, ajustez les lignes comme suit :

```ini
exten => 1,1,Goto(dept_1,100,1)
exten => 2,1,Goto(dept_1,101,1)
exten => 3,1,Goto(dept_2,200,1)
```

La configuration finale de l’IVR sera alors :

```ini
[global]
exten => 900,1,Goto(ivr_1,s,1)

[ivr_1]
exten => s,1,Answer()
exten => s,2,Set(TIMEOUT(response)=10)
exten => s,3,Background(custom/IVR1-message)
exten => s,4,WaitExten()

exten => 1,1,Goto(dept_1,100,1)
exten => 2,1,Goto(dept_1,101,1)
exten => 3,1,Goto(dept_2,200,1)
exten => _[04-9*#],1,Playback(custom/IVR1-invalide)
exten => _[04-9*#],2,Goto(ivr_1,s,1)

exten => t,1,Goto(ivr_1,s,3)
```



Voici un résumé détaillé de la configuration des files d'attente et des conférences dans Asterisk, tiré de votre document :

---

# -------------------------------------------------------------- #
#                                                                #
#                      Asterisk – Queues                         #
#                                                                #
# -------------------------------------------------------------- #


Les files d'attente (queues) permettent de gérer les appels entrants de manière plus sophistiquée que les Ring Groups, en dirigeant les appels vers les agents disponibles de manière ordonnée.

#### Configuration des Files d'Attente

1. **Fichier `queues.conf` :**
   - **Définition de la File d'Attente :**
     ```ini
     [sav]
     musiconhold=default
     strategy=rrmemory
     timeout=20
     retry=15
     maxlen=0
     wrapuptime=15
     joinempty=no
     leavewhenempty=yes
     ```
   - **Paramètres Principaux :**
     - `musiconhold` : Musique d'attente.
     - `strategy` : Stratégie de distribution des appels (ex : `rrmemory` pour distribution en mémoire).
     - `timeout` : Temps maximal de sonnerie avant de passer à l'agent suivant.
     - `retry` : Temps d'attente avant de réessayer de distribuer l'appel.
     - `maxlen` : Nombre maximum d'appels dans la file d'attente.
     - `wrapuptime` : Temps d'attente après la fin d'un appel avant de réassigner un nouvel appel.
     - `joinempty` : Autorise ou non l'ajout d'appels dans une file d'attente vide.
     - `leavewhenempty` : Permet de sortir les appels d'une file d'attente vide.

2. **Fichier `extensions.conf` :**
   - **Configuration pour les Agents :**
     ```ini
     exten => 961,1,AddQueueMember(sav,SIP/${CALLERID(num)})
     exten => 961,n,Playback(agent-loginok)
     exten => 961,n,Hangup
     exten => 962,1,RemoveQueueMember(sav,SIP/${CALLERID(num)})
     exten => 962,n,Playback(agent-loggedoff)
     exten => 962,n,Hangup
     ```
   - **Placement des Appels dans la File d'Attente :**
     ```ini
     exten => 960,1,Answer
     exten => 960,n,Queue(sav|t)
     exten => 960,n,Voicemail(101)
     exten => 960,n,Hangup
     ```

---

### Asterisk – Conférences

Les conférences permettent des appels multi-participants avec différentes options de sécurité et gestion des participants.

#### Configuration des Conférences

1. **Module `MeetMe` :** (déprécié, à utiliser ConfBridge si possible)
   - **Fichier `meetme.conf` :**
     ```ini
     [rooms]
     conf => 910
     conf => 920,123
     conf => 930,123,9876
     ```
   - **Fichier `extensions.conf` :**
     ```ini
     exten => 910,1,MeetMe(910)
     exten => 920,1,MeetMe(920)
     exten => 930,1,MeetMe(930)
     ```
   - **Options supplémentaires :**
     - `s` : Menu de la conférence
     - `M` : Musique d'attente
     - `c` : Annonce du nombre de participants
     - `a` : Mode administrateur

2. **Module `ConfBridge` :**
   - **Fichier `confbridge.conf` :**
     ```ini
     [User_NoAuth]
     type=user
     admin=no
     music_on_hold_when_empty=yes
     announce_user_count=yes

     [User_Auth]
     type=user
     admin=no
     music_on_hold_when_empty=yes
     announce_user_count=yes
     pin=1234

     [User_Admin]
     type=user
     admin=yes
     music_on_hold_when_empty=yes
     announce_user_count=yes
     pin=5678

     [ConfRoom_1]
     type=bridge
     max_members=10

     [ConfRoom_2]
     type=bridge
     max_members=100
     ```
   - **Fichier `extensions.conf` :**
     ```ini
     exten => 900,1,ConfBridge(Room_1,ConfRoom_1,User_NoAuth)
     exten => 901,1,ConfBridge(Room_1,ConfRoom_1,User_Admin)
     exten => 903,1,ConfBridge(Room_2,ConfRoom_2,User_Auth)
     exten => 904,1,ConfBridge(Room_2,ConfRoom_2,User_Admin)
     ```

   - **Paramètres ConfBridge :**
     - 1er paramètre : Nom de la salle.
     - 2e paramètre : Salle à rejoindre.
     - 3e paramètre : Profil utilisateur (authentification et options).

---