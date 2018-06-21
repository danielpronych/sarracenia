SR\_Report
==========

traiter les rapport de télémétrie
---------------------------------

Manual section

:   1

Date

:   @Date@

Version

:   @Version@

Manual group

:   Metpx-Sarracenia Suite

### SYNOPSIS

> **sr\_report** foregroundstopreload\|status configfile
>
> **sr\_report** cleanupsetup configfile

### DESCRIPTION

sr\_report est un programme pour traiter efficacement les rapports de
transferts de fichiers à partir de Sarracenia. Le format des rapports
est indiqué dans le *man page* [sr\_report(7)](sr_report.7.md) Lorsque
les clients téléchargent un message à partir d'un site de Sarracenia,
ils publient un message d´information sur leur succès à le faire.

La commande **sr\_report** prend deux arguments : un fichier de
configuration décrit ci-dessous, suivi d'une action, l'une des actions
suivantes : startrestartreload\|status ou foreground..... (auto-décrit).
sr\_report est sr\_subscribe avec les paramètres suivants modifiés: :

> no\_download On topic-prefix v02.report cache off accept\_unmatch On
> report\_back off

L'action **foreground** est différente. Il est utilisé lors de la
construction d'une configuration. ou déboguer des choses, quand
l'utilisateur veut exécuter le programme et son fichier de
configuration. interactivement... L'instance **foreground** n'est pas
concernée par d'autres actions, mais si les instances configurées sont
en cours d'exécution, il partage la même file d'attente de messages
(configurée).

Les actions **cleanup**, **declare**, **setup**, **setup** peuvent être
utilisées pour gérer les ressources sur le serveur rabbitmq. Les
ressources sont soit des files d'attente, soit des échanges. **declare**
crée les ressources. **setup** crée et fait en plus les liaisons des
files d'attente.

### CONFIGURATION

En général, les options de cette composante sont décrites dans le manuel
de l [sr\_subscribe(1)](sr_sr_subscribe.1.md) page qui doit être lue en
premier. Il explique en détail la langue de configuration de l'option,
et comment trouver les paramètres de l'option.

#### EXEMPLES

Voici un court exemple complet de fichier de configuration:

    broker amqp://dd.weather.gc.ca/

    subtopic model_gem_global.25km.grib2.#
    accept .*

Celui-ci se connectera au courtier dd.weather.gc.ca, en tant que
anonymous avec mot de passe anonymous (par défaut) pour obtenir des
annonces à propos de dans le répertoire
<http://dd.weather.gc.ca/model_gem_global/25km/grib2>. Tous les rapports
de téléchargements de ces fichiers présents sur la pompe sera accepté
pour traitement par sr\_report.

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
