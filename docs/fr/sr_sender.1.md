SR\_Sender
==========

Envoyer des fichiers publiés à des serveurs distants
----------------------------------------------------

Manual section

:   1

Date

:   @Date@

Version

:   @Version@

Manual group

:   MetPX-Sarracenia

### DESCRIPTION

**sr\_sender** est un composant dérivé de
[sr\_subscribe(1)](sr_subscribe.1.md) utilisé pour envoyer des fichiers
locaux à un serveur distant, principalement avec SFTP. **sr\_sender**
est un consommateur standard, utilisant tous les paramètres AMQP normaux
pour les courtiers, les bourses, les files d'attente, et tout le
filtrage standard côté client avec *accept*, *reject*, et *on\_message.*

Souvent, un courtier annoncera les fichiers à l'aide d'un protocole
réseau tel que HTTP, mais pour l'expéditeur, il s'agit en fait d'un
fichier local. Dans de tels cas, on pourra voir un message : **ERROR :
The file to send is not local.** Un plugin on message convertira l'url
web en fichier local: :

> base\_dir /var/httpd/www on\_message msg\_2localfile msg\_2localfile

Ce plugin on\_message fait partie des paramètres par défaut pour les
expéditeurs, mais un plugin doit encore spécifier base\_dir pour qu'il
fonctionne.

Si un **post\_broker** est défini, **sr\_sender** vérifie si le nom de
grappe indiqué par l'option **to** se trouve dans l'un des groupes de
destination du message. Si ce n'est pas le cas, le message est ignoré
(le fichier n´est pas envoyé.)

#### DESTINATION INDISPONIBLE

Si le serveur auquel les fichiers sont envoyés va être indisponible pour
une période prolongée, et il ya un grand nombre de messages à leur
envoyer, puis la file d'attente s'accumulera sur le courtier. Comme la
performance de l'ensemble du courtier est affecté par de grandes files
d'attente, il faut minimiser ces files d'attente.

Les options *-save* et *-restore* sont utilisées pour éloigner les
messages du courtier. alors qu'une file d'attente trop longue
s'accumulera certainement. L'option *-save* copie les messages dans un
fichier disque (par instance) (dans le même répertoire). qui stocke les
fichiers state et pid), sous forme de chaînes codées json, une par
ligne. Quand une file d'attente s'accumule:

    sr_sender stop <config>
    sr_sender -save start <config>

Et exécutez l'expéditeur en mode *save* (qui écrit continuellement les
messages entrants sur le disque). dans le journal, une ligne pour chaque
message écrit sur le disque:

    2017-03-03 12:14:51,386 [INFO] sr_sender saving 2 message topic: v02.post.home.peter.sarra_devdocroot.sub.SASP34_LEMM_031630__LEDA_60215

Continuez dans ce mode jusqu'à ce que le serveur absent soit à nouveau
disponible. A ce moment-là:

    sr_sender stop <config> 
    sr_sender -restore start <config> 

Lors de la restauration à partir du fichier disque, des messages tels
que les suivants apparaîtront dans le journal:

    2017-03-03 12:15:02,969 [INFO] sr_sender restoring message 29 of 34: topic: v02.post.home.peter.sarra_devdocroot.sub.ON_02GD022_daily_hydrometric.csv

après le dernier, on verra:

    2017-03-03 12:15:03,112 [INFO] sr_sender restore complete deleting save file: /home/peter/.cache/sarra/sender/tsource2send/sr_sender_tsource2send_0000.save 

et le sr\_sender fonctionnera normalement par la suite.

#### EXEMPLE 1 : REPLICATION POMPE À POMPE

> -   **mirror \<boolean\> (default: True)**
> -   **base\_dir \<directory\> (None)**
> -   **destination \<url\> (MANDATORY)**
> -   **do\_send \<script\> (None)**
> -   **kbytes\_ps \<int\> (default: 0)**
> -   **post\_base\_dir \<directory\> (default: '')**
> -   **to \<clustername\> (default: \<post\_broker host\>)**
> -   **on\_post \<script\> (default: None)**
> -   **post\_broker
>     amqp{s}://\<user\>:\<pw\>@\<brokerhost\>\[:port\]/\<vhost\>**
> -   **url \<url\> (default: destination)**

Pour la duplication de données d´une pompe a une autres, **mirror** est
réglé sur True (par défaut).

**base\_dir** fournit le chemin d'accès au répertoire qui, lorsqu'il est
combiné avec le chemin d'accès relatif. un dans la notification
sélectionnée donne le chemin absolu du fichier à envoyer. La valeur par
défaut est None, ce qui signifie que le chemin d'accès dans la
notification est le chemin absolu.

La **destination** définit le protocole et le serveur à utiliser pour
livrer les produits. Sa forme est une url partielle, par exemple :
**<ftp://myuser@myhost>**\*\* Le programme utilise le fichier
\~/.conf/sarra/credentials.conf pour obtenir les détails restants. (mot
de passe et options de connexion). Les protocoles supportés sont ftp,
ftps et sftp. Si le l'utilisateur a besoin d'implémenter un autre
mécanisme d'envoi, il fournirait le script du plugin. par l'option
**do\_send**.

Sur le site distant, le **post\_base\_dir** sert aux mêmes fins que le
**base\_dir** sur ce serveur. La valeur par défaut est None, ce qui
signifie que le chemin d'accès délivré est absolu. Maintenant, nous
sommes prêts à envoyer le produit..... Par exemple, si la notification
sélectionnée ressemble à ceci :

**2015081316161959.854 <http://this.pump.com/>
relative/path/to/IMPORTANT\_produit**\*\*.

**sr\_sender** effectue la pseudo-livraison suivante :

envoie le fichier
local\[**base\_dir**\]/relative/path/to/IMPORTANT\_product à
**destination**/\[**post\_base\_dir**\]/relative/path/to/IMPORTANT\_product
(**kbytes\_ps** est supérieur à 0, le processus tente de respecter cette
vitesse de livraison... ftp,ftps,ftps,ou sftp)

A ce stade, un besoin de configuration de pompe à pompe doit envoyer la
notification à distance..... (Si le post\_broker n'est pas défini, il
n'y aura pas de publication.... juste la réplication de produits)

L´avis contient toutes les mêmes informations (attributs de thème et
autres en-têtes), à l'exception du champ url, dans notre exemple.. :
**<http://this.pump.com/>**\*\*

Par défaut, **sr\_sender** met la **destination** dans ce champ.
L'utilisateur peut écraser ceci en spécifiant l'option
**post\_base\_url**. Par exemple :

**post\_base\_url <http://remote.apache.com>**

L'utilisateur peut fournir un script **on\_post**. Juste avant que le
message n'arrive publier au **post\_broker** et **post\_exchange**, le
routine **on\_post** est appelé.... avec l'instance de classe
**sr\_sender** comme argument. Le script peut effectuer tout ce que vous
voulez.... s'il renvoie False, le message ne sera pas être publié. Si
Vrai, le programme continuera le traitement.

#### EXEMPLE 2: DISSEMINATION ( STYLE SUNDEW )

Dans ce type d'utilisation, nous ne repost généralement pas.... mais si
la fonction **post\_broker** et **post\_exchange**
(**url**,\**on\_post*\*) sont définis, le produit sera annoncé (avec
éventuellement un nouvel emplacement et un nouveau nom) Réintroduire les
options dans un ordre différent. avec de nouvelles pour faciliter
l'explication.

> -   **mirror \<boolean\> (défaut: True)**
> -   **base\_dir \<directory\> (défaut: None)**
> -   **destination \<url\> (OBLIGATOIRE)**
> -   **post\_base\_dir \<directory\> (défaut: '')**
> -   **directory \<path\> (OBLIGATOIRE)**
> -   **on\_message \<script\> (défaut: None)**
> -   **accept \<regexp pattern\> (défaut: None)**
> -   **reject \<regexp pattern\> (défaut: None)**

Il y a 2 différences avec le cas précédent : le répertoire\****, et les
optionsnom de fichier. Lebase\_dir*\* est le même, et il en va de même
pour le**destination\*\* et les options **post\_base\_dir**.

L'option **répertoire** définit un autre "chemin relatif" pour le
produit. à sa destination. Il est marqué aux options **accept** définies
après lui. Si une autre séquence de **répertoire/**accept\*\* suit dans
le fichier de configuration, le deuxième répertoire est étiqueté aux
acceptations suivantes et ainsi de suite.

Les modèles **accept/reject** s'appliquent à l'url d'avis de message
comme ci-dessus. Voici un exemple, voici quelques options de
configuration ordonnées.. :

    directory /my/new/important_location

    accept .*IMPORTANT.*

    directory /my/new/location/for_others

    accept .*

l'avis en cause:

**20150813161959.854 <http://this.pump.com/>
relative/path/to/IMPORTANT\_product**

Le fichier a été sélectionné par la première option **accept**. Le
chemin relatif distant devient **/my/new/important\_location** .... et
**sr\_sender** effectue la pseudo-livraison suivante :

envoie le fichier
local\[**base\_dir**\]/relative/path/to/IMPORTANT\_product à
**destination**/\[**post\_base\_dir**\]/my/new/important\_location/IMPORTANT\_product

Habituellement, cette façon d'utiliser **sr\_sender** ne nécessite pas
de publication du produit. Mais si **post\_broker** et
**post\_exchange** sont fournis, et **post\_base\_url**, comme
ci-dessus, est réglé sur **<http://remote.apache.com>**, que
**sr\_sender** reconstruirait :

Topic (thème):
**v02.post.my.new.important\_location.IMPORTANT\_product**

Avis: **20150813161959.854 <http://remote.apache.com/>
my/new/important\_location/IMPORTANT\_product**

### AUSSI VOIR

[sr\_subscribe(1)](sr_subscribe.1.md) - Sélectionner et télécharger des
fichiers publiés.

[sr\_shovel(8)](sr_shovel.8.md) - copier des avis (pas les fichiers).

[sr\_winnow(8)](sr_winnow.8.md) - une sr\_shovel(1) avec *cache* pour
vaner (séparer le blé de l'ivraie.)

[sr\_sender(1)](sr_sender.1.md) - s'abonne aux avis des fichiers
locaux, envoie les aux systèmes distants, et les publier à nouveau.

[sr\_report(1)](sr_report.1.md) - messages de rapport de processus.

[sr\_post(1)](sr_post.1.md) - publier les avis de fichiers.

[sr\_watch(1)](sr_watch.1.md) - sr\_post(1) en boucle, veillant sur les
répertoires.

[sr\_sarra(8)](sr_sarra.8.md) - Outil pour S´abonner, acquérir, et
renvoyer récursivement ad nauseam.

[sr\_post(7)](sr_post.7.md) - Le format des avis (messages d'annonce
AMQP)

[sr\_report(7)](sr_report.7.md) - le format des messages de rapport.

[sr\_pulse(7)](sr_pulse.7.md) - Le format des messages d'impulsion.

[<https://github.com/MetPX/>](https://github.com/MetPX) - sr\_subscribe
est un composant de MetPX-Sarracenia, la pompe de données basée sur
AMQP.
