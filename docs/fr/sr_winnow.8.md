SR\_Winnow
==========

Supprimer des avis redondants
-----------------------------

Manual section

:   8

Date

:   @Date@

Version

:   @Version@

Manual group

:   MetPX-Sarracenia

### SYNOPSIS

**sr\_winnow** foregroundstopreloaddeclare\|setup configfile

### DESCRIPTION

sr\_winnow\*\* est un programme qui s'abonne aux notifications de
fichiers, et réenregistre les notifications, en supprimant les
notifications redondantes en comparant leurs données L'en-tête
**sum**\*\* mémorise l'empreinte digitale d'un fichier comme décrit
ci-dessus. dans la page de manuel [sr\_post(7)](sr_post.7.md)

**sr\_winnow** est un [sr\_subscribe(1)](sr_subscribe.1.md) avec les
options suivantes forcées:

    no-download True  
    suppress_duplicates on
    accept_unmatch True

La durée de vie des suppress\_duplicates peut être ajustée, mais elle
est toujours active.

**sr\_winnow** se connecte à un *courtier* (souvent le même que le
courtier d'affichage). et souscrit aux notifications d'intérêt. Sur
réception d´un avis, il cherche sa **sum** dans son cache. s'il est
trouvé, le fichier est déjà passé, de sorte que la notification est
ignorée. Si ce n'est pas le cas, le fichier est nouveau, et le **sum**
est ajouté. dans le cache et l'avis est affiché.

**sr\_winnow** peut être utilisé pour couper les messages de
[sr\_post(1)](sr_post.1.md), [sr\_poll(1)](sr_poll.1.md) ou
[sr\_watch(1)](sr_watch.1.md) etc..... C'est utilisé lorsqu'il y a
plusieurs sources de données identiques, de sorte que les clients ne
téléchargent que le fichier une seule fois, à partir de la première
source qui les a publié.

La commande **sr\_winnow** prend deux arguments : une action
startstopreload\|status..... (auto-descriptif?) suivi d'un fichier de
configuration décrit ci-dessous.

Le **foreground** est utilisé lors du débogage d'une configuration,
lorsque l'utilisateur souhaite exécuter le programme et son fichier de
configuration de manière interactive.

Les actions **cleanup**, **declare**, **setup**, **setup** peuvent être
utilisées pour gérer les ressources sur le serveur rabbitmq. Les
ressources sont soit des files d'attente, soit des échanges. **declare**
crée les ressources. **setup** crée et fait en plus les liaisons des
files d'attente.

### CONFIGURATION

En général, les options de cette composante sont décrites dans le manuel
de l [sr\_subscribe(1)](sr_subscribe.1.md) page qui doit être lue en
premier. Il explique en détail la langue de configuration de l'option,
et comment trouver les paramètres de l'option.

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
