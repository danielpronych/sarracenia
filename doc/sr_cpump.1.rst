==========
 SR_CPUMP 
==========

-----------------
sr_shovel in C
-----------------

:Manual section: 1 
:Date: @Date@
:Version: @Version@
:Manual group: MetPX-Sarracenia

.. contents::

SYNOPSIS
========

**sr_cpump** foreground|start|stop|restart|reload|status configfile
**sr_cpump** cleanup|declare|setup configfile

DESCRIPTION
===========

**sr_cpump** is an alternate implementation of `sr_subscribe(7) <sr_subscribe.1.rst>`_ 
with some limitations.  

 - doesn't download data, but only circulates posts.
 - runs as only a single instance (no multiple instances.) 
 - does not support any plugins.
 - does not support vip for high availability.
 - different regular expression library: POSIX vs. python.
 - does not support regex for the strip command (no non-greedy regex)

It can therefore act as a drop-in replacement for:

   `sr_report(1) <sr_report.1.rst>`_ - process report messages.

   `sr_shovel(8) <sr_shovel.8.rst>`_ - process shovel messages.

   `sr_winnow(8) <sr_winnow.8.rst>`_ - process winnow messages.

The C implementation may be easier to make available in specialized environments, 
such as High Performance Computing, as it has far fewer dependencies than the python version.
It also uses far less memory for a given role.  Normally the python version 
is recommended, but there are some cases where use of the C implementation is sensible.

**sr_cpump** connects to a *broker* (often the same as the posting broker)
and subscribes to the notifications of interest. On reception of a post,
it looks up its **sum** in its cache.  if it is found, the file has already come through,
so the notification is ignored. If not, then the file is new, and the **sum** is added 
to the cache and the notification is posted.  

**sr_cpump** can be used, like `sr_winnow(8) <sr_winnow.8.rst>`_,  to trim messages 
from `sr_post(1) <sr_post.1.rst>`_, `sr_poll(1) <sr_poll.1.html>`_  
or `sr_watch(1) <sr_watch.1.rst>`_  etc... It is used when there are multiple 
sources of the same data, so that clients only download the source data once, from 
the first source that posted it.

The **sr_cpump** command takes two argument: an action start|stop|restart|reload|status... (self described)
followed by a configuration file.

The **foreground** action is used when debugging a configuration, when the user wants to 
run the program and its configfile interactively...   The **foreground** instance 
is not concerned by other actions.  The user would stop using the **foreground** instance 
by simply <ctrl-c> on linux or use other means send SIGINT or SIGTERM to the process.

The actions **cleanup**, **declare**, **setup** can be used to manage resources on
the rabbitmq server. The resources are either queues or exchanges. **declare** creates
the resources. **setup** creates and additionally does the bindings of queues.

The actions **add**, **remove**, **edit**, **list**, **enable**, **disable** act
on configurations.

CONFIGURATION
=============

In general, the options for this component are described by 
the `sr_subscribe(1) <sr_subscribe.1.rst>`_  page which should be read first.
It fully explains the option configuration language, and how to find
the option settings.

**NOTE**: The regular expression library used in the C implementation is the POSIX
one, and the grammar is slightly different from the python implementation.  Some
adjustments may be needed.


ENVIRONMENT VARIABLES
=====================

if the SR_CONFIG_EXAMPLES variable is set, then the *add* directive can be used
to copy examples into the user's directory for use and/or customization.

An entry in the ~/.config/sarra/default.conf (created via sr_subscribe edit default.conf )
could be used to set the variable::

  declare env SR_CONFIG_EXAMPLES=/usr/lib/python3/dist-packages/sarra/examples

the value should be available from the output of a list command from the python
implementation.

SEE ALSO
========

`sr_report(7) <sr_report.7.rst>`_ - the format of report messages.

`sr_report(1) <sr_report.1.rst>`_ - process report messages.

`sr_post(1) <sr_post.1.rst>`_ - post announcemensts of specific files.

`sr_post(7) <sr_post.7.rst>`_ - The format of announcements.

`sr_subscribe(1) <sr_subscribe.1.rst>`_ - the download client.

`sr_watch(1) <sr_watch.1.rst>`_ - the directory watching daemon.

`dd_subscribe(1) <dd_subscribe.1.rst>`_ - the http-only download client.
