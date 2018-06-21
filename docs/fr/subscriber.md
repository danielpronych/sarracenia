Guide d´abonnés
===============

Recevoir des données d´une pompe MetPX-Sarracenia
-------------------------------------------------

\[ [English version](../subscriber.md) \]

### Revision Record

Quand on visionne le document dans un dépôt git, on utilise celui-ci
pour suivre la version. Cette section sert uniquement lors de la
production d´un document sur papier. Durant sa préparation les champs
ci-dessous vont être remplacés par les valeurs approprié.

version

:   @Version@

date

:   @Date@

### Introduction

Une pompe de données Sarracenia est un serveur web avec des avis publiés
quand les fichiers servi changent. Pour savoir quelles données sont déjà
disponibles sur une pompe, on peut visualiser l'arbre à l'aide d'un
furreteur web. Pour des besoins immédiats simples, on peut télécharger
des données à l'aide du fureteur lui-même, ou un outil standard tel que
wget. L'intention habituelle est d´utiliser sr\_subscribe pour
automatiquement télécharger les données souhaitées sur une base
régulière et automatisé, et permettre traitement par d´autre logiciels.
Noter:

-   L'outil est entièrement piloté en ligne de commande (il n'y a pas
    d'interface graphique) Plus précisément, il est principalement
    piloté par des fichiers de configuration. la plupart de
    l´\*interface\* implique l'utilisation d'un éditeur de texte pour
    modifier les fichiers de configuration.
-   tout en étant écrit pour être compatible avec d'autres
    environnements, l'accent est mis sur l'utilisation en Linux.
-   l'outil peut être utilisé soit comme outil de l'utilisateur final,
    soit comme moteur de transfert à l'échelle du système.
-   Ce guide est axé sur le cas de l'utilisateur final.
-   Des documents de référence plus détaillés sont disponibles à
    l'adresse suivante [sr\_subscribe(1)](sr_subscribe.1.md)
-   Toute la documentation du paquet est disponible. à l'adresse
    <https://github.com/MetPX>

Alors que Sarracénie peut fonctionner avec n'importe quelle arborescence
web, ou n'importe quelle URL que les sources choisissent d'afficher, il
y a une mise en page conventionnelle. Le serveur Web d'une pompe de
données ne fera qu'exposer les dossiers accessibles sur le Web et la
racine de l'arbre est la date, au format AAAAMMJJJ. Ces dates ne
représentent quand il a été mis dans le réseau de pompage, et Sarracenia
utilise toujours le temps universel coordonné, les dates peuvent ne pas
correspondre à la date et l'heure actuelles dans la localité de
l'abonné:

    Index of /

    Icon  Name                    Last modified      Size  Description
    [PARENTDIR] Parent Directory                             -   
    [DIR] 20151105/               2015-11-27 06:44    -   
    [DIR] 20151106/               2015-11-27 06:44    -   
    [DIR] 20151107/               2015-11-27 06:44    -   
    [DIR] 20151108/               2015-11-27 06:44    -   
    [DIR] 20151109/               2015-11-27 06:44    -   
    [DIR] 20151110/               2015-11-27 06:44    -  

Un nombre variable de jours est stocké sur chaque pompe de données. Les
pompes qui mettent l'accent sur la fiabilité de la livraison en temps
réel, aura moins de jours en ligne. Pour d'autres pompes, lorsque des
pannes de plus longue durée sont nécessaires à tolérer, plus de jours
seront conservés.

Sous le premier niveau de l'arborescence par dates, il y a un répertoire
par source. Une Source en Sarracenia est un compte utilisé pour ajouter
de donnée dans le réseau de pompes. Les données peuvent traverser de
nombreuses pompes sur leur chemin vers celui qui est visible pour un
abonné en particulier:

    Index of /20151110

    Icon  Name                    Last modified      Size  Description
    [PARENTDIR] Parent Directory                             -   
    [DIR] UNIDATA-UCAR/           2015-11-27 06:44    -   
    [DIR] NOAAPORT/               2015-11-27 06:44    -   
    [DIR] MSC-CMC/                2015-11-27 06:44    -   
    [DIR] UKMET-RMDCN/            2015-11-27 06:44    -   
    [DIR] UKMET-Internet/         2015-11-27 06:44    -   
    [DIR] NWS-OPSNET/             2015-11-27 06:44    -  

Les données de chacun de ces répertoires ont été obtenues à partir de la
base de données nommée source. Dans ces exemples, il est en fait injecté
par la groupe DataInterchange de Services Partagés Canada, et les noms
sont choisis pour représenter l'origine des données.

Vous devriez pouvoir lister les configurations disponibles avec
*sr\_subscribe list* :

    blacklab% sr_subscribe list

    packaged plugins: ( /usr/lib/python3/dist-packages/sarra/plugins ) 
             __pycache__     destfn_sample.py       download_cp.py       download_dd.py 
         download_scp.py     download_wget.py          file_age.py        file_check.py 
             file_log.py       file_rxpipe.py        file_total.py          hb_cache.py 
               hb_log.py         hb_memory.py          hb_pulse.py         html_page.py 
             line_log.py         line_mode.py         msg_2http.py        msg_2local.py 
       msg_2localfile.py     msg_auditflow.py     msg_by_source.py       msg_by_user.py 
            msg_delay.py        msg_delete.py      msg_download.py          msg_dump.py 
           msg_fdelay.py msg_filter_wmo2msc.py  msg_from_cluster.py     msg_hour_tree.py 
              msg_log.py     msg_print_lag.py   msg_rename4jicc.py    msg_rename_dmf.py 
    msg_rename_whatfn.py       msg_renamer.py msg_replace_new_dir.py          msg_save.py 
         msg_skip_old.py        msg_speedo.py msg_sundew_pxroute.py    msg_test_retry.py 
      msg_to_clusters.py         msg_total.py        part_check.py  part_clamav_scan.py 
           poll_pulse.py       poll_script.py    post_hour_tree.py          post_log.py 
       post_long_flow.py     post_override.py   post_rate_limit.py        post_total.py 
            watch_log.py 
    configuration examples: ( /usr/lib/python3/dist-packages/sarra/examples/subscribe ) 
                all.conf     all_but_cap.conf            amis.conf            aqhi.conf 
                cap.conf      cclean_f91.conf       cdnld_f21.conf       cfile_f44.conf 
           citypage.conf           clean.conf       clean_f90.conf            cmml.conf 
    cscn22_bulletins.conf         ftp_f70.conf            gdps.conf         ninjo-a.conf 
              q_f71.conf           radar.conf            rdps.conf            swob.conf 
              t_f30.conf      u_sftp_f60.conf 

    user plugins: ( /home/peter/.config/sarra/plugins ) 
            destfn_am.py         destfn_nz.py       msg_tarpush.py 

    general: ( /home/peter/.config/sarra ) 
              admin.conf     credentials.conf         default.conf

    user configurations: ( /home/peter/.config/sarra/subscribe )
         cclean_f91.conf       cdnld_f21.conf       cfile_f44.conf       clean_f90.conf 
            ftp_f70.conf           q_f71.conf           t_f30.conf      u_sftp_f60.conf 

    blacklab% 

Chaque section de la liste montre le contenu du répertoire entre
parenthèses. il suffit d'éditer les fichiers dans les répertoires
directement, ou de les modifier autrement, car la commande list existe
seulement pour des raisons de commodité. Il y a quatre sections:

> -   plugins système : routines python que l'on peut appeler à partir
>     de la configuration de l'abonné.
> -   plugins utilisateur : routines python écrites par l'utilisateur du
>     même type.
> -   général : fichiers de configuration qui sont référencés par
>     d'autres fichiers de configuration.
> -   configurations utilisateur : ce sont celles définies par
>     l'utilisateur et le plus souvent d'intérêt.

Pour visualiser une configuration particulière, donnez à sr\_subscribe
la liste des fichiers en argument:

    blacklab% sr_subscribe list msg_log.py

``` sourceCode
#!/usr/bin/python3

"""
  the default on_msg handler for sr_log.
  prints a simple notice.

"""

class Msg_Log(object):

    def __init__(self,parent):
        parent.logger.debug("msg_log initialized")

    def on_message(self,parent):
        msg = parent.msg
        parent.logger.info("msg_log received: %s %s%s topic=%s lag=%g %s" % \
           tuple( msg.notice.split()[0:3] + [ msg.topic, msg.get_elapse(), msg.hdrstr ] ) )
        return True


msg_log = Msg_Log(self) # required: Make instance of class whose name is lower case version of class.

self.on_message = msg_log.on_message  # assign self.on_message to corresponding function.

blacklab%
```

### Un premier exemple

L'arbre décrit ci-dessus est l'arbre *conventionnel* que l'on trouve sur
la plupart des pompes de données, mais la pompe de données originale,
dd.weather.gc.ca, est antérieure à la convention. Indépendamment de
l'arbre, on peut le parcourir pour trouver les données d'intérêt. Sur
dd.weather.gc.ca, on peut naviguer jusqu'à
<http://dd.weather.gc.ca/observations/swob-ml/> pour trouver l'arbre de
toutes les observations météorologiques au format SWOB publié récemment
par n'importe quel bureau de prévision d'Environnement Canada.

Initialisez d'abord le fichier de stockage des informations
d'identification:

    blacklab% sr_subscribe edit credentials.conf

    amqp://anonymous:anonymous@dd.weather.gc.ca

La commande *edit* appelle simplement l'éditeur configuré de
l'utilisateur. sur le fichier à créer au bon endroit. Pour créer une
configuration pour obtenir les fichiers swob:

    blacklab% sr_subscribe edit swob.conf

    broker amqp://anonymous@dd.weather.gc.ca
    subtopic observations.swob-ml.#
    accept .*

    blacklab% 
    blacklab% sr_subscribe status swob
    2017-12-14 06:54:54,010 [INFO] sr_subscribe swob 0001 is stopped
    blacklab% 

NOTE :

> Ce qui précède écrira les fichiers dans le répertoire de travail
> courant, et ils arriveront rapidement. Il peut être plus avantageux de
> créer un répertoire dédié et d'utiliser l'option *directory* pour y
> placer les fichiers. par exemple : mkdir
> /tmp/swob\_downloads\_downloads *directory /tmp/swob\_downloads*

Sur la première ligne, *broker* indique l'endroit où se connecter pour
obtenir le service de notifications. Le terme *broker* est tiré de
l'AMQP (<http://www.amqp.org>), qui est le protocole utilisé pour
transférer les notifications. Les notifications qui seront reçues ont
toutes des thèmes ( *topic* ) qui correspondent au chameni relatif du
fichier annoncé.

Démarrez maintenant un abonné (supposons que le fichier de configuration
s'appelait dd\_swob.conf):

    blacklab% sr_subscribe start dd_swob
    2015-12-03 06:53:35,268 [INFO] user_config = 0 ../dd_swob.conf
    2015-12-03 06:53:35,269 [INFO] instances 1 
    2015-12-03 06:53:35,270 [INFO] sr subscribe dd swob 0001 started

on peut surveiller l'activité avec la commande *log*:

    blacklab% sr_subscribe log dd_swob

    2015-12-03 06:53:35,635 [INFO] Binding queue q_anonymous.21096474.62787751 with key v02.post.observations.swob-ml.# to exchange xpublic on broker amqp://anonymous@dd.weather.gc.ca/
    2015-12-03 17:32:01,834 [INFO] user_config = 1 ../dd_swob.conf
    2015-12-03 17:32:01,835 [INFO] sr_subscribe start
    2015-12-03 17:32:01,835 [INFO] sr_subscribe run
    2015-12-03 17:32:01,835 [INFO] AMQP  broker(dd.weather.gc.ca) user(anonymous) vhost(/)
    2015-12-03 17:32:01,835 [INFO] AMQP  input :    exchange(xpublic) topic(v02.post.observations.swob-ml.#)
    2015-12-03 17:32:01,835 [INFO] AMQP  output:    exchange(xs_anonymous) topic(v02.report.#)

    2015-12-03 17:32:08,191 [INFO] Binding queue q_anonymous.21096474.62787751 with key v02.post.observations.swob-ml.# to exchange xpublic on broker amqp://anonymous@dd.weather.gc.ca/
    blacklab% 

Le sr\_subscribe obtiendra la notification et téléchargera le fichier
dans le répertoire répertoire de travail actuel. Comme le démarrage est
normale, cela signifie que l'option l'information d'authentification
était bonne. Les mots de passe sont stockés dans le répertoire le
fichier \~/.config/sarra/credentials.conf. Le format n'est qu'un url
complet sur chaque ligne. L'exemple ci-dessus serait:

    amqp://anonymous:anonymous@dd.weather.gc.ca/

Le mot de passe est situé après le :, et avant le @ dans l'URL comme
c'est la norme. la pratique. Ce fichier credentials.conf doit être privé
(permissions octales linux : 0600). De même, si un fichier.conf est
placé dans le répertoire \~/.config/sarra/subscribe, alors sr\_subscribe
le trouvera sans avoir à donner le chemin complet.

Un téléchargement normal ressemble à ceci:

    2015-12-03 17:32:15,031 [INFO] Received topic   v02.post.observations.swob-ml.20151203.CMED
    2015-12-03 17:32:15,031 [INFO] Received notice  20151203223214.699 http://dd2.weather.gc.ca/ \
           observations/swob-ml/20151203/CMED/2015-12-03-2200-CMED-AUTO-swob.xml
    2015-12-03 17:32:15,031 [INFO] Received headers {'filename': '2015-12-03-2200-CMED-AUTO-swob.xml', 'parts': '1,3738,1,0,0', \
          'sum': 'd,157a9e98406e38a8252eaadf68c0ed60', 'source': 'metpx', 'to_clusters': 'DD,DDI.CMC,DDI.ED M', 'from_cluster': 'DD'}
    2015-12-03 17:32:15,031 [INFO] downloading/copying into ./2015-12-03-2200-CMED-AUTO-swob.xml 

Donnant toutes les informations contenues dans la notification. Voici un
échec:

    2015-12-03 17:32:30,715 [INFO] Downloads: http://dd2.weather.gc.ca/observations/swob-ml/20151203/CXFB/2015-12-03-2200-CXFB-AUTO-swob.xml  into ./2015-12-03-2200-CXFB-AUTO-swob.xml 0-6791
    2015-12-03 17:32:30,786 [ERROR] Download failed http://dd2.weather.gc.ca/observations/swob-ml/20151203/CXFB/2015-12-03-2200-CXFB-AUTO-swob.xml
    2015-12-03 17:32:30,787 [ERROR] Server couldn't fulfill the request. Error code: 404, Not Found

Notez que ce message n'est pas toujours un échec, car sr\_subscribe
retries quelques fois avant d'abandonner. Quoi qu'il en soit, après
quelques minutes, voici ce qui suit le répertoire courant ressemble à:

    blacklab% ls -al | tail
    -rw-rw-rw-  1 peter peter   7875 Dec  3 17:36 2015-12-03-2236-CL3D-AUTO-minute-swob.xml
    -rw-rw-rw-  1 peter peter   7868 Dec  3 17:37 2015-12-03-2236-CL3G-AUTO-minute-swob.xml
    -rw-rw-rw-  1 peter peter   7022 Dec  3 17:37 2015-12-03-2236-CTRY-AUTO-minute-swob.xml
    -rw-rw-rw-  1 peter peter   6876 Dec  3 17:37 2015-12-03-2236-CYPY-AUTO-swob.xml
    -rw-rw-rw-  1 peter peter   6574 Dec  3 17:36 2015-12-03-2236-CYZP-AUTO-swob.xml
    -rw-rw-rw-  1 peter peter   7871 Dec  3 17:37 2015-12-03-2237-CL3D-AUTO-minute-swob.xml
    -rw-rw-rw-  1 peter peter   7873 Dec  3 17:37 2015-12-03-2237-CL3G-AUTO-minute-swob.xml
    -rw-rw-rw-  1 peter peter   7037 Dec  3 17:37 2015-12-03-2237-CTBF-AUTO-minute-swob.xml
    -rw-rw-rw-  1 peter peter   7022 Dec  3 17:37 2015-12-03-2237-CTRY-AUTO-minute-swob.xml
    -rw-rw-rw-  1 peter peter 122140 Dec  3 17:38 sr_subscribe_dd_swob_0001.log
    blacklab% 

### Ressources côté serveur allouées aux abonnés

Chaque configuration a pour résultat que les ressources correspondantes
sont déclarées sur le broker. Quand on change les paramètres *subtopic*
ou *queue*, ou quand on s'attend à ne pas utiliser une configuration
pour une période de temps prolongée, il est préférable de faire:

    sr_subscribe cleanup swob.conf

qui dé-alloue la file d'attente (et ses liaisons) sur le serveur.
Pourquoi ? Chaque fois qu'un abonné est démarré, une file d'attente est
créée sur la pompe de données. Les liens de thème définis par le fichier
de configuration. Si l'abonné est arrêté, la file d'attente continue à
recevoir des messages tels que définis par la sélection de sous-thèmes,
et lorsque la commande de l'abonné repart, les messages en file
d'attente sont transmis au client.

Ainsi, lorsque l'option *subtopic* est modifiée, puisqu'elle est déjà
définie dans le fichier on finit par ajouter une liaison plutôt que de
la remplacer. Par exemple, si l'on a un sous-thème ( *subtopic* ) qui
contient SATELLITE, puis arrête l'abonné, éditer le fichier et
maintenant le thème ( *topic* ) ne contient plus que RADAR, lorsque
l'abonné est non seulement tous les fichiers satellites en file
d'attente seront envoyés au consommateur, mais le RADAR est ajouté aux
fixations, plutôt que de les remplacer. l'abonné obtiendra les données
SATELLITE et RADAR, même si la configuration ne contient plus le
premier.

Aussi, si l'on expérimente et qu'une file d'attente doit être arrêtée
pour une très longue durée Dans le temps, il peut accumuler un grand
nombre de messages. Le nombre total de messages sur une pompe de données
a un effet sur les performances de la pompe pour tous les utilisateurs.
Il est donc Il est conseillé de demander à la pompe de décharger les
ressources lorsqu'elles ne seront pas nécessaires. pendant des périodes
prolongées, ou lors d'expériences avec différents réglages.

### Utiliser plusierus configurations

Placez tous les fichiers de configuration, avec le suffixe.conf dans le
repertoire: \~/.config/sarra/sarra/subscribe/ Par exemple, s'il y a deux
fichiers dans ce répertoire : CMC.conf et NWS.conf, on pourrait alors
exécuter:

    peter@idefix:~/test$ sr_subscribe start CMC.conf 
    2016-01-14 18:13:01,414 [INFO] installing script validate_content.py 
    2016-01-14 18:13:01,416 [INFO] installing script validate_content.py 
    2016-01-14 18:13:01,416 [INFO] sr_subscribe CMC 0001 starting
    2016-01-14 18:13:01,418 [INFO] sr_subscribe CMC 0002 starting
    2016-01-14 18:13:01,419 [INFO] sr_subscribe CMC 0003 starting
    2016-01-14 18:13:01,421 [INFO] sr_subscribe CMC 0004 starting
    2016-01-14 18:13:01,423 [INFO] sr_subscribe CMC 0005 starting
    2016-01-14 18:13:01,427 [INFO] sr_subscribe CMC 0006 starting
    peter@idefix:~/test$ 

pour lancer la configuration de téléchargement CMC. On peut utiliser la
commande sr pour démarrer/arrêter plusieurs configurations à la fois. La
commande sr va passer par les répertoires par défaut et démarrer. toutes
les configurations qu'il trouve:

    peter@idefix:~/test$ sr start
    2016-01-14 18:13:01,414 [INFO] installing script validate_content.py 
    2016-01-14 18:13:01,416 [INFO] installing script validate_content.py 
    2016-01-14 18:13:01,416 [INFO] sr_subscribe CMC 0001 starting
    2016-01-14 18:13:01,418 [INFO] sr_subscribe CMC 0002 starting
    2016-01-14 18:13:01,419 [INFO] sr_subscribe CMC 0003 starting
    2016-01-14 18:13:01,421 [INFO] sr_subscribe CMC 0004 starting
    2016-01-14 18:13:01,423 [INFO] sr_subscribe CMC 0005 starting
    2016-01-14 18:13:01,416 [INFO] sr_subscribe NWS 0001 starting
    2016-01-14 18:13:01,416 [INFO] sr_subscribe NWS 0002 starting
    2016-01-14 18:13:01,416 [INFO] sr_subscribe NWS 0003 starting
    peter@idefix:~/test$ 

lancera certains processus sr\_subscribe tels que configurés par
CMC.conf et d'autres. pour correspondre à NWS.conf. Sr stop fera aussi
ce à quoi vous vous attendez. Tout comme le statut sr. Notez qu'il y a 5
processus sr\_subscribe qui commencent avec le CMC. et 3 NWS. Ce sont
des *instances* et partagent la même chose file d'attente de
téléchargement.

### Livraison prioritaire

Bien que le protocole sur la Sarracenia n'établisse pas explicitement un
ordre de priorité, l'utilisation de la de files d'attente multiples
offre des avantages similaires. Résultats de chaque configuration dans
une déclaration de file d'attente côté serveur. Grouper les produits à
priorité égale en une file d'attente en les sélectionnant à l'aide d'une
configuration commune. Plus les groupes sont petits, plus le délai de
traitement est faible. Alors que toutes les files d'attente sont
traitées avec la même priorité, les données passent plus rapidement par
des files d'attente plus courtes. On peut résumer avec:

    **Utiliser des configurations multiples pour établir des priorités**

Pour concrétiser les conseils, prenez l'exemple des données
d'Environnement Canada. mart ("dd.weather.gc.ca"), qui distribue des
binaires grillagés, le satellite GOES. des milliers de prévisions de
villes, d'observations, de produits RADAR, etc.... Pour le temps réel,
les alertes et les données RADAR sont la plus haute priorité. À certains
moments de la journée, ou en cas pannes, plusieurs centaines de milliers
de produits peuvent être en file d´attente et peut retarder la réception
de produits hautement prioritaires si une seule file d'attente est
utilisée.

Pour assurer un traitement rapide des données dans ce cas, définissez
une configuration pour vous abonner aux avertissements météorologiques
(qui sont un très petit nombre de produits), une seconde pour les RADARS
(un groupe plus grand mais encore relativement petit), et un troisième
(le plus grand groupe) pour tous les membres du les autres données.
Chaque configuration utilisera une file d'attente séparée. Les
avertissements seront les plus rapides, RADARS se mettront en file
d'attente les uns contre les autres, ce qui leur permettra de faire
l'expérience d'un certain nombre d'entre eux plus de retard, et d'autres
produits partageront une seule file d'attente et seront sujets à plus de
retard dans les cas délais.

<https://sourceforge.net/p/metpx/sarracenia/ci/master/tree/samples/config/ddc_hipri.conf>:

    broker amqp://dd.weather.gc.ca/
    mirror
    directory /data/web
    subtopic alerts.cap.#
    accept .*

<https://sourceforge.net/p/metpx/sarracenia/ci/master/tree/samples/config/ddc_normal.conf>:

    broker amqp://dd.weather.gc.ca/
    subtopic #
    reject .*alerts/cap.*
    mirror
    directory /data/web
    accept .*

Où vous voulez que le miroir du data mart commence à /data/web
(probablement qu'il y a un serveur web configurés pour afficher ce
répertoire.) Probablement, la configuration *ddc\_normal* (fournit comme
exemple) va connaître beaucoup de files d'attente, car il y a beaucoup
de données à télécharger. Le fichier *ddc\_hipri.conf* est seulement
abonné aux avertissements météorologiques dans le format du CAP, il y
aura donc peu ou pas de file d'attente pour ces données.

### Raffiner la sélection

... avertissement: : **FIXME** : Faire une diagramme, avec:

> -   le filtrage par sous-thème se fait sur le courtier ( *broker* )
> -   le accept/reject se fait dans le client sarracenia.

Choisissez *subtopics* (qui sont appliqués sur le courtier sans
téléchargement de messages) pour réduire le nombre de messages qui
traversent le réseau. Les options *reject* et *accept* sont évaluées par
les processus sr\_subscriber eux-mêmes, qui fournissent un filtrage des
avis transférés basé sur des expressions régulières. les expressions
dans les options *accept* et *reject* sont évalués contre sur le chemin
d'accès réel (l´URL local complet), indiquant quels fichiers publiés
devraient être téléchargés. Regardez dans les *Downloads*. du fichier
journal pour des exemples de ce chemin transformé.

Note

Brève introduction aux expressions régulières

Les expressions régulières sont un moyen très puissant d'exprimer les
correspondances de motifs. Ils offrent une flexibilité extrême, mais
dans ces exemples, nous utiliserons seulement un petit sous-ensemble :
Le point (.) est un joker qui correspond à n'importe quel caractère
unique. S'il est suivi d'un nombre d'occurrences, il indique le nombre
de lettres qui correspondent. Le caractère \* (astérisque), signifie un
nombre quelconque d'occurrences. alors :

> -   .\* signifie n'importe quelle séquence de caractères de n'importe
>     quelle longueur. En d'autres termes, faire correspondre n'importe
>     quoi.
> -   cap.\* signifie toute séquence de caractères commençant par cap.
> -   .*CAP.* signifie n'importe quelle séquence de caractères avec CAP
>     quelque part dedans.
> -   .\*CAP signifie toute séquence de caractères qui se termine par
>     CAP.
> -   Dans le cas où plusieurs portions de la chaîne de caractères
>     pourraient correspondre, la plus longue est sélectionnée.
> -   .*?CAP comme ci-dessus, mais*non-greedy\*, ce qui signifie que le
>     match le plus court est choisi.
> -   noter que l'implantaions de regexp en C n'inclu pas le
>     *greediness*, alors certains expressions ne seront pas interpretés
>     pareilles par les outils implanté en C: sr\_cpost, sr\_cpump, où
>     libsrshim.

Veuillez consulter diverses ressources Internet pour obtenir de plus
amples renseignements:

> -   [<https://docs.python.org/fr/3/library/re.html>](https://docs.python.org/fr/3/library/re.html)
> -   [<https://fr.wikipedia.org/wiki/Expression_r%C3%A9guli%C3%A8re>](https://fr.wikipedia.org/wiki/Expression_r%C3%A9guli%C3%A8re)

pour revenir aux exemples de fichiers de configuration :

Notez ce qui suit:

    blacklab% sr_subscribe edit swob

    broker amqp://anonymous@dd.weather.gc.ca
    subtopic observations.swob-ml.#
    directory /tmp
    mirror True
    accept .*
    #
    # instead of writing to current working directory, write to /tmp.
    # in /tmp. Mirror: create a hierarchy like the one on the source server.

On peut aussi intercaler les directives *directory* et *accept/reject*
pour construire des directives une hiérarchie de répertoires
arbitrairement différente de ce qui se trouvait sur la pompe de données
source. Le fichier de configuration est lu de haut en bas, donc
sr\_subscribe\_subscribe trouve un réglage de l'option *directory*,
seules les clauses *accept* après il fera en sorte que les fichiers
soient placés relativement à ce répertoire: :

> blacklab% sr\_subscribe edit ddi\_ninjo\_part1.conf
>
> broker amqp://ddi.cmc.ec.gc.ca/ subtopic ec.ops.*.*.ninjo-a.\#
>
> directory /tmp/apps/ninjo/import/point/reports/in accept .*ABFS\_1.0.*
> accept .*AQHI\_1.0.* accept .*AMDAR\_1.0.*
>
> directory /tmp/apps/ninjo/import/point/catalog\_common/in accept
> .*ninjo-station-catalogue.*
>
> directory /tmp/apps/ninjo/import/point/scit\_sac/in accept
> .*\~\~SAC,SAC\_MAXR.*
>
> directory /tmp/apps/ninjo/import/point/scit\_tracker/in accept
> .*\~\~TRACKER,TRACK\_MAXR.*

Dans l'exemple ci-dessus, les données du catalogue de ninjo-station sont
placées dans le répertoire catalog\_common/in, plutôt que dans le
répertoire *point/reports/in* ( la hiérarchie utilisée pour stocker les
données qui correspondent aux trois premiers clauses *accept* )

Note

Notez que .\* dans la directive subtopic, où cela signifie ´match
n'importe quel topic´ (c'est-à-dire qu'aucun caractère de point n'est
permis dans le fichier ) a une signification différente de celle qu'il a
dans une accept. où il s'agit de faire correspondre n'importe quelle
chaîne de caractères.

Oui, c'est déroutant. Non, on ne peut rien y faire.

### Plugins

Le traitement des fichiers par défaut est souvent très bien, mais il y a
aussi des personnalisations pré-construites qui peut être utilisé pour
modifier le traitement effectué par les composants. La liste des plugins
pré-construits est la suivante dans un répertoire 'plugins' où le paquet
est installé (visible avec *sr\_subscribe list*) sortie de
l'échantillon:

    blacklab% sr_subscribe list

    packaged plugins: ( /usr/lib/python3/dist-packages/sarra/plugins ) 
             __pycache__     destfn_sample.py       download_cp.py       download_dd.py 
         download_scp.py     download_wget.py          file_age.py        file_check.py 
             file_log.py       file_rxpipe.py        file_total.py          hb_cache.py 
               hb_log.py         hb_memory.py          hb_pulse.py         html_page.py 
             line_log.py         line_mode.py         msg_2http.py        msg_2local.py 
       msg_2localfile.py     msg_auditflow.py     msg_by_source.py       msg_by_user.py 
            msg_delay.py        msg_delete.py      msg_download.py          msg_dump.py 
           msg_fdelay.py msg_filter_wmo2msc.py  msg_from_cluster.py     msg_hour_tree.py 
              msg_log.py     msg_print_lag.py   msg_rename4jicc.py    msg_rename_dmf.py 
    msg_rename_whatfn.py       msg_renamer.py msg_replace_new_dir.py          msg_save.py 
         msg_skip_old.py        msg_speedo.py msg_sundew_pxroute.py    msg_test_retry.py 
      msg_to_clusters.py         msg_total.py        part_check.py  part_clamav_scan.py 
           poll_pulse.py       poll_script.py    post_hour_tree.py          post_log.py 
       post_long_flow.py     post_override.py   post_rate_limit.py        post_total.py 
            watch_log.py 
    configuration examples: ( /usr/lib/python3/dist-packages/sarra/examples/subscribe ) 
                all.conf     all_but_cap.conf            amis.conf            aqhi.conf 
                cap.conf      cclean_f91.conf       cdnld_f21.conf       cfile_f44.conf 
           citypage.conf           clean.conf       clean_f90.conf            cmml.conf 
    cscn22_bulletins.conf         ftp_f70.conf            gdps.conf         ninjo-a.conf 
              q_f71.conf           radar.conf            rdps.conf            swob.conf 
              t_f30.conf      u_sftp_f60.conf 

    user plugins: ( /home/peter/.config/sarra/plugins ) 
            destfn_am.py         destfn_nz.py       msg_tarpush.py 

    general: ( /home/peter/.config/sarra ) 
              admin.conf     credentials.conf         default.conf

    user configurations: ( /home/peter/.config/sarra/subscribe )
         cclean_f91.conf       cdnld_f21.conf       cfile_f44.conf       clean_f90.conf 
            ftp_f70.conf           q_f71.conf           t_f30.conf      u_sftp_f60.conf 

    blacklab% 

Pour tous les plugins, le préfixe indique comment le plugin doit être
utilisé : un file\_ plugin est à utiliser avec *on\_file*, les plugins
*Msg\_* sont à utiliser avec on\_message, etc.... Lorsque les plugins
ont des options, les options doivent être placées avant la déclaration
du plugin. dans le fichier de configuration:

    msg_total_interval 5
    on_message msg_total

Le plugin *msg\_total* est invoqué à chaque fois qu'un message est reçu,
et l´option *msg\_total\_interval*. utilisée par ce plugin, a été fixée
à 5. Pour en savoir plus : *sr\_subscribe list msg\_total.py*

Les plugins sont tous écrits en python, et les utilisateurs peuvent
créer leurs propres plugins et les placer directement dans
\~/.config/sarra/plugins. Pour plus d'informations sur la création de
nouveaux plugins personnalisés, consultez: [Guide de programmation de
Sarracenia](Prog.md)

pour récapituler :

-   Pour afficher les plugins actuellement disponibles sur le système
    *sr\_subscribe list*
-   Pour visualiser le contenu d'un plugin : *sr\_subscribe list
    \<plugin\>*
-   le début du plugin décrit sa fonction et ses paramètres
-   Les plugins peuvent avoir des paramètres d'options, tout comme les
    plugins intégrés
-   pour les définir, placez les options dans le fichier de
    configuration avant l'appel du plugin lui-même
-   pour créer votre propre plugin : *sr\_subscribe edit \<plugin\>.py*

### Exemple : file\_rxpipe

Le plugin file\_rxpipe pour sr\_subscribe fait en sorte que toutes les
instances écrivent les noms. de fichiers téléchargés dans un tube nommé.
La mise en place de ce système nécessitait deux lignes en un fichier de
configuration sr\_subscribe:

    blacklab% sr_subscribe edit swob 

    broker amqp://anonymous@dd.weather.gc.ca
    subtopic observations.swob-ml.#

    file_rxpipe_name /home/peter/test/.rxpipe
    on_file file_rxpipe
    directory /tmp
    mirror True
    accept .*
    # file_rxpipe est un plugin fourni avec Sarracenia qui écrit le nom de chaque fichier
    # téléchargé dans un *named pipe*

Avec l'option *on\_file*, on peut spécifier une option de traitement
telle que rxpipe. Avec rxpipe, chaque fois qu'un transfert de fichier
est terminé et qu'il est prêt pour post-traitement, son nom est écrit
dans le tube linux (nommé .rxpipe) dans le fichier répertoire de travail
actuel.

### Exemple : Analyse antivirus

Un autre exemple d'utilisation facile d'un plugin est de réaliser une
analyse antivirus. En supposant que ClamAV est installé, ainsi que
python3-pyclamd alors on peut ajouter les éléments suivants à un
sr\_subscribe fichier de configuration:

    broker amqp://dd.weather.gc.ca
    on_part part_clamav_scan.py
    subtopic observations.swob-ml.#
    accept .*

de sorte que chaque fichier téléchargé (ou chaque partie du fichier s'il
est volumineux), pour être scanné AV. Échantillon:

    blacklab% sr_subscribe --reset foreground ../dd_swob.conf 
    clam_scan on_part plugin initialized
    clam_scan on_part plugin initialized
    2016-05-07 18:01:15,007 [INFO] sr_subscribe start
    2016-05-07 18:01:15,007 [INFO] sr_subscribe run
    2016-05-07 18:01:15,007 [INFO] AMQP  broker(dd.weather.gc.ca) user(anonymous) vhost(/)
    2016-05-07 18:01:15,137 [INFO] Binding queue q_anonymous.sr_subscribe.dd_swob.13118484.63321617 with key v02.post.observations.swob-ml.# from exchange xpublic on broker amqp://anonymous@dd.weather.gc.ca/
    2016-05-07 18:01:15,846 [INFO] Received notice  20160507220115.632 http://dd3.weather.gc.ca/ observations/swob-ml/20160507/CYYR/2016-05-07-2200-CYYR-MAN-swob.xml
    2016-05-07 18:01:15,911 [INFO] 201 Downloaded : v02.report.observations.swob-ml.20160507.CYYR 20160507220115.632 http://dd3.weather.gc.ca/ observations/swob-ml/20160507/CYYR/2016-05-07-2200-CYYR-MAN-swob.xml 201 blacklab anonymous 0.258438 parts=1,4349,1,0,0 sum=d,399e3d9119821a30d480eeee41fe7749 from_cluster=DD source=metpx to_clusters=DD,DDI.CMC,DDI.EDM rename=./2016-05-07-2200-CYYR-MAN-swob.xml message=Downloaded 
    2016-05-07 18:01:15,913 [INFO] part_clamav_scan took 0.00153089 seconds, no viruses in ./2016-05-07-2200-CYYR-MAN-swob.xml
    2016-05-07 18:01:17,544 [INFO] Received notice  20160507220117.437 http://dd3.weather.gc.ca/ observations/swob-ml/20160507/CVFS/2016-05-07-2200-CVFS-AUTO-swob.xml
    2016-05-07 18:01:17,607 [INFO] 201 Downloaded : v02.report.observations.swob-ml.20160507.CVFS 20160507220117.437 http://dd3.weather.gc.ca/ observations/swob-ml/20160507/CVFS/2016-05-07-2200-CVFS-AUTO-swob.xml 201 blacklab anonymous 0.151982 parts=1,7174,1,0,0 sum=d,a8b14bd2fa8923fcdb90494f3c5f34a8 from_cluster=DD source=metpx to_clusters=DD,DDI.CMC,DDI.EDM rename=./2016-05-07-2200-CVFS-AUTO-swob.xml message=Downloaded 

### Métriques Speedo

l'activation du plugin speedo permet de comprendre la largeur de bande
passante. et le nombre de messages par seconde d'un ensemble donné de
critères de sélection. résultat :

    blacklab% sr_subscribe --reset foreground ../dd_swob.conf 
    2016-05-07 18:05:52,097 [INFO] sr_subscribe start
    2016-05-07 18:05:52,097 [INFO] sr_subscribe run
    2016-05-07 18:05:52,097 [INFO] AMQP  broker(dd.weather.gc.ca) user(anonymous) vhost(/)
    2016-05-07 18:05:52,231 [INFO] Binding queue q_anonymous.sr_subscribe.dd_swob.13118484.63321617 with key v02.post.observations.swob-ml.# from exchange xpublic on broker amqp://anonymous@dd.weather.gc.ca/
    2016-05-07 18:05:57,228 [INFO] speedo:   2 messages received:  0.39 msg/s, 2.6K bytes/s, lag: 0.26 s

### Mises à jour partielles des fichiers

Lorsque les fichiers sont volumineux, ils sont divisés en plusieurs
parties. Chaque pièce est transférée séparément par sr\_sarracenia.
Ainsi, lorsqu'un gros fichier est mis à jour, la nouvelle partie les
notifications (messages) sont créées. sr\_subscribe vérifiera si le
fichier sur disque correspond à la nouvelle pièce en additionnant les
données locales et en comparant les données locales. qu'au poste. S'ils
ne correspondent pas, alors la nouvelle partie du fichier sera
téléchargé.

### Réception redondant de fichiers

Dans les environnements où une grande fiabilité est requise, plusieurs
serveurs sont souvent configurés pour fournir des services. L'approche
de Sarracenia à l'égard de la La haute disponibilité est ´Active-Active´
dans la mesure où toutes les sources sont en ligne et la production de
données se fait en parallèle. Chaque source publie des données, et les
consommateurs l'obtiennent de la première source qui le rend disponible,
l'utilisation de sommes de contrôle pour déterminer si la donnée est
nouvelle ou non.

Ce filtrage nécessite la mise en œuvre d'une pompe locale sans données
avec sr\_winnow. Consultez le Guide de l'administrateur pour plus
d'informations.

### Plus d'informations

Le [sr\_subscribe(1)](sr_subscribe.1.md) est la source définitive de
référence. des informations sur les options de configuration. Pour plus
d'informations, consulter : [Documentation Sarracenia](sarra-docs-f.md)
