SR\_Sarra
=========

Selectionner, acquérir et renvoyer récursivement a autrui
---------------------------------------------------------

Manual section

:   8

Date

:   @Date@

Version

:   @Version@

Manual group

:   MetPx Sarracenia Suite

### SYNOPSIS

**sr\_sarra** foregroundstopreload\|status configfile

**sr\_sarra** cleanupsetup configfile

### DESCRIPTION

**sr\_sarra** est un programme qui s'abonne aux notifications de
fichiers, Acquiert les fichiers et les annonce à leurs nouveaux
emplacements. Le protocole de notification est défini ici
[sr\_post(7)](sr_post.7.md)

**sr\_sarra** se connecte à un *broker* (souvent le même que le serveur
de fichiers distant) ) et s´abonne aux notifications d'intérêt. Il
utilise l'avis des informations pour télécharger les fichier au serveur
local. Il envoie ensuite un avis pour les fichiers téléchargés sur un
courtier (généralement aussi sur le serveur local).

**sr\_sarra** peut être utilisé pour acquérir des fichiers à partir de
[sr\_post(1)](sr_post.1.md) ou [sr\_watch(1)](sr_watch.1.md) ou pour
réproduire un dossier accessible sur le Web (WAF), qui annoncent ses
produits.

Le **sr\_sarra** est un [sr\_subscribe(1)](sr_subscribe.1.md) avec les
presets suivants:

    mirror True

#### Besoins spécifiques de consommation

Si les messages sont affichés directement à partir d'une source,
l'échange utilisé est'[xs]()\<brokerSourceUsername\>\_\<xxz\>'. Un tel
message peut ne pas contenir une source ni une grappe d'origine, ou un
utilisateur malveillant peut régler les valeurs incorrectement. Pour se
protéger contre les paramètres malveillants, les administrateurs doit
setté *source\_from\_exchange* à **True**.

-   **source\_from\_exchange \<boolean\> (par défaut : False)**.

Lors de la réception, le programme réglera les valeurs suivantes dans la
classe mère (ici le cluster est la valeur de option **cluster** extraite
du fichier default.conf) :

self.msg.headers\['source'\] = \<brokerUser\>User\>.
self.msg.headers\['from\_cluster'\] = cluster

Ceux-ci prime sur les valeurs présentes dans le message. Ce réglage
devrait toujours être utilisé lors de l'ingestion de données provenant
d'une échange d'un utilisateur.

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
