Le français suit (recherchez FRANCAIS)

dd\_subscribe Guide
===================

1- dd.weather.gc.ca (the MSC Datamart) is Environment Canada's public
meteorological data access repository.

2- For each product posted on the Datamart, an AMQP message is
immediately transmitted. This message contains : "md5sum filesize
<http://servername/> filepath". The product's URL is described by the
last two fields. Any application which can subscribe to an AMQP service
can receive notification of products being published and then retrieve
them in real time via http. There is a wide variety of languages and
platforms whereby this procedure can be implemented. Here you will find
a simple demonstration client, "dd\_subscribe". It is implemented in the
Python language.

3- Download clients:

-   Sarracenia ( <http://github.com/MetPX/sarracenia> ) a complete
    reference implementation in Python \>= 3.4. It runs on Linux, Mac,
    and Windows. This is the best choice to use, if you can.
-   Sarrac ( <https://github.com/MetPX/sarrac> ) is a C implementation
    of data insertion (post & watch.) It is Linux only. There is also a
    libcshim to be able to tranparently implement data insertion with
    this tool, and libsarra allows C programs to post directly. There is
    consumer code as well (to read queues) so messages can be passed to
    the downloader of your choice, but no built-in downloading so far.
    This subset is meant to be used where python3 environments are
    impractical (example: high performance computing environments.), or
    where memory & cpu is usage is particularly important such as in
    embedded systems.
-   node-sarra ( <https://github.com/darkskyapp/node-sarra> ) An
    embryonic implementation for node.js.
-   dd\_subscribe is a python2 program that uses python-amqplib to
    receive these amqp notification messages, retrieve the products from
    the datamart via HTTP and place them in a chosen local directory.

4- dd\_subscribe's usage is : dd\_subscribe \[-n\] \[-l logdir\]
config\_file. By default, the program will automatically initiate
product download upon notification. If you want dd\_subscribe to simply
display the notification message without retrieving the products,use the
"-n" The -l option sets a logging directory, and a file named
config\_file\_PID.log will be written.(where PID is the process id)

5- The config file is simple (see dd\_subscribe manpage). To make things
even easier, the example config files provided with the script contain
valid configuration parameters that should be enough to get you started.
The config files may contain :

> 1.  credentials for the rabbitmq server. These options are
>
>     > host default host dd.weather.gc.ca port default port 5672
>     > amqp-user default amqp-user anonymous amqp-password default
>     > amqp-password anonymous
>
> 2.  amqp exchange settings to be able to receive the desired
>     notifications (URL)
>
>     > exchange default exchange xpublic exchange\_type default
>     > exchange\_type topic subtopic no default ...
>
>     -   subtopic replaces amqp exchange\_key options
>     -   several subtopic options may be declared
>     -   to arrive at a valid subtopic, browse the datamart
>         (<http://dd.weather.gc.ca>) and pick any directories where the
>         products are interesting for you. For each directory, create a
>         subtopicas follows:
>
>         > subtopic directory1.subdirectory2.\*.subdirectory4.\#
>         >
>         > where \* replace a directory name (one \* per directory)
>         >
>         > :   \# stands for the remaining possibilities
>         >
> 3.  amqp queue settings to be able to queue the desired notifications
>     (URL)
>
>     > queue default None durable default False expire default None
>
>     -   queue sets the queue name. It should start with cmc.
>     -   expire is expressed in minutes... it sets how long should live
>         a queue without connections
>     -   durable means write queue on disk if the rabbitmq server is
>         stop/restarted...
>     -   by default, dd\_subscribe creates a queue name that should be
>         unique and starts with cmc and puts it into a file
>         .\<configname\>.queue, where \<configname\> is the config
>         filename.
>
> 4.  http credentials (not used for now... might be implemented for
>     restricted products)
>
>     > http-user default http-user None http-password default
>     > http-password None
>
> 5.  delivery specifications
>
>     > lock default lock .tmp directory default directory . accept
>     > default accept None reject default reject None mirror enabling
>     > mirror False flatten default flat char. '/' timeout default
>     > timeout 180
>
>     -   The 'lock' option is a suffix given to the file during the
>         download and taken away when it is completed... This prevents
>         the file from being processed prematurely.
>     -   The 'directory' option defines the target directory on your
>         server. Combined with accept/reject options, the user can
>         select the files of interest and their directories of
>         residence. Theses options are processed sequentially. A
>         rejected product is never downloaded. Accepted products are
>         placed in the closest directory declared above the 'accept'
>         option that picked it. The accept and reject option use regexp
>         to match URLs. The patterns in accept/reject clauses use
>         regular expression syntax, more information here:
>         <https://en.wikipedia.org/wiki/Regular_expression> briefly ´.´
>         is a one character wildcard matching any single character ´\*´
>         means ´any number of repetitions. so ´.\*´ means any sequence
>         of characters, (a wildcard.)
>
>         ex. directory /mylocal/myradars
>
>         :   accept .*RADAR.*
>
>             directory /mylocal/mygribs reject .*Reg.* accept .*GRIB.*
>
>     -   The option 'mirror', if set to True, will put the files into a
>         directory tree similar to the one it resides on
>         dd.weather.gc.ca except that the basename of the tree will be
>         the path set by the directory option.
>     -   The option 'flatten' sets a character that will be used to
>         rename the file on the basis of its path name on
>         dd.weather.gc.ca, replacing the '/' with the chosen character.
>         The file will placed with that extended name in the directory
>         defined by the 'directory' option.
>     -   The option 'timeout' sets a limit in seconds of time under
>         which the file should have been downloaded and placed under
>         the proper directory/name... If the timeout is reached the
>         download is retried ... until succes.
>
6- Under samples/config you will find working configuration files, provided as is,

:   without guaranty. Under samples/program you will find other programs
    we played with.

7- FUN FACT: sarracenia : another rare, mostly carnivorous, Canadian

:   plant... (as are sundew,columbo)

FRANCAIS

Notes de publication pour sarracenia/dd\_subscribe

1- dd.weather.gc.ca (le datamart du SMC) est le dépôt public de données
météorologiques d'Environnement Canada

2- Chaque fois qu'un produit arrive dans le datamart, un message AMQP
est immédiatement transmis. Ce message a la forme : "md5sum
taillefichier <http://servername/> filepath". Le URL du produit est
décrit par les deux derniers chanps. Toute application capable de
s'abonner à un service AMQP peut recevoir les notifications des produits
en qui sont publiés et les récupérer en temps réel par HTTP. Il existe
un grand nombre de langages et de plateformes qui peuvent être utilisées
pour mettre en oeuvre cette procédure. Vous trouverez ici un script de
démonstration simple, "dd\_subscribe". Le script est écrit en Python.

3- dd\_subscribe est un programme en python, utilisant python-amqplib
pour recevoir les notification AMQP, récupérer les produits sur le
datamart par HTTP et les placer dans un répertoire local choisi par
l'usager.

4- L'utilisation du programme: dd\_subscribe \[-n\] \[-l logdir\]
fichier\_config. Par défaut, le programme télécharge immédiatement le
produit lorsqu'une notification est reçue. Si vous voulez simplement
afficher les notifications sans effectuer de téléchargement, utilisez
l'option "-n". L'option "-l" quand a elle, définit un répertoire de
logging et un fichier nomme "fichier\_config\_PID.log" sera écrit. (PID
est le ID du process)

5- Le fichier de configuration est simple (voir le manpage pour
dd\_subscribe). Pour faciliter encore les choses, les exemples de
fichiers de configurations qui sont fournis avec le programme
contiennent des paramètres valides qui devraient suffire pour commencer:

    a) identifiants pour le serveur rabbitmq. Ces paramètres sont: 

             host               default  host          dd.weather.gc.ca
             port               default  port          5672
             amqp-user          default  amqp-user     anonymous
             amqp-password      default  amqp-password anonymous


    b) réglages d'échanges amqp permettant de recevoir les notifications (indiquant
       l'URL du produit)

            exchange            default  exchange      xpublic
            exchange_type       default  exchange_type topic
            subtopic            no default ... 

       - le subtopic replace les clés d'échanges amqp (exchange_key)
       - il est permi de déclarer plusieurs subtopic
       - Pour déterminer une valeur correcte pour un subtopic, explorez le dépôt
         http://dd.weather.gc.ca et choisissez n'importe quel répertoire contenant des
         produits qui sont d'intérêt pour vous. Pour chacun de ces répertoires, spécifiez
         le subtopic comme suit:

               subtopic directory1.subdirectory2.*.subdirectory4.#

               ou        *              caractère de remplacement (wildcard) 
                                        (un seul '*' per par répertoire)
                         #              signifie les possibilités restantes

    c) réglages de la queue amqp permettant de recevoir les notifications

             queue              default  None        
             durable            default  False         
             expire             default  None

       - queue défini le nom de la queue, qui commence toujours avec cmc. Par défaut un nom de queue
         au hazard est créé et conserver dans un fichier nomme .fichier_config.queue
       - expire est un nombre de minutes... qui déclare la longueur de la vie d'une queue sans connection
       - durable permet d'écrire la queue sur disque si le serveur rabbitmq est arrêté ou redemarré
       - par defaut, dd_subscribe crée un nom de queue qui devrait être unique et l'enregistre dans
         un fichier nommé .<configname>.queue où <configname> est le nom du fichier de configuration.


    d) identifiant http (non utilisé en ce moment, pourrait l'être pour des produits
       à distribution restreinte)

             http-user          default  http-user     None
             http-password      default  http-password None


    e) paramètres de livraison

             lock               default  lock          .tmp
             directory          default  directory     .
             accept             default  accept        None
             reject             default  reject        None
             mirror             enabling mirror        False
             flatten            default  flat char.    '/'
             timeout            default  timeout       180 


       - Le paramètre 'lock' contrôle le suffixe qui sera donné au
         fichier pendant le téléchargement qui sera retiré une fois la
         tâche complétée.  Par ce moyen, le fichier en cours de
         téléchargement ne sera pas traité prématurément.

       - Le paramètre 'directory' contrôle le répertoire où seront
         reçues les données sur votre serveur.  En combinaison avec
         'accept/reject' vous pouvez gérer les fichiers qui sont
         téléchargés et leur répertoire de résidence.

         Ces paramètres sont traités séquentiellement. Un produit
         rejeté n'est jamais téléchargé.  Les produits acceptés sont
         placés dans le répertoire le plus récent qui ait été
         déclaré au-dessus du paramètre accept qui a été utilisé
         pour le sélectionner.  Les paramètres accept et reject
         acceptent des expressions régulières pour la reconnaissance
         des URL.  Plus d´information içi: https://fr.wikipedia.org/wiki/Expression_rationnelle
         brièvement:  
         ´.´ va accepter n´importe lequel caractère.
         ´*´ indique une quantité indefinie de répétitions. 
         Alors ´.*´ accept n´importe lequel séquence de caractères.


         ex.     directory /home/steve/myradars
                 accept    .*RADAR.*

                 directory /home/julie/donnees/grib
                 reject    .*Reg.*
                 accept    .*GRIB.*

       - Si vous donnez au paramètre 'mirror' la valeur 'True', les
     fichiers seront placés dans une structure de répertoires
     similaire à celle qui existe sur dd.weather.gc.ca. La racine
     de la structure sera le répertoire indiqué par le paramètre
     'directory'.

       - Le paramètre 'flatten' permet de spécifier un caractère qui
     sera utilisé pour renommer le fichier d'après son chemin sur
     dd.weather.gc.ca, en remplaçant les '/' par le caractère
     choisi. Le fichier sera placé avec ce nom étendu dans le
     répertoire défini par le paramètre 'directory'.

       - L'option 'timeout' défini une limite en seconds pour le temps ou le fichier
         est téléchargé et placé dans le répertoire/nom approprié... Si le timeout
         est dépassé, le download est repris... jusqu'à ce qu'il soit un succès.

6- Dans le répertoire samples/config vous trouverez des fichiers de
configuration qui devraient fonctionner tels quels (sans garantie). Sous
samples/program vous trouverez d'autres programmes avec lesquels nous
avons expérimenté.

7- Détail distrayant: sarracenia est le nom latin de la sarracène, une
plante canadienne rare et à prédominance carnivore (au même titre que la
droséra et la columbo).
