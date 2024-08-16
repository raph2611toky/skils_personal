# -------------------------------------------------------------- #
#                                                                #
#              Configuration Basique d’Asterisk                  #
#                                                                #
# -------------------------------------------------------------- #


Afin de débuter la configuration de notre serveur Asterisk, voyons quelques configurations de base.
Nous allons créer des utilisateurs, puis configurer le DialPlan pour permettre aux appels de passer.
A l’issue de cet article vous disposerez d’un système basique mais fonctionnel.

1) L’administration d’Asterisk
------------------------------

Avant de nous plonger dans la configuration d’Asterisk, attardons nous sur la manière de
l’administrer.
Nous disposons de deux choses pour administrer Asterisk :
La console
Les fichiers de configuration
https://www.networklab.fr/configuration-basique-dasterisk/

Page 1 sur 29La console permet principalement de faire du debug et de voir l’état du serveur.
Nous pouvons aussi l’utiliser pour redémarrer Asterisk, charger des modules, etc...
La console se lance avec la commande suivante :
asterisk –r
Il est possible de placer le paramètre « v » à la fin de la commande.
De cette manière la console s’ouvrira en mode verbeux.
Sans le mode verbeux, la console ne retourne aucun debug lors des actions.
Avec le mode verbeux, nous obtenons des retours sur les commandes entrées.
Plus nous plaçons de « v » à la fin de la commande, plus nous obtiendrons de debug.
asterisk -rvvv
La configuration d’Asterisk se fait dans les fichiers de configuration.
https://www.networklab.fr/configuration-basique-dasterisk/

Ces fichiers sont placés dans le répertoire suivant :
# /etc/asterisk/


Pour que les modifications des fichiers soient prises en compte, il faut relancer Asterisk. Ou au
moins le module concerné.
asterisk –rv
reload


2) Création d’utilisateur
-------------------------

La configuration des utilisateurs est à faire dans le fichier users.conf (dans /etc/asterisk/)
Avant d’éditer les fichiers pour la première fois, vous pouvez les vider comme ceci :
# echo "" > users.conf


Chaque utilisateur sera défini dans ce fichier. Nous y retrouverons les paramètres des utilisateurs.
Afin de simplifier la création d’utilisateur, nous pouvons placer les paramètres communs dans un
Template.
Les utilisateurs feront alors référence au Template.
De cette manière, il sera très simple d’ajouter de nouveaux users.
Commençons donc par créer le Template.


[default_template](!)      ; Nom du template . Le « ! » indique qu’il s’agit d’un Template
type=friend                ; Type d'objet SIP (friend = utilisateur)
host=dynamic               ; L’utilisateur n’est pas associé à une IP fixe
dtmfmode=rfc2833           ; Mode DTMF
disallow=all               ; Interdit tous les codecs
allow=ulaw                 ; Autorise le codec ulaw
nat=never                  ; L'utilisateur ne se trouve pas derrière un NAT
hassip=yes                 ; L’utilisateur possède un compte SIP
hasiax=no                  ; L’utilisateur ne possède pas de compte iax
callwaiting = yes          ; L’utilisateur peut mettre des appels en attente
transfer=yes               ; L’utilisateur peut transférer des appels
canpark=yes                ; L’utilisateur peut mettre des appels dans le parking
hasvoicemail=yes           ; L’utilisateur possède une boîte vocale
deny=0.0.0.0/0.0.0.0       ; Range d’IP non-autorisées pour le client
permit=192.168.1.0/255.255.255.0     ; Range d’IP autorisées pour le client
qualify=yes                ; Permet le monitoring

Certains des paramètres ont pour valeur par défaut la valeur indiquée ici.

Le type d’objet SIP peut prendre 3 valeurs :
  -  Peer
  -  User
  -  Friend
Le Peer est un objet auquel nous pouvons envoyer des appels (exemple : le Trunk vers l’ITSP).
L’User est un objet qui ne peut qu’appeler.
Le Friend est à la fois Peer et User. Il peut envoyer et recevoir des appels (exemple : un utilisateur)

Nous pouvons ensuite créer des utilisateurs :

[100](default_template)                 ; Numéro SIP et Template utilisé
fullname = Marc Aubert                  ; Nom complet de l'utilisateur us
username = maubert                      ; Nom d'utilisateur      
secret=password                         ; Mot de passe
mailbox = 100                           ; N° de boîte vocale
context=dept_1                          ; Contexte de l’utilisateur

[101](default_template)                 ; Numéro SIP et Template utilisé
fullname = Alain Aldric                 ; Nom complet de l'utilisateur
username = aaldric                      ; Nom d'utilisateur
secret=password                         ; Mot de passe
mailbox = 101                           ; N° de boîte vocale
context=dept_1                          ; Contexte de l’utilisateur

[200](default_template)                 ; Numéro SIP et Template utilisé
fullname = Leon Morgan                  ; Nom complet de l'utilisateur
username = lmorgan                      ; Nom d'utilisateur
secret=password                         ; Mot de passe
mailbox = 200                           ; N° de boîte vocale
context=dept_2                          ; Contexte de l’utilisateur

Pensez à relancer Asterisk pour qu’il prenne en compte les modifications.
# asterisk –rvv
# reload

Veillez à ce qu’il ne retourne pas d’erreur.


3) Configuration des Voicemails
-------------------------------

Les Voicemails permettent de laisser des messages aux utilisateurs lors-ce-que ceux-ci ne sont pas disponibles.
Il s’agit donc de leur messagerie vocale.
Pour se connecter à leur messagerie, les utilisateurs devront composer un certain numéro, puis
entrer un mot de passe.

Voyons comment configurer le fichier voicemail.conf.
Le fichier à éditer est le suivant :
# nano /etc/asterisk/voicemail.conf

Je vous invite à jeter un œil à son contenu avant de le vider.
# echo "" > voicemail.conf


Au début du fichier, une section générale définira les paramètres généraux des Voicemails.
En voici un example :

[general]
maxmsg=100                   ; Nombre max de message sur la Voicemail. Si elle est pleine, il n'est pas possible de rajouter des messages
maxsecs=0                    ; Durée max d'un message. "0" = pas de limite
minsecs=2                    ; Durée minimum d'un message
maxlogins=3                  ; Nombre max d'erreur de login
review=no                    ; Permet à l'appelant de réécouter son message avant de le transmettre à la Voicmail. Accessible en terminant le message par #
saycid=no                    ; Dicte le numéro de l'appelant avant de jouer le message qu'il a laissé

La plupart de ces paramètres sont ici à leur valeur par défaut (hormis minsecs)
Dans la suite du fichier, nous définirons les utilisateurs.

[dept_1_vm]
100 => 1234, Marc Aubert
101 => 1234, Alain Aldric

[dept_2_vm]
200 => 1234, Leon Morgan

Ici, “1234” correspond au mot de passe de la Voicemail de l’utilisateur.
Il est possible de désactiver l’utilisation du mot de passe, en ne spécifiant rien avant la virgule.
200 => , Leon Morgan

Les trois utilisateurs précédemment créés ont à présent chacun une boite vocale.
En appelant leur messagerie, il leurs sera possible de consulter leurs messages, mais aussi de
personnaliser leur message d’accueil.
Asterisk propose aussi d’envoyer un mail à l’utilisateur lors-ce-que celui a reçu un message sur sa
Voicemail. De plus, le message audio sera inclus en pièce-jointe du mail.
Cette option nécessite une configuration plus poussée. Il faudra aussi qu’Asterisk puisse envoyer
des mails.

N’oubliez pas de relancer Asterisk pour prendre en compte les modifications.
# asterisk –rv
# reload

Ou au moins la configuration des Voicemails.
# asterisk –rv
# voicemail reload



4) Le DialPlan
--------------

But du DialPlan

Passons à présent au cœur d’Asterisk : le DialPlan.
Le DialPlan est ce qui va définir le routage des appels à travers le serveur.
La configuration du DialPlan est contenue dans le fichier suivant :
# /etc/asterisk/extensions.conf


Dans ce fichier, nous devrons définir le comportement d’Asterisk vis-à-vis des appels.
Par exemple, que ce passe-t-il lors-ce-que Asterisk reçoit un appel à destination du numéro 100 ?
Nous allons définir une règle qui dit qu’il faut faire sonner le téléphone de l’utilisateur 100, et ce
pendant X secondes, avant de renvoyer l’appelant sur la messagerie de l’utilisateur 100.

De même, pour permettre à un utilisateur de consulter sa messagerie, nous définirons un numéro
associés à la messagerie du groupe d’utilisateur.

Par exemple, pour les utilisateurs 100 à 190, s’ils composent le numéro 199, ils tomberont sur leur
messagerie.
Etc...

Voici un aperçu de ce que cela pourrait donner dans le fichier extensions.conf :

exten => _1[0-8]X,1,Dial(SIP/${EXTEN},30)
exten => _1[0-8]X,2,Voicemail(${EXTEN}@dept_1_vm)


Sans rentrer dans les détails pour le moment, cela signifie que si quelqu’un appelle un numéro entre
100 et 189, le téléphone associé à ce numéro sonnera pendant 30 secondes. Sans réponse,
l’appelant tombera sur la Voicemail de l’utilisateur qu’il cherchait à joindre.

Pour ce qui est de consulter la messagerie :

exten => 199,1,Answer()
exten => 199,2,VoiceMailMain(${CALLERID(num)}@dept_1_vm)

Quand un utilisateur appel le numéro 199, il sera redirigé vers sa propre messagerie. A condition
qu’il ait une messagerie définie dans dept_1_vm.

Étudions plus en détail le fonctionnement du fichier extensions.conf.

+ ---------------------------- +
+        Les contextes         + 
+ ---------------------------- +

Tout d’abord, le DialPlan est agencé sous forme de contexte.
Chaque utilisateur appartient à un contexte, d’après le fichier User.conf.

Quand un utilisateur lance un appel, Asterisk va chercher, dans le contexte associé à l’utilisateur, les actions à effectuer.

Les contextes sont définis entre crochet.
Voici un exemple :

[dept_1]
exten => _1[0-8]X,1,Dial(SIP/${EXTEN},30)
exten => _1[0-8]X,2,Voicemail(${EXTEN}@dept_1_vm)

[dept_2]
exten => _2[0-8]X,1,Dial(SIP/${EXTEN},30)
exten => _2[0-8]X,2,Voicemail(${EXTEN}@dept_2_vm)



+ ------------------------------- +
+         Les Extensions          +
+ ------------------------------- +

Les entrées dans le fichier extension.conf sont appelées des extensions.
Elles se composent comme ceci :

exten => Numéro,Priorité, Applications ()

Le mot clé « Exten => » marque le début d’une extension.
Le numéro correspond au numéro de téléphone pris en compte par l’extension.
La priorité définie l’ordre des actions de l’extension.

En effet, nous spécifierons toujours plusieurs actions dans une extension (voir exemple précédent).
L’application définit ce que le serveur va faire.
Voyons les possibilités qui s’offrent à nous pour la rédaction d’une extension.

Commençons par le numéro.

+ ------------------------------- +
+           Les numéros           +
+ ------------------------------- +

Comme nous l’avons vu, nous pouvons spécifier un numéro bien précis.

exten => 199,1,Answer()

Ou bien, nous pouvons spécifier un pattern.
Le but ici est de prendre en compte plusieurs numéros.
Tout d’abord, un pattern doit commencer par un « _ ».
Ensuite, nous pouvons utiliser les caractères suivants :
 - « X » : correspond aux chiffres de 0 à 9
 - « Z » : correspond aux nombres de 1 à 9
 - « N » : correspond aux nombres de 2 à 9
 - « . » : correspond à un ou plusieurs chiffres
 - « ! » : correspond à zéro ou plusieurs chiffres

 Nous pouvons aussi utiliser les crochets.
[1-5] correspond aux nombre de 1 à 5.
[123] correspond aux nombres 1, 2 ou 3.
Voici à présent quelques exemples :

exten => _[123].[7-9],1,Answer()

Cette extension englobe tous les numéros commençant par 1, 2 ou 3, et qui finissent par 7, 8 ou 9.

exten => _0XXXXXXXXX,1, Answer()

Cette extension correspond à tous les numéros à 10 chiffres, qui commencent par 0.

exten => _1[0-8]X,1,Answer()

Cette extension englobe tous les numéros de 100 à 189. Ainsi nous pouvons garder les 10 derniers
numéros comme numéros spéciaux (Voicemail, Conférence, etc...).


+ ------------------------------- +
+         Les applications        +
+ ------------------------------- +


Les applications définissent ce que doit faire le serveur.
Par exemple, Answer() signifie que le serveur doit décrocher l’appel.
Ces applications peuvent prendre un ou plusieurs paramètres.
Voici une liste de quelques applications possibles :

  -  Answer() : permet de décrocher l’appel
  -  HangUp() : permet de raccrocher l’appel
  -  Dial(type/identifier,timeout) : permet de composer un numéro, avec un timeout en cas de
non-réponse
  -  VoiceMail(user@context) : permet de joindre la messagerie de l’utilisateur spécifié
  -  VoiceMailMain(user@context) : permet de consulter la messagerie de l’utilisateur spécifié
  -  Playback(sound-file) : permet de jouer un son
  -  SetMusicOnHold(class) : permet de jouer une musique d’attente
  -  Goto(contexte,extension,priorité): permet de se rendre à un contexte précis, à une
certaine extension, à une certaine priorité


Il existe encore bien d’autres applications.
En paramètre de ces applications, nous pouvons utiliser des variables.

+ ------------------------------- +
+         Les variables           +
+ ------------------------------- +

Voici quelques variables qui peuvent être utilisés dans le DialPlan :

  -  ${EXTEN} : Renvoie l’extension actuellement appelée
  -  ${CONTEXT} : Renvoie le contexte actuel
  -  ${CALLERID(name)} : Renvoie le nom de la personne qui appel
  -  ${CALLERID(num)} : Renvoie le numéro de la personne qui appel
  -  ${DATETIME} : Renvoie la date actuelle au format DDMMYYYY-HH:MM:SS
  -  ${PRIORITY} : Renvoie la priorité actuelle de l’extension


  De même que pour les applications, il existe de très nombreuses variables.
A présent, vous êtes en mesure de comprendre l’intégralité des exemples précédents.

exten => _1[0-8]X,1,Dial(SIP/${EXTEN},30)
exten => _1[0-8]X,2,Voicemail(${EXTEN}@dept_1_vm)

Le « ${EXTEN} » de la priorité 1 fait référence au numéro composé par l’appelant, ce qui permet de
joindre le numéro qui a été composé.
Le « ${EXTEN} » de la priorité 2 permet de joindre la Voicemail.

exten => 199,1,Answer()
exten => 199,2,VoiceMailMain(${CALLERID(num)}@dept_1_vm)

Ici, le ${CALLERID(num)} fait référence au numéro de l’appelant, et lui permet de joindre sa
Voicemail.


+ ------------------------------- +
+    Les extensions spéciales     +
+ ------------------------------- +

Il existe aussi certaines extensions spéciales.
Voyons certaines de ces extensions.

# L’extension « I »

Correspond à l’extension qui est appelée quand l’appelant compose une extension qui n’existe pas
dans le contexte ou dans l’IVR (standard auto avec choix au clavier).

# L’extension « t »
Correspond à l’extension qui est appelée lors d’un timeout. Par exemple, si l’utilisateur ne choisit pas
d’option dans un IVR.

# L’extension « h »
Correspond à l’extension qui est appelée lors-ce-que l’utilisateur raccroche.

# L’extension « s »
Correspond à l’extension qui est appelée lors-ce-que le serveur n’a pas d’information sur le numéro
appelé (cas typique d’un appel sur une ligne analogique).

Par exemple, dans le contexte d’un IVR, si l’utilisateur ne fait pas de choix, nous pouvons
raccrocher.


# exten => t,1,Hangup()

Ou encore, en cas de choix invalide, nous pouvons jouer un son.

# exten => i,1,Playback(invalid)


5) Configuration du DialPlan
----------------------------

A présent que nous avons étudié la structure du DialPlan, configurons celui de notre serveur, afin
d’obtenir un comportement basique.
De plus, ce sera l’occasion de voir des exemples sur les notions abordées précédemment.

Tout d’abord, il nous faut permettre aux utilisateurs d’un même contexte de s’appeler entre eux.

En effet, même les actions basiques comme celle-ci sont à configurer dans le DialPlan.
La configuration à mettre en place a déjà été présentée précédemment.
Avant de configurer quoi que ce soit, il faut vider le fichier extensions.conf.
Au passage, n’hésitez pas à jeter un œil à la configuration d’exemple avant de la supprimer.


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




# -------------------------------------------------------------- #
#                                                                #
#            Asterisk – CDR – Call Detail Record                 #
#                                                                #
# -------------------------------------------------------------- #

Le CDR ou Call Detail Record est une fonctionnalité d’Asterisk qui permet de recueillir des informations sur les appels qui transitent par le serveur.

Ces informations peuvent ensuite être utilisées pour facturer les appels surtaxés, ou bien simplement à des fins d’analyse.

1) Fonctionnement
-----------------

Comme évoqué en introduction, le Call Detail Record permet de collecter toute une série d’informations sur les appels qui transitent par notre serveur Asterisk.

Dans ces informations, nous retrouvons par exemple :

    La source de l’appel
    La destination de l’appel
    La date de l’appel
    La durée de l’appel
    Etc…

 

Ces informations peuvent être extraites soit dans un fichier CSV, soit dans une base MySQL.

Par défaut, Asterisk est configuré pour collecter les données dans un fichier CSV.


Le CDR est souvent utilisé pour facturer les appels surtaxés aux appelants.

Mais il existe aussi un grand nombre d’outils permettant d’analyser les données, et de restituer des rapports comportant des graphiques, etc…


2) Configuration
----------------

La configuration du CDR est à faire dans le fichier cdr.conf.

Voici la configuration de base (normalement) déjà présente dans le fichier :

[csv]
usegmtime=yes    ; log date/time in GMT.  Default is "no"
loguniqueid=yes  ; log uniqueid.  Default is "no"
loguserfield=yes ; log user field.  Default is "no"
accountlogs=yes  ; create separate log file for each account code. Default is "yes"

Il faut également modifier le fichier cdr_manager.conf comme ceci :
[general]
enabled = yes


# -------------------------------------------------------------- #
#                                                                #
#               Asterisk – IVR – Standard Auto                   #
#              ( Initiation Session Protocole )                  #
#                                                                #
# -------------------------------------------------------------- #

Les IVR – Interactive Voice Response ou Standard Automatiques sont très pratiques pour une entreprise.

Le principe est simple et très connu : après la lecture d’un message préenregistré, l’appelant peut faire un choix au clavier.

Cela permet par exemple de mettre l’appelant en relation avec la bonne personne.

Au travers de cet article, nous verrons comment mettre en place un IVR.

1) Fonctionnement d’un IVR
--------------------------

Comme dit précédemment, un IVR est un standard automatique.
Ils sont très utilisés pour les standards, les calls center, etc…

Voici un exemple de fonctionnement d’un IVR :

    L’appelant compose le numéro de l’IVR
    L’appel est décroché par un robot
    Un message est joué (ex : pour joindre Marc Aubert taper 1, pour joindre Alain Aldric taper 2, etc…)
    L’appelant fait son choix et appuie sur la touche correspondante au clavier
    Si le choix est valide, Asterisk redirige l’appelant vers le bon utilisateur

Bien entendu, nous pouvons appliquer le même procédé pour rediriger l’utilisateur vers des services (ex : taper 1 pour l’accueil, 2 pour le SAV, 3 pour le service commercial, etc…).

Chaque service peut ensuite faire référence à un Ring Group.
Les possibilités sont multiples.
Pour la configuration, comme toujours elle se fera dans le DialPlan, c’est à dire dans le fichier extensions.conf.
Pour ce qui est du message à diffuser, il existe deux solutions :

    Jouer un fichier audio que l’on a enregistré
    Faire de la synthèse vocale

Bien entendu, la première option est la meilleure.

Tout simplement car le rendu sera meilleur est plus professionnel.
Néanmoins, la synthèse vocale est très simple à mettre en place (hormis la première configuration).

Il suffira simplement de taper le message dans le fichier de configuration, et Asterisk se chargera d’en faire un message audio.
Ce peut donc être idéal pour dépanner.
De plus, c’est une bonne solution pour tester la mise en place d’un IVR.
Nous commencerons par mettre en place un IVR simple, puis nous passerons à la synthèse vocale.


2) Configuration IVR
--------------------

Plutôt qu’un long discours, voyons tout de suite la configuration de l’IVR.
Comme mentionné auparavant, la configuration se fait dans le fichier extensions.conf.

La bonne pratique est de créer un contexte spécifique pour l’VR.

Mais il est tout à fait possible d’intégrer l’IVR dans un contexte déjà existent.
Tout d’abord, il faut créer une extension correspondant à l’IVR, dans le contexte qui devra permettre de joindre l’IVR.

Afin de rendre l’IVR accessible par tout le monde, vous pouvez créer un contexte global, que vous inclurez dans tous les autres contextes.

dans extensions.conf:

[global]
exten => 900,1,Goto(ivr_1,s,1)

[dept_1]
include => global

Ensuite, créer un contexte pour l’IVR.

[ivr_1]
exten => s,1,Answer()
exten => s,2,Set(TIMEOUT(response)=10)                 ; Temps max pour choisir une option   
exten => s,3,Playback(custom/IVR1-message)             ; Fichier audio à jouer
exten => s,4,WaitExten()                               ; Lecture du choix

exten => 1,1,Dial(SIP/100)                             ; Si le choix est '1' appeller le 100
exten => 2,1,Dial(SIP/101)                             ; Si le choix est '2' appeller le 101 
exten => 3,1,Dial(SIP/200)                             ; Si le choix est '3' appeller le 200 
exten => _[04-9*#],1,Goto(ivr_1,s,1)                   ; Pour tout autre choix, renvoyer au début

exten => t,1,Goto(ivr_1,s,3)

Le fichier audio à jouer sera cherché dans /var/lib/asterisk/sounds/

L’idéal est d’y créer un nouveau dossier contenant les fichiers audio « spéciaux ».

mkdir /var/lib/asterisk/sounds/custom

Après un redémarrage, l’IVR devrait fonctionner.
Il est possible d’améliorer l’IVR de plusieurs manières.

Premièrement, pour rendre l’IVR plus réactif, nous pouvons autoriser l’utilisateur à interrompre le message audio en choisissant une option avant la fin du message (utile pour les utilisateurs qui connaissent l’IVR).

Au lieu d’utiliser l’application Playback, il faut alors utiliser l’action Background.

exten => s,3,Background(custom/IVR1-message)

Ensuite, en cas de choix invalide, nous pouvons retourner un message à l’utilisateur, avant de relancer le message d’accueil.

La détection d’entrée invalide devient alors :

exten => _[04-9*#],1,Playback(custom/IVR1-invalide)
exten => _[04-9*#],2,Goto(ivr_1,s,1)

Aussi, vous aurez peut être remarqué que lors-ce qu’un utilisateur ne répond pas, l’appelant ne tombe pas sur la messagerie.

Vous pouvez modifier la configuration pour prendre cela en compte.

 

Le renvoie vers les utilisateurs devient alors :

exten => 1,1,Goto(dept_1,100,1)           
exten => 2,1,Goto(dept_1,101,1)
exten => 3,1,Goto(dept_2,200,1)

 

De cette manière, l’IVR utilise le comportement défini dans les contextes associés aux utilisateurs.

 

Bien entendu, vous pouvez faire pointer l’IVR vers un Ring Group.

 

La configuration finale de l’IVR est donc la suivante :

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

 

L’IVR est maintenant bien plus agréable à utiliser.

Vous noterez que l’IVR est utilisable pas plusieurs personnes en même temps


# -------------------------------------------------------------- #
#                                                                #
#                       Asterisk – Queues                        #
#                                                                #
# -------------------------------------------------------------- #

Les files d’attente peuvent être utiles pour gérer les appels entrants.

Le concept de base fait penser aux Ring Group, même si les Queues permettent de mieux gérer la distribution des appels.

Dans cet article nous verrons comment mettre en place une file d’attente basique.

1) Fonctionnement
-----------------

Une file d’attente dans Asterisk fonctionne comme une vraie file d’attente.
Lors-ce qu’un utilisateur appel, il est placé dans la file d’attente, à la fin, et une musique d’attente lui est jouée.
Le premier entré dans la file sera le premier à sortir (sauf en cas d’utilisation de priorité).

Des agents doivent faire partie de la file d’attente. Leur rôle sera de prendre en charge les appels dans la file d’attente.

De cette manière, nous pourrons avoir 5 appels dans la file d’attente, ainsi que deux agents qui se chargent de la file.
Petit à petit, les agents vont prendre les appels, jusqu’à vider la file d’attente.
C’est là la première différence avec les Ring Group.

Quand un appel entre dans un Ring Group, il va automatiquement être routé vers le premier utilisateur du Ring Group, quitte à générer un double appel si celui-ci est déjà occupé.
Alors que dans une file d’attente, les appels seront dirigés vers les utilisateurs libres.
Autre différence, les agents peuvent rejoindre et quitter la file d’attente.
C’est-à-dire qu’un agent n’est pas forcé de prendre en charge les appels de la queue.

2) Configuration d’une file d’attente
-------------------------------------

La configuration d’une file d’attente fait appel aux fichiers queues.conf et extensions.conf.
La file d’attente sera définie dans le fichier queues.conf.
Nous pourrons y placer de nombreux paramètres (musique d’attente, temps de sonnerie, stratégie de répartition des appels, etc…). 

Le fichier extensions.conf contiendra la configuration qui permet aux agents de rejoindre la file d’attente.
C’est aussi grâce à ce fichier que nous pouvons placer des appels dans la file d’attente.
Commençons par définir la file d’attente.

Dans le fichier queues.conf, placer la configuration suivante :

[sav]
musiconhold=default
strategy=rrmemory
timeout = 20
retry = 15
maxlen = 0
wrapuptime=15
joinempty = no
leavewhenempty = yes

Musiconhold fait référence aux sections du fichier musiconhold.conf.

Strategy permet de définir la stratégie de réparation des appels.

Il existe différentes stratégies :

    ringall : les postes de tous les agents sonnent, l’appel est donné au premier qui décroche
    roundrobin : donne les appels aux agents à tour de rôle
    leastrecent : donne l’appel à l’agent inactif depuis le plus longtemps
    fewestcalls : donne l’appel à l’agent qui a pris le moins d’appel
    random : donne l’appel à un agent au hasard
    rrmemory : donne les appels aux agents à tour de rôle, en gardant en mémoire le dernier qui a eu un appel


Timeout définit le temps maximum de sonnerie du poste d’un agent, avant de passer l’appel à l’agent suivant.

Retry définit le temps qu’Asterisk attend avant de retenter de placer un appel chez l’un des agents.

Maxlen définit le nombre maximum d’appels dans la Queue. 0 permet de ne pas mettre de limite.
Wrapuptime définit le temps minimum avant qu’Asterisk puisse redonner un appel à un Agent qui vient de raccrocher.

Joinempty permet d’autoriser ou non le placement d’appel dans une file d’attente dans laquelle il n’y a aucun agent.
Leavewhenempty permet de sortir les appels d’une file d’attente dans l’laquelle il n’y a aucun agent.
Libre à vous de personnaliser ces paramètres en fonction de vos besoins.

Sachez qu’il en existe encore bien d’autres.
Passons à présent à la configuration du fichier extensions.conf.
Premièrement, nous devons permettre aux agents de rejoindre et de quitter la Queue.

Voici la configuration pour les agents. Celle-ci est à placer dans les contextes contenant des utilisateurs pouvant devenir Agent.

N’oubliez pas qu’il est possible de placer la configuration dans un contexte parent, pour ensuite inclure ce contexte dans d’autres contextes.

exten => 961,1,Addqueuemember(sav,SIP/${CALLERID(num)})
exten => 961,n,Playback(agent-loginok)
exten => 961,n,Hangup
exten => 962,1,Removequeuemember(sav,SIP/${CALLERID(num)})
exten => 962,n,Playback(agent-loggedoff)
exten => 962,n,Hangup

Quand un utilisateur compose le 961, il devient agent de la Queue « sav ».

Quand il compose le 962, il perd son statut d’agent de la Queue « sav ».
Pour ce qui est de placer des appels dans la Queue, la configuration est la suivante :

exten => 960,1,Answer
exten => 960,n,Queue(sav|t)
exten => 960,n,Voicemail(101)
exten => 960,n,Hangup

Tous les appels vers 960 seront redirigés vers la Queue.
L’option « t » de la ligne 2 permet à l’appelé de rediriger l’appel.
Avec la configuration précédente, tous les appels sur 960 seront placés dans la file d’attente « sav », et les utilisateurs s’étant enregistrés en composant le 961 pourront prendre en charge ces appels.
L’idéal serait bien entendu de jouer un message d’accueil à l’utilisateur qui entre dans la Queue.

Vous pouvez faire cela avec un fichier audio, ou avec du TTS (si vous avez déjà configuré ce dernier).
Par exemple :

exten => 960,1,Answer
exten => 960,2,agi(googletts.agi,"Bonjour et bienvenue chez NetworkLab !",fr,any)
exten => 960,3,agi(googletts.agi,"Un de nos conseillers va prendre votre appel.",fr,any)
exten => 960,n,Queue(sav|t|||30)
exten => 960,n,Voicemail(101)
exten => 960,n,Hangup


# -------------------------------------------------------------- #
#                                                                #
#                   Asterisk – Conférences                       #
#                                                                #
# -------------------------------------------------------------- #

Les conférences téléphoniques peuvent être utiles pour réaliser des appels à plus de deux personnes.

La mise en place est très simple, et l’utilisation l’est tout autant.

Voyons ensemble comment Asterisk permet la réalisation de conférences téléphoniques.

1) Fonctionnement
-----------------

Les conférences téléphoniques fonctionnent par salle.

Quand un utilisateur veut rejoindre une conférence, il appelle le numéro de la salle, afin d’y entrer.

Tous les utilisateurs ayant fait de même se retrouveront ensemble dans ladite salle.

Les utilisateurs peuvent alors dialoguer, quitter et rejoindre la salle à leur convenance, etc…
Anciennement, le module qui gérait les conférences dans Asterisk s’appelait MeetMe. Aujourd’hui, il est deprecated et ConfBridge a prit le relais.

Nous verrons les deux dans cet article, même si il est recommandé d’utiliser ConfBridge. Néanmoins, je vous recommande de lire la partie sur MeetMe dans tous les cas, afin de profiter des explications.

2) MeetMe
---------

Configuration

Dans le fichier meetme.conf, la configuration est la suivante :

[rooms]
conf => N° salle, MDP, MDP admin
Le numéro de salle peut être au choix :

    Le numéro utilisé pour entrer dans la salle
    Un numéro arbitraire

En effet, le numéro à composer pour entrer dans la salle sera défini dans le DialPlan.

La bonne pratique veut que l’on utilise le même numéro dans extensions.conf que dans meetme.conf.
Nous allons créer trois salles :

    910 : une salle ouverte
    920 : une salle avec un mot de passe
    930 : une salle avec un mot de passe et un mot de passe administrateur
La configuration sera alors la suivante :

[rooms]
conf => 910
conf => 920,123
conf => 930,123,9876

Dans extensions.conf, il faudra ajouter la partie suivante :

exten => 910,1,MeetMe(910)
exten => 920,1,MeetMe(920)
exten => 930,1,MeetMe(930)

Pour que les salles de conférence soient accessibles par tout le monde, le mieux est de créer un contexte global, qui sera inclus dans les autres contextes.

Comme ceci :
[global]
exten => 910,1,MeetMe(910)
exten => 920,1,MeetMe(920)
exten => 930,1,MeetMe(930)

[dept_1]
include => global

[dept_2]
include => global

Il est possible d’ajouter des options pour l’accès aux conférences.

Voici certaines d’entre elles :

    s : permet d’accéder au menu de la conférence avec la touche « * » (mode mute, augmenter / réduire volume, etc…)
    M : permet de jouer une musique d’attente quand l’utilisateur est seul dans la conférence
    c : permet d’annoncer le nombre de participant actuel quand l’utilisateur rejoint la conférence
    a : rend l’utilisateur administrateur de la conférence

Au moment de rejoindre la conférence, si l’utilisateur est administrateur, et qu’un mot de passe admin a été configuré, l’utilisateur devra entrer ce dernier.

Un fois dans la conférence, l’utilisateur aura accès à des options avancées à l’aide du menu.

Il est donc indispensable que le menu soit activé (option « s »).
Ces options sont à configurer dans extensions.conf.

Nous pouvons par exemple utiliser la configuration suivante :

[global]
exten => 910,1,MeetMe(910,cMs)
exten => 920,1,MeetMe(920,cMS)
exten => 930,1,MeetMe(930,cMs)

[dept_1]
include => global
exten => 930,1,MeetMe(930,acMs)

[dept_2]
include => global

De cette manière, nous aurons une salle de conférence 910, qui sera publique, avec les options suivantes :

    Menu basique accessible
    Musique d’attente lors-ce que l’utilisateur est tout seul
    Annonce du nombre de participant

Nous aurons ensuite une salle 920, pareille que la salle 910 mais avec un mot de passe.
Quant à la salle 930, les utilisateurs du contexte dept_1 y accèdent en mode admin, alors que les utilisateurs du contexte dept_2 y accèdent en mode utilisateur.

Par conséquent, ils ne fourniront pas le même mot de passe à l’entrée.
Par ailleurs, si un utilisateur accède à une conférence en mode admin, et que celle-ci n’a pas de mot de passe admin de configuré, l’utilisateur devra fournir le mot de passe classique.

Si vous avez gardé un range pour les numéros spéciaux dans la numérotation de vos départements, vous pouvez fournir une à plusieurs salles de conférence spécifiques à chaque département.

Par exemple en réservant les 10 derniers numéros :
Dept_1 :

    Numéro 190 : salle 190, sans MDP
    Numéro 191 : salle 191, avec MDP

Dept_2 :

    Numéro 290 : salle 290, sans MDP
    Numéro 291 : salle 291, avec MDP

3) Confbridge
-------------

La configuration de ConfBridge repose sur deux fichiers :

    extensions.conf
    confbridge.conf

 Voici un exemple de configuration pour confbridge.conf

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

Nous retrouvons la définition de trois profils d’utilisateurs.
Le premier permet d’entrer dans une salle de conférence sans authentification, le deuxième nécessite d’entrer un mot de passe et le troisième permet d’entrer en tant qu’admin.

Dans les trois cas, une musique d’attente est jouée si la salle est vide. De plus, le nombre d’utilisateurs présents dans la salle est annoncé lors de la connexion.
Ensuite, deux salles sont définies. L’une peut accueillir 10 utilisateurs et l’autre 100.

Voici à présent en exemple de configuration pour le fichier extensions.conf

exten => 900,1,ConfBridge(Room_1,ConfRoom_1,User_NoAuth)
exten => 901,1,ConfBridge(Room_1,ConfRoom_1,User_Admin)

exten => 903,1,ConfBridge(Room_2,ConfRoom_2,User_Auth)
exten => 904,1,ConfBridge(Room_2,ConfRoom_2,User_Admin)

Les paramètres de Confbridge en parenthèse fonctionnent comme suit :
1er paramètre : nom de la salle. Ne fait pas référence au contenu de Confbridge.conf.
2e paramètre : salle à rejoindre lors ce que l’on compose le numéro
3e paramètre : profil d’utilisateur

Ainsi, si quelqu’un compose le 900, il pourra entrer dans la salle ConfRoom1 avec le profil User_NoAuth.

Si quelqu’un compose le 903, il pourra entrer dans la salle ConfRoom2 avec le profil User_Auth (un code pin lui sera alors demandé).

