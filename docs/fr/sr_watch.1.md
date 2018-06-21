SR\_Watch
=========

regarder un répertoire et publier des messages lorsque les fichiers qui
s'y trouvent changent

Manual section

:   1

Date

:   @Date@

Version

:   @Version@

Manuel group

:   la Suite Metpx-Sarracenia

SYNOPSIS
--------

**sr\_watch** \[ *-pbu--post\_broker broker\_url* \]....\[ *-p--path* \]
\[reloadstartstatusstop\] \[chemin\]

DESCRIPTION
-----------

Surveille un répertoire et publie des messages lorsque les fichiers dans
le répertoire changent. Ses arguments sont très similaires à
[sr\_post](sr_post%20%3Csr_post.1.md). Dans la suite MetPX-Sarracenia,
l'objectif principal est d'afficher la disponibilité et modifications de
ses dossiers. Les abonnés utilisent *sr\_subscribe* pour consommer le
message et télécharger les fichiers changés.

Les messages sont envoyés à un serveur AMQP, également appelé courtier,
spécifié avec l'option \[ *-pb\|--post\_broker broker\_url* \].

### CREDENTIALS

L'option broker définit toutes les informations d'identification pour se
connecter au serveur **RabbitMQ**\*\*.

Courtier
amqp{s}://\<utilisateur\>:\<pw\>@\<brokerhost\>\[:port\]/\<vhost\>\*\*\*\*.

> (par défaut : amqp://anonymous:<anonymous@dd.weather.gc.ca>/)

Tous les outils sr\_ tools stockent toutes les informations
d'authentification sensibles dans le fichier credentials.conf. Les mots
de passe pour les comptes SFTP, AMQP et HTTP sont stockés sur URL´s,
ainsi que d'autres pointeurs. à des fins telles que les clés privées ou
les modes FTP.

Pour plus de détails, voir : [sr\_subscribe(1)
credentials](sr_sr_subscribe.1.html#credentials) credentials

### Paramètres obligatoires

L'option \[*-u\|--url url url*\] spécifie le protocole, les informations
d'identification, l'hôte et le port vers lesquels les abonnés se
connectera pour obtenir le fichier.

format de l'argument à l'option *url*:

    ftp|http|http|sftp]://[user[:password]@]host[:port]/ /[:port
    ou
    ftp|http|http|sftp]://[user[:password]@]host[:port]/ /[:port
    ou
    fichier :

L'option\[*-p\|--chemin*\] indique à *sr\_watch* ce qu'il faut chercher.
Si le *path* spécifie un répertoire, *sr\_watches* crée un message quand
un fichier dans ce répertoire qui est créé, modifié ou supprimé. Si le
*path* spécifie un fichier, *sr\_watch* surveille uniquement ce fichier.
Dans l'avis, il est spécifié avec le *chemin* du produit. Il y a
généralement un message par fichier.

Un exemple d'une excution de *sr\_watch* vérifiant un fichier:

    sr_watch -s s_sftp://stanley@mysftpserver.com/ -p /data/shared/products/foo -b amqp://broker.com -action start

Ici, *sr\_watch* vérifie les événements sur le fichier
/data/shared/products/foo. Les paramètres par défaut des rapports
d'événements si le fichier le fichier est modifié ou supprimé. Lorsque
le fichier est modifié, *sr\_watch* lit le fichier
/data/shared/products/foo. et calcule sa somme de contrôle. Il construit
ensuite un message, se connecte à broker.com en tant
qu'utilisateur'guest' (informations d'identification par défaut). et
envoie le message aux valeurs par défaut vhost '/' et échange
'xs\_stanley' (échange par défaut)

Un abonné peut télécharger le fichier /data/shared/products/foo en se
connectant en tant qu'utilisateur stanley. sur mysftpserver.com en
utilisant le protocole sftp à broker.com en supposant qu'il a les
informations d'identification appropriées.

La sortie de la commande est la suivante:

    [INFO] v02.post.data.shared.products.foo'20150813161959.854 s_sftp://stanley@mysftpserver.com/ /data/shared/products/foo''.
          source=guest parts=1,256,1,0,0,0,0 somme=d,fc473c7a2801babbd3818260f50859de 

Dans MetPX-Sarracenia, chaque article est publié sous un certain thème.
Après le '\[INFO\]', l'information suivante donne le fBtopic\* du
fichier publié. Les thèmes dans *AMQP* sont un champ hierarchique, avec
chaque sous-thème séparé par une points. Dans MetPX-Sarracénie il est
constitué d'un *topic\_prefix* par défaut : version *V02*, d'une action
*post*.., suivi par *subtopic* par défaut : le chemin du fichier séparé
par des points, ici, *data.shared.products.foo*.

Après la hiérarchie des thèmes vient le corps de l'avis. Il se compose
d'un temps *20150813161959.854*, et l'url source du fichier dans les 2
derniers champs.

La ligne restante donne des informations qui sont placées dans l'en-tête
du message amqp. Ici, il se compose de *source=guest*, qui est
l'utilisateur amqp, *parts=1,256,0,0,0,1*.., qui proposent de
télécharger le fichier en 1 partie de 256 octets (la taille réelle du
fichier), suivi de 1,0,0,0. donne le nombre de blocs, le nombre d'octets
restants et le nombre d'octets actuel. bloc.
*sum=d,fc473c7a2801babbd3818260f50859de* mentionne les informations de
la somme de contrôle, ici, *d* signifie la somme de contrôle md5
effectuée sur les données, et *fc473c7a2801babbd3818260f50859de*. est la
valeur de la somme de contrôle. Lorsque l'événement sur un fichier est
une suppression, sum=R,0 R signifie de supprimer un fichier.

Un autre exemple avec un fichier:

    sr_watch -dr /data/web/public_data -s http://dd.weather.gc.ca/ -p bulletins/alphanumériques/SACN32_CWAO_123456 -b amqp://broker.com -action start

Par défaut, sr\_watch vérifie le fichier
/data/web/public\_data/bulletins/alphanumériques/SACN32\_CWAO\_123456
(concaténer le répertoire base\_dir et le chemin relatif de l'url source
pour obtenir le chemin du fichier local). Si le fichier change, il
calcule sa somme de contrôle. Il construit ensuite un message, se
connecte à broker.com en tant qu'utilisateur'guest'. (informations
d'identification par défaut) et envoie le message aux valeurs par défaut
vhost'/' et exchange'sx\_guest' (échange par défaut)

Un abonné peut télécharger le fichier
<http://dd.weather.gc.ca/bulletins/alphanumeric/SACN32_CWAO_CWAO_123456>
en utilisant http. sans authentification sur dd.weather.gc.ca.

Un exemple de vérification d'un répertoire:

    sr_watch -dr /data/web/public_data -s http://dd.weather.gc.ca/ -p bulletins/alphanumérique -b amqp://broker.com -action start

Ici, sr\_watch vérifie la création de fichiers (modification) dans
/data/web/public\_data/bulletins/alphanumérique. (concaténer le
répertoire base\_dir et le chemin relatif de l'url source pour obtenir
le chemin du répertoire). Si le fichier SACN32\_CWAO\_123456 est créé
dans ce répertoire, sr\_watch calcule sa somme de contrôle. Il construit
ensuite un message, se connecte à broker.com en tant
qu'utilisateur'guest'. (informations d'identification par défaut) et
envoie le message à exchange'amq.topic' (échange par défaut)

Un abonné peut télécharger le fichier créé/modifié
<http://dd.weather.gc.ca/bulletins/alphanumeric/SACN32_CWAO_CWAO_123456>
en utilisant http. sans authentification sur dd.weather.gc.ca.

ARGUMENTS ET OPTIONS
--------------------

Veuillez vous référer à la page [sr\_subscribe(1)](sr_subscribe.1.md)
manuel pour une description détaillée des éléments suivants les
paramètres communs et les méthodes de spécification.

### \[--blocksize \<valeur\>\>\]

la valeur doit être l'une des valeurs suivantes: :

> 0 - calcul automatique d'une stratégie de partitionnement appropriée
> (par défaut) 1 - toujours envoyer les fichiers en une seule partie.
> \<sz\> - a utilisé une taille de partition fixe (exemple : 1M)

Les fichiers peuvent être annoncés comme plusieurs blocs (ou pièces.)
Chaque pièce a une somme de contrôle séparée. Les pièces et leurs sommes
de contrôle sont stockées dans le cache. Les blocs peuvent traverser le
réseau séparément, et en parallèle. Lorsque les fichiers changent, les
transferts sont les suivants optimisé en n'envoyant que des pièces qui
ont changé.

L'algorithme d'autocalcul détermine une taille de bloc qui encourage un
nombre raisonnable de pièces. pour des fichiers de différentes tailles.
Comme la taille du fichier varie, le calcul automatique donnera des
valeurs différentes. résultats. Ceci aura pour résultat de renvoyer des
informations qui n'ont pas été modifiées en tant que partitions d'une
partition différente. la taille aura des sommes différentes. Lorsque des
fichiers volumineux sont annexés à un fichier, il est logique de
spécifier un fichier taille de partition fixe.

Dans les cas où l'on utilise un téléchargeur personnalisé qui ne
comprend pas le partitionnement, ou il est nécessaire d´éviter que le
fichier soit divisé en plusieurs parties, donc on spécifierait '1' pour
forcer l'envoi de tous les fichiers. comme une seule pièce.

La valeur du *blocksize* est un entier qui peut être suivi de
l'indicatif *\[BMGT\]* : pour les Bytes, Kilobytes, Megabytes,
Gigabytes, Gigabytes, Terabytes respectivement. Toutes ces références
sont des pouvoirs de 2.

### \[-b\|--courtier \<courtier\>\]

> courtier\* est le courtier auquel se connecter pour envoyer le
> courrier.

### \[-c\|--config \<configfile\>\]

> Un fichier rempli d'options.

### \[--delete \<boolean\>\]

En mode force\_polling, supposons que les répertoires se vident, de
sorte que chaque fichier dans chaque *path*. devrait être affiché à
chaque carte d'électeur, au lieu d'en afficher de nouvelles. Utiliser la
mise en cache pour ignorer les fichiers qu´on a déjà vu. En mode
polling, la vitesse de reconition des fichiers modifiés est limitée à la
vitesse à laquelle on peut traverser (balayer?) l´arborescence. La
méthode de balayage doit être choisie en fonction de la performance
recherchée.

### \[-pbd\|--post\_base\_base\_dir \<path\>\]

L'option *base\_dir* fournit le chemin du répertoire qui, lorsqu'il est
combiné avec l'url relative de *source url*, donne le chemin absolu
local vers le fichier de données à enregistrer.

### \[-eévénementévénement\|...\>\]

Une liste des types d'événements à surveiller séparés par un 'symbole de
tuyau'. events disponibles : create, delete, follow, link, modify, poll
Par défaut : ils sont tous par défaut, à l'exception de poll.

Les événements *create*, *modify* et *delete* reflètent ce qui est
attendu : un fichier en cours de création, de modification ou de
suppression. Si *link* est défini, les liens symboliques seront affichés
comme liens afin que les consommateurs puissent choisir. S'il n'est pas
défini, aucun événement de lien symbolique ne sera jamais posté.

... note:: Déplacer ou renommer les événements donne lieu à un double
motif spécial, avec un message comme ancien nom. et un champ *newname*
set, et un second post avec le nouveau nom, et un champ *oldname* set.
Cela permet aux abonnés d'effectuer un renommage réel et d'éviter de
déclencher un téléchargement lorsque c'est possible.

### \[-ex\|--exchange \<échange\>\]

sr\_watch publie à une échange nommée *[xs]()*"broker\_username" par
défaut. Utilisez l'option *exchange* pour remplacer cette valeur par
défaut.

### \[-fp\|--force\_polling \<boolean\>\]

Par défaut, sr\_watch sélectionne une méthode optimale (en fonction du
système d'exploitation) pour regarder un répertoire. Pour les grands
arbres, la méthode optimale peut être beaucoup plus rapide (10x ou même
100x) pour reconnaître quand un fichier a été modifié. Dans certains
cas, cependant, les méthodes optimales de la plate-forme ne fonctionnent
pas (par exemple avec certains partages réseau, ou distribué), il faut
donc utiliser une méthode d'interrogation plus lente mais plus fiable et
portable. Le *force\_polling* permet à sr\_watch de sélectionner la
méthode d'interrogation malgré la disponibilité d'une méthode
normalement meilleure.

LIMITATION CONNUE : Lorsque *force\_polling* est choisi, le réglage *sleep* doit être d'au moins 5 secondes.

:   Ce n'est pas, pour l'instant, clair pourquoi c´est le cas.

NOTE:

    Lorsque les répertoires sont consommés par les processus en utilisant l'option *supprimer* de l'abonné, ils restent vides, et
    chaque fichier doit être rapporté à chaque passage.  Lorsque les abonnés n'utilisent pas *delete*, sr_watch doit
    savoir quels fichiers sont nouveaux.  Il le fait en notant l'heure du début de la dernière passe de vote.
    Les fichiers sont affichés si leur temps de modification est plus récent que cela.  Il en résultera de nombreux 
    avis multiples par sr_watch, qui peut être minimisé par l'utilisation de cache.   On pourrait même dépendre 
    de la mémoire cache entièrement et activez l'option *delete*, qui fera en sorte que sr_watch tentera de publier
    l'arbre entier chaque fois (en ignorant mtime)

### \[-fs\|--follow\_symlinks \<boolean\>\]

L'option *follow\_symlinks* provoque la traversée de liens symboliques.
si *follow\_symlinks* est activé. et que la destination d'un lien
symbolique est un fichier, alors ce fichier de destination doit être
posté ainsi que le lien. Si la destination du lien symbolique est un
répertoire, alors le répertoire doit être ajouté à ceux qui sont
surveillé par sr\_watch. Si *follow\_symlinks* est faux, alors aucune
action liée à la destination de la symbolique est pris.

### \[-header \<nom\>=\<valeur\>\]

Ajout d'un en-tête \<nom\> avec la valeur donnée aux avis. Utilisé pour
passer des chaînes de caractères en tant que métadonnées dans le fichier
les publicités visant à améliorer la prise de décision pour les
consommateurs. Doit être utilisé avec parcimonie. Il y a des limites sur
le nombre d'en-têtes pouvant être utilisés, et la réduction de la taille
des messages a des impacts sur la performance importantes.

### \[-h--help\]

Afficher les options du programme.

### \[-l \<logpath\>\]

Définissez un fichier dans lequel tous les journaux seront écrits. Le
fichier journal tournera à minuit et sera conservé pour un historique de
5 fichiers.

### \[-p\|--path path\]

**sr\_post** évalue le chemin du système de fichiers à partir de
l'option **path**. et éventuellement le **post\_base\_dir** si l'option
est utilisée.

Si un chemin d'accès définit un fichier, ce fichier est surveillé.

Si un chemin définit un répertoire, alors tous les fichiers de ce
répertoire sont regardé......

Si ce chemin définit un répertoire, tous les fichiers de ce répertoire
sont les suivants surveillé et devrait **sr\_watch** trouver un (ou
plusieurs) répertoire(s), elle les regarde récursivement jusqu'à ce que
tout l'arbre soit scanné.

Les avis AMQP sont faites des champs arborescents, l'heure de l'avis, la
valeur de l'option **url** et les chemins résolus vers lesquels ont été
retirés. le *post\_base\_dir* présent et nécessaire.

### \[-real\|--realpath \<boolean\>\]

L'option realpath résout les chemins donnés à leurs chemins canoniques,
éliminant toute indirection via des liens symboliques. Le comportement
améliore la capacité de sr\_watch à surveiller les arbres, mais les
arbres peuvent avoir des chemins complètement différents des arguments
donnés. Cette option renforce également la traversée des liens
symboliques. Ceci est implémenté pour préserver le comportement d'une
itération précédente de sr\_watch, mais il n'est pas clair s'il est
nécessaire ou utile. Vos commentaires sont les bienvenus.

### \[-rn\|--rename \<path\>\]

Avec l'option *rename*, l'utilisateur peut suggérer un chemin de
destination pour ses fichiers. Si le se termine par'/', il suggère un
chemin d'accès au répertoire...... Si ce n'est pas le cas, l'option
spécifie un renommage de fichier.

### \[-sub\|--subtopic \<key\>\]

La valeur par défaut du sous-thème peut être écrasée par l'option
*subtopic*.

### \[--sleep \<time\> \<time\> \]

Le temps d'attente entre la génération d'événements. Lorsque les
fichiers sont écrits fréquemment, c'est contre-productif de produire un
avis pour chaque changement, car il peut produire un flux continu de
changements où les transferts ne peut pas être fait assez rapidement
pour suivre le rythme. Dans de telles circonstances, on peut regrouper
tous les changements apportés à un dossier durant l´intervalle *sleep*,
et de produire un seul avis.

### \[-to\|--to \<destination\>,\<destination\>,\<destination\>,... \]

> Une liste séparée par des virgules des grappes de destination
> auxquelles les données affichées doivent être envoyées. Demandez aux
> administrateurs de pompes la liste des destinations valides.
>
> default : le nom d'hôte du courtier sur lequel le message est posté.

... note: : FIXME: une bonne liste de destination devrait pouvoir être
découverte.

### \[-tp\|--topic\_prefix \<key\>\]

Par défaut, le sujet est fait du topic\_prefix par défaut : version
*V02*, une action *post*.., suivi du sous-thème par défaut : le chemin
du fichier séparé par des points (le point étant le séparateur de thème
pour amqp). Vous pouvez écraser le préfixe du sujet en définissant cette
option.

### \[-pbu\|--post\_base\_url \<url\>\]

L'option **post\_base\_url** définit le protocole, les informations d'
identification, l'hôte et le port sous que le produit peut être
récupéré.

Le corps d´un avis contient trois champs : l'heure de l'avis, cette
valeur **base\_url** et le chemin\*\*\**, relatif à*post\_base\_dir\*,
si nécessaire.

la concaténation des deux derniers champs de l'avis définit l´URL
complete que les abonnés utiliseront pour télécharger le produit.

### \[sum\|--sum \<string\>\]

Tous les avis incluent une somme de contrôle. Il est placé dans un
en-tête du message amqp qui aura la forme d'un entrée *sum* avec la
valeur par défaut 'd,md5\_checksum\_on\_data'. L'option *sum* indique au
programme comment calculer la somme de contrôle. C'est une chaîne de
caractères séparés par des virgules. Les valeurs de *sum* valides sont :

    [0|n|d|d|s|N|N|z]
    où    0 : no checksum.... la valeur dans post est un entier aléatoire (uniquement pour tester/déboguer.)
          d : do md5sum on file content (par défaut pour l'instant, compatibilité)
          n : fait la somme de contrôle md5sum sur le nom de fichier
          N : fait la somme de contrôle SHA512 sur le nom de fichier.
          s : do SHA512 sur le contenu du fichier (par défaut à l'avenir)
          z,a : calculer la valeur de la somme de contrôle à l'aide de l'algorithme a et assigner après le téléchargement.

D'autres algorithmes peuvent être contribués. Voir la Programmer´s
Guide.

### Stratégies de détection de fichiers

Le travail fondamental de sr\_watch est de remarquer quand les fichiers
sont disponibles pour être transférés. La stratégie appropriée varie en
fonction de:

> le **nombre de fichiers de l'arbre** à surveiller, le délai **minimum
> pour signaler les changements** aux fichiers qui est acceptable, et la
> **taille de chaque fichier** dans l'arbre.

L'arbre le plus facile à surveiller est le plus petit \*\* Avec un seul
répertoire à surveiller où l'on affiche un message pour un composant
*sr\_sarra*, alors l'utilisation de l'option *delete* gardera en tout
temps le nombre minimale de fichiers dans le répertoire et minimisera le
temps de remarquer les nouveaux. Dans ces conditions optimales,
l'observation des fichiers dans un centième de seconde, c'est
raisonnable de s'y attendre. N'importe quelle méthode fonctionnera bien
pour de tels arbres, mais... les charge imposé sur l´ordinateur par la
méthode par défaut de sr\_watch (inotify) sont généralement les plus
basses.

sr\_watch est sr\_post avec l'option *sleep* qui lui permettra de
boucler les répertoires donnés en arguments. sr\_cpost est une version C
qui fonctionne de manière identique, sauf qu'elle est plus rapide et
utilise beaucoup moins de mémoire, à l'adresse le coût de la perte du
support des plugins. Avec sr\_watch (et sr\_cpost) La méthode par défaut
de la remarque les changements dans les répertoires utilisent des
mécanismes spécifiques au système d'exploitation (sous Linux : INOTIFY)
pour reconnaître les modifications sans avoir à analyser manuellement
l'arborescence complète des répertoires. Une fois amorcés, les
changements de fichiers sont remarqués instantanément, mais nécessitent
une première marche à travers l'arbre, *une passe d'amorçage*.

Par exemple, **supposons qu'un serveur peut examiner 1500
fichiers/seconde**. Si un arbre de taille moyenne est de 30 000
fichiers, alors il faudra 20 secondes pour une passe d'amorçage\**. En
utilisant la méthode la plus rapide disponible, on doit supposer qu'au
démarrage d'une telle arborescence de répertoires, il faudra environ 20
secondes avant qu'elle ne démarre de façon fiable. L'affichage de tous
les fichiers dans l'arborescence. Après cette analyse initiale, les
fichiers sont remarqués avec une latence inférieure à la seconde. Donc
unsommeil de 0.1 (vérifiez les changements de fichiers toutes les
dixièmes de seconde) est raisonnable, à condition que nous acceptions
l'amorçage initial.*\* Si l'on choisit l'option **force\_polling**,
alors ce délai de 20 secondes est encouru pour chaque passe de balayage,
plus le temps nécessaire pour effectuer l'affichage lui-même. Pour le
même arbre, un réglage *sleep* de 30 secondes serait le minimum à
recommander. Attendez-vous à ce que les fichiers seront remarqués
environ 1,5\*, les paramètres *sleep* en moyenne. Dans cet exemple,
environ 45 secondes. Certains seront ramassés plus tôt, d'autres plus
tard. A part les cas spéciaux où la méthode par défaut manque de
fichiers, *force\_polling* est beaucoup plus lente sur des arbres de
taille moyenne que la méthode par défaut et ne devrait pas être utilisé
si la rapidité d'exécution est une préoccupation.

Dans les clusters de supercalculateurs, des systèmes de fichiers
distribués sont utilisés, et les méthodes optimisées pour le système
d'exploitation les modifications de fichiers (INOTIFY sous Linux) ne
franchissent pas les limites des nœuds. Pour utiliser sr\_watch avec la
stratégie par défaut sur un répertoire dans un cluster de calcul, on
doit généralement avoir un processus sr\_watch sr\_watch s'exécutant sur
chaque noeud. Si cela n'est pas souhaitable, alors on peut le déployer
sur un seul nœud avec *force\_polling* mais le timing sera le suivant
être limité par la taille du répertoire.

Au fur et à mesure que l'arbre surveillé prend de l'ampleur, la latence
au démarrage de sr\_watch´s augmente, et si le sondage (
*force\_polling* ) est utilisé, la latence à la modification des
fichiers d'avis augmentera également. Par exemple, avec un arbre avec 1
million de fichiers, il faut s'attendre, au mieux, à une latence de
démarrage de 11 minutes. S'il s'agit d'un sondage, alors une attente
raisonnable du temps qu'il faut pour remarquer les nouveaux fichiers
serait de l'ordre de 16 minutes.

Si la performance ci-dessus n'est pas suffisante, alors il faut
considérer l'utilisation de la librairie de cales ( *shim* library ) à
la place de sr\_watch. Tout d'abord, il faut installer la version C de
Sarracenia, et en suite rajouter à l'environnement pour tous les
processus qui vont écrire des fichiers à publier pour l'appeler:

    export SR_POST_CONFIG=shimpost.conf
    export LD_PRELOAD="libsrshim.so.1".

où *shimpost.conf* est un fichier de configuration sr\_cpost dans le
répertoire \~/.config/sarra/post/. Un sr\_cpost est le même que celui de
sr\_post, sauf que les plugins ne sont pas supportés. Avec la librairie
en place, chaque fois qu'un fichier est écrit, les clauses
*accept/reject* du fichier shimpost.conf sont les suivantes consulté, et
s'il est accepté, le fichier est publié tel qu'il le serait par
sr\_watch.

Jusqu'à présent, la discussion a porté sur le temps nécessaire pour
remarquer qu'un fichier a changé. Un autre facteur à prendre en
considération est le temps d'afficher les fichiers une fois qu'ils ont
été remarqués. Il y a des compromis basés sur l'algorithme de checksum
choisi. Le choix le plus robuste est le choix par défaut : *s* ou
SHA-512. Lorsque vous utilisez la méthode de la somme *s*, l'ensemble du
fichier sera lue afin de calculer sa somme de contrôle, ce qui est
susceptible de déterminer le temps jusqu'à l'affichage. la somme de
contrôle sera utilisé par les consommateurs en aval pour déterminer si
le fichier annoncé est nouveau ou s'il s'agit d'un fichier qui a déjà
été vu, et c'est vraiment pratique.

Pour les fichiers plus petits, le temps de calcul de la somme de
contrôle est négligeable, mais il est généralement vrai que les fichiers
plus volumineux Lorsque **en utilisant la méthode shim library**, le
processus qui a écrit le fichier est le même que celui qui a écrit le
fichier. En calculant la somme de contrôle\**, la probabilité que les
données du fichier se trouvent dans un cache accessible localement est
assez élevée, de sorte qu'il est aussi peu coûteux que possible*\*. Il
convient également de noter que la commande sr\_watch/sr\_cpost Les
processus de surveillance des répertoires sont à thread unique, alors
que lorsque les jobs utilisateur appellent sr\_post, ou utilisent le
shim. il peut y avoir autant de processus d'affichage de fichiers qu'il
y a de rédacteurs de fichiers.

Pour raccourcir les temps d'enregistrement, on peut sélectionner des
algorithmes *sum* qui ne lisent pas la totalité de l'enregistrement
comme *N* (SHA-512 du nom du fichier seulement), mais on perd alors la
capacité de différenciation entre les versions du fichier.

note ::

:   devrait penser à utiliser N sur sr\_watch, et à faire recalculer les
    sommes de contrôle par des pelles multi-instance. pour que cette
    pièce devienne facilement parallélisable. Devrait être simple, mais
    pas encore exploré. à la suite de l'utilisation de la bibliothèque
    de cales. FIXME.

Une dernière considération est que dans de nombreux cas, d'autres
processus sont en train d'écrire des fichiers dans des répertoires
surveillés par sr\_watch. Le fait de ne pas établir correctement les
protocoles de complétion de fichiers est une source commune de problèmes
intermittents et difficiles à diagnostiquer en matière de transfert de
fichiers. Pour des transferts de fichiers fiables, Il est essentiel que
les processus qui écrivent des fichiers et sr\_watch s'entendent sur la
façon de représenter un fichier qui n'est pas complet.

### Tableau de stratégie de détection de fichiers

+--------------------------------------------------------------------------------------------+
\| \| \| Stratégies de détection de fichiers (ordre : de la plus rapide
à la plus lente) \| \| Le Méthodes plus rapides marchent sur les plus
grands arborescences. \| \| \|
+-------------+---------------------------------------+--------------------------------------+
\| Méthode \| Description \| Application \|
+=============+=======================================+======================================+
\| Beaucoups de travaux d´utilisateur qui\| \| ne peuvent pas être
modifié afin de \| \| \| - nécessite le paquet C. \| \| - export
LD\_PRELOAD=libsrshim.so.1 \| \| - usage accru de *reject* \| - arbres
de millions de fichiers. \| - fonctionne sur n´importe quelle \| -
efficacité maximale. \| \| \| taille d´arbre de fichiers. \| -
complexité maximale. \| - très multi-tâches. \| - ou python3 n´est pas
disponible. \| \| \| - E/S par origine (plus efficace) \| - pas de
sr\_watch. \| \| - pas de plugins. \| \| \| \| \|
+-------------+---------------------------------------+--------------------------------------+
\| l´usager publie quand il a fini d´ \| [sr\_post(1)](sr_post.1.md) où
d´autres composants sr\_ \| \| une fois écriture complété. \| \| \| \|
\| - contrôle plus fine. \| \| \| - publieur fait la somme de contrôle
\| - d´habitude meilleur. \| - Moins de aller-retouers \| - meilleur
approche que sr\_watch. \| - un peu plu len que le bibliothèque \| -
L´usager doit publier explicitement\| - pas de balayage de répertoire.
\| dans ces scripts/jobs. \| - très multi-tâches. \| \|
+-------------+---------------------------------------+--------------------------------------+
fonctionne comme watch si sleep \> 0 \| - ou python3 est dure a avoir.
\| \| \| \| - ou la vitesse est important. \| - plus vite que sr\_watch.
\| - ou on n´a pas besoin de plugins. \| \| \| - utilise moins de
mémoire vive que \| - limité sues with tree size \| \| \| sr\_watch \|
as sr\_watch, just a little later. \| \| \| - peut marcher avec des
arbres \| (see following methods) \| \| \| plus grand que sr\_watch \|
\|
+-------------+---------------------------------------+--------------------------------------+
\| Réception de livraisons d´autres \| lorsque complete, renommé pour
enlevé suffix. Suffix est programmable. \| \| - require aller-retour
pour renommage \| \| (un peu plus lent) \| \| \| \| - on peu présumer
1500 fichier/second \| \| \| (defaut) \| - gros arborescences auras de
delais \| \| au démarrage - chaque noeud dans un grappe a besoin \| \|
de tourner un instance. \| \| \| \| - chaque sr\_watch est une seul
tâche. \| \|
+-------------+---------------------------------------+--------------------------------------+
utilisez conventsion linux pour cacher \| \| des fichiers avec un prefix
'.' compatabilité \| \| \| \| \| \|
+-------------+---------------------------------------+--------------------------------------+
Age minimal (de modification)du fichier avant qu´il est considéré
complet. - rajout ce délai sur chaque transfert\| \| \| \| - Vulnérable
à des pannes réseau. \| \| - Vulnérable à des horloges désynchr \| \| \|
\| onizés \| \| \| \| \| \| \| \| \| \|
+-------------+---------------------------------------+--------------------------------------+
Tel que les 3 méthodes précedentes mais en se servant de listings de
répertoires \| \| \| \| \| \| \| \| - Gros arbres plus lents \| \| \| \|
- le plus compatbile (marchera \| \| n´importe où) \| \|
+-------------+---------------------------------------+--------------------------------------+

OPTIONS SPÉCIFIQUES AUX DÉVELOPPEURS
------------------------------------

### \[-debug\|--debug\]

Active si *-debug\|--debug* apparaît dans la ligne de commande.... ou
*debug* est réglé sur True dans le fichier de configuration utilisé.

### \[-r\|--randomize\]

Actif si *-r--randomize* apparaît dans la ligne de commande.... ou
randomomize\* est réglé sur True dans le fichier de configuration
utilisé. S'il y a plusieurs messages parce que le fichier est affiché.
par bloc parce que l'option *blocksize* a été définie, le bloc sont
aléatoires, ce qui signifie que les messages ne seront pas affichés.
classés par numéro de bloc.

### \[-rr\|--reconnect\]

Actif si *-rc\|--reconnect* apparaît dans la ligne de commande.... ou
Reconnect\* est réglé sur True dans le fichier de configuration utilisé.
S'il y a plusieurs messages parce que le fichier est annoncé. par bloc
parce que l'option *blocksize* a été définie, il y a un la reconnexion
au courtier à chaque fois qu'un courrier doit être publié.

### \[--on\_heartbeat\]

Toutes les *heartbeat* secondes, le *on\_heartbeat* est invoqué. Pour
les opérations périodiques, cela se produit relativement rarement,
l'échelle de plusieurs minutes, habituellement. L'argument est en fait
une durée, de sorte qu'il peut être exprimé en différentes unités de
temps : 5m (cinq minutes), 2h (deux heures), jours ou semaines.

### \[--on\_watch\]

Toutes les *sleep* secondes, les modifications apportées au système de
fichiers sont traitées par lots. Avant ce traitement, le plugin
*on\_watch* est invoqué. Il peut être utilisé pour mettre un fichier
dans l'un des répertoires surveillés..... Le *sleep* est généralement un
intervalle beaucoup plus court que les battements du cœur. Il s'agit
également d'un et peut donc être exprimée dans les mêmes unités.

CAVEATS
-------

### Fichiers temporaires

Afin d'éviter les alertes pour les fichiers partiellement écrits
(généralement temporaires), *sr\_watch* n'affiche pas de fichier pour
les modifications apportées aux fichiers portant certains noms :

> les fichiers dont le nom commence par un point **.**. les fichiers
> dont les noms se terminent par.tmp

### Instance INOTIFY

De nombreux systèmes linux ont des limites sur le nombre de répertoires
qui peuvent être surveillés et qui sont réglés assez bas, afin de
minimiser utilisation de la mémoire du noyau. Si vous voyez un message
de ce type: :

> raise OSError("inotify instance limit reached") OSError: inotify
> instance limit reached

Dans ce cas, utilisez les privilèges adminsitratifs pour définir *sysctl
fs.inotify.max\_user\_instance=\<enough\>* à un nombre suffisament
grand. Plus de mémoire du noyau sera allouée pour cela, mais il n´y a
pas d'autres effets connuse du à la modification de ce paramètre.

SEE ALSO
--------

[sr\_post(1)](sr_post.1.md) - publier des avis de fichiers.

[sr\_post(7)](sr_post.7.md) - le format des avis.

[sr\_report(7)](sr_report.7.md) - le format des rapports de télémétrie.

[sr\_report(1)](sr_report.1.md) - consommateur des rapports.

[sr\_sarra(8)](sr_sarra.8.md) - Selectionner, acquérir, et
Récursivement Reannoncer Ad vitam aeternam.

[sr\_subscribe(1)](sr_subscribe.1.md) - Sélectionner et télécharger des
fichiers publiés.
