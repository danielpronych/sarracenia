Status: Pre-Draft

Configuration / Administration
==============================

Asymmetric... can use wget request to a static directory for
configuration?

> -   this doesn´t work in S \> 1. need to pass results back as
>     messages.
> -   does work for ´public´ info like bin, checksum scripts, include

What is the tree:

> cfg/
>
> :   .htaccess
>
> > \<valid user\>
> >
> > bin/
> >
> > :   sr-\<clients\>
> >
> > include/
> >
> > :   some standard patterns set by admins.
> >
> > checksum/
> >
> > :   u.py \<the library of checksum scripts\>
> >
> >     > \<source\>/ \<config for source?\>
> >
> > .htaccess
> >
> > :   the \<source user\> and \<the cluster admin user\> and
> >     \<monitors?\>
> >
> > users.conf - user setting for default viewing permissions.
> >
> > :   limits.conf:
> >
> >         - quota in K and # files?
> >         - set per source, per scope.
> >
> >     \<dir\>/\<dir\>/\<dir\>/
> >
> >     :   users.conf -- per directory settings.
> >
> > we can do it statically on users' behalf, but would be nicer if...

Tree is per cluster/scope...

> v01.cfg.\<source\>.limits \<new contents\> of that file.

but the scope is not specified.

> v01.cfg.\<source\>.\<scope\>.limits.conf

Things to set
-------------

> per scope:
>
> :   per directory: permissions to read (used to create .htaccess file)
>     and re-create every day, as the day directories roll over.
>
>     quota in bytes, in files.
>
>     :   a log watcher tallies, and signals to something when quota
>         exceeded. perhaps makes a ´quota exceeded´ message? quota
>         exceeded should propagate back.
>
>     users are per scope. what users a source is permitted to see.
>     (cannot list all users by default.)
>
> that means file deletion needs to work.

Things sources will want to set
-------------------------------

> -   this sets default, which can still be over-ridden by command-line
>     settings.
> -   destination list (in scopes and perhaps accounts)
> -   
>
>     block-size for retransmission stuff.
>
>     :   -   perhaps un-necessary, built-in heuristic is likely good
>             enough.
>
> I think client programs will have, as a baseline : --broker
> amqp://<user@broker>/ --set DD\_BROKER as an environment variable, or
> have it in a config file...
>
> \- setting default broker is hard to do, because to get these
> settings, you have contacted a broker and asked for your settings.

pxpush, built in?
-----------------

use amqp to push config changes around.

there are admin exchanges... no sources can post to them. only admin
users can.

sr\_admin Alice stop.

:   

    sends a v01.cfg.\<source\>.stop message around and admin bus.

    :   -- stop ingesting messages coming from \<source\> -- likely
        implemented in validation code. -- default scope will be
        cluster-wide (all of ddsr) -- option to go multi-cluster?

    once the stop is processed on a node, emit:

    :   

        v01.log.Alice.admin.stopped ...

        :   -- and the source will hear about it! -- there will be a log
            message for each node on which it occurred.

        v01.cfg.\<client\>.drop

        :   

            -- drop messages coming from \<client\>

            :   (if there is a DOS or a they have a problem.)

    set ingest space limits.

    :   v01.cfg.\<source\>.\<scope\>.quota.

        v01.cfg.\<source\>.\<scope\>.quota.

    or perhaps:

    :   

        v01.cfg.query.\<source\>.\<scope\>

        :   -   returns attributes for a given source in a given scope.

    > set ingest bandwidth limits.

Alice can send a sr\_admin Alice stop, and it should work.

Bob (client\> can send an sr\_admin Bob drop... ? ) ... not sure...

v01.cfg.\<source\>.queue ? returns the number of files which have not
yet been validated.... (1st line) and the file names. (1 per line?)

-------- v

v01.cfg.\<source\>.rmafterdelivery.yes ? -- deferred. determines whether
source file should be deleted after all scopes have reported success in
obtaining the file.

> hmm...
>
> :   something monitors the log files, and knows which files are going
>     to which scopes. As the log messages return, that is noted. when
>     all scopes have reported receipt. delete local file.
>
>     this is is complicated... maybe not. not really sure if it is
>     useful...
>
>     use case is large files with lots of blocks, where keeping dozens
>     of GB in flight does not make sense.
>
------------ pxpush, built in? ---------------------------------

command line arguments and config files
---------------------------------------

low priority...

This is a problem to be addressed after the basic proof of concept is
demonstrated.

MetPX-sundew runs as an administrator configured tool. having
configurations entirely in configuration files makes sense for that. We
have positional significance (config file options apply from top down in
file.)

MetPX-sarracenia, is intended to be more user facing and interactive.
User facing commands ought to have robust command line parsing.

sr\_subscribe (dd\_subscribe) and sr\_post, might be candidates for
this.

How to do this is not obvious...

It would appear that optparse, want to do it elegantly.

read options from

> $DD\_ROOT (default if not present, /etc/sr/ ) \~/.sr .sr commandline

have them work together.

Don't want to change the config file format... hmm.. maybe we should...
lot's of work here.

argparse is the current command line parsing module for python. It's
flexible and builds all the help strings (in one language)

what's wrong with argparse?

:   -   no ordering
    -   cannot repeat arguments

so if you want to have similar to:

> reject \^x.z reject \^x.w accept \^x
>
> accept \^z.

then you don't ... so it looks like it is just incompatible. maybe just
have a series of keywords on the command line with a line separator?

sr\_subscribe (dd\_subscribe) directives='directory /home/cc;reject
\^x.z;reject \^x.w;accept \^x;accept \^z;'

have to deal with escaping the separator, then just split on ; and run
it through the same parser?

I dunno, it looks so complicated, that maybe it just isn't worth it, and
stick with just the config file.

need to look at all the config options needed, the URL notation saves a
lot.

Store Client Config Files on Switch?
------------------------------------

just have enough configuration to query the switch. amqp://<user@ddsr>
then most other options just stored on the switch?

clients don't have to maintain a large config file... That way, admins
can see what product selections clients are doing.

Admins could know exactly what the config file is,...

:   -   but they get that info from the logs, not much point.
    -   if clients want to provide configs, email works.
    -   is there a real value?

Checksum scripts
----------------

v01.cfg.register.checksum.\<script\> body of file is the indicated
script. to be pushed to all nodes in the cluster such that they post the
file in the right place in their static tree.

v01.cfg.get.checksum.\<script\> nah... just issue a wget... see ´client
updates.´ retrieve request transfer of the checksum script named
\<script\> from the network. these scripts:

> -   are public
> -   have global scope everywhere where a script is mentioned it should
>     refer to the same script.
> -   as they are executed in many contexts, deps and complexity must be
>     low.
> -   expected to be invoked within process, not forked.

public client updates
---------------------

Is this something we want... a self-updating network? like OTA...

This avoids a lot of ´adm.get´ commands...

It is very difficult to co-ordinate clients in updating their clients.
the initial client is a wrapper that just invokes a request to pull down
current code. inspired by: dropbox, minecraft.

just have a standard tree on any sr where latest clients can be
retrieved...

say we have a public http accessible static tree on every switch...

:   sr/bin has clients sr/lib/checksums has the checksum scripts.

so just do a wget -r on the tree to update.

:   -   usually, caching protocol says it has not changed.

once in a while... retrieve the latest versions of client components:
sr\_subscribe (dd\_subscribe), sr\_sarra, sr\_sender ?

sensitive client updates
------------------------

> scopes\_account.conf -- this might be sensitive? each line: \<scope\>:
> account,account...
>
> unclear... some clients will not be allowed to see this. have to
> figure out who can see what. there might be a per source setting
> indicating which scope/user combos are visible.

Can ask for the node list
-------------------------

somebody, like a sr\_sender, or a sr\_subscribe, connects to a central
switch (sr) and asks how many nodes there are (dd1, dd2), fire up
transfer engines for both. if someone adds a node, a log message alerts
them to a change in list, and they

does this help or make sense?
