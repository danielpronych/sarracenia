SR\_Log2Save
============

Lire un fichier log pour créé un save
-------------------------------------

Manual section

:   8

Date

:   @Date@

Version

:   @Version@

Manual group

:   Metpx-Sarracenia Suite

### SYNOPSIS

> **sr\_log2save**

### DESCRIPTION

Afin de renvoyer des articles à une destination donnée, on peut
récupérer l'avis pour un fichier donné, avec une entrée de fichier
journal standard pour ce fichier. *sr\_log2save* lit le journal et les
écrire dans la sortie standard convertie (json) dans le fichier
enregistrer le format utilisable par *sr\_shovel* avec
*-restore\_to\_queue*.

#### EXEMPLE

exemple:

    cat ~/test/save.conf <<EOT

    broker amqp://tfeed@localhost/
    topic_prefix v02.post
    exchange xpublic

    post_rate_limit 5
    on_post post_rate_limit 

    post_broker amqp://tfeed@localhost/

    EOT

    sr_log2save <log/sr_sarra_download_0003.log >shovel/save/sr_shovel_save_0000.save
    sr_shovel -restore_to_queue q_tsub.sr_subscribe.t.99524171.43129428 foreground save.conf 

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
