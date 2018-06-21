SR\_CPUMP
=========

sr\_shovel in C
---------------

Manual section

:   1

Date

:   @Date@

Version

:   @Version@

Manual group

:   MetPX-Sarracenia

### SYNOPSIS

**sr\_cpump** foregroundstopreloaddeclare\|setup configfile

### DESCRIPTION

**sr\_cpump** is an alternate implementation of
[sr\_subscribe(7)](sr_subscribe.1.md) with some limitations.

> -   doesn't download data, but only circulates posts.
> -   runs as only a single instance (no multiple instances.)
> -   does not support any plugins.
> -   does not support vip for high availability.
> -   different regular expression library: POSIX vs. python.
> -   does not support regex for the strip command (no non-greedy regex)

It can therefore act as a drop-in replacement for:

> [sr\_report(1)](sr_report.1.md) - process report messages.
>
> [sr\_shovel(8)](sr_shovel.8.md) - process shovel messages.
>
> [sr\_winnow(8)](sr_winnow.8.md) - process winnow messages.

The C implementation may be easier to make available in specialized
environments, such as High Performance Computing, as it has far fewer
dependencies than the python version. It also uses far less memory for a
given role. Normally the python version is recommended, but there are
some cases where use of the C implementation is sensible.

**sr\_cpump** connects to a *broker* (often the same as the posting
broker) and subscribes to the notifications of interest. On reception of
a post, it looks up its **sum** in its cache. if it is found, the file
has already come through, so the notification is ignored. If not, then
the file is new, and the **sum** is added to the cache and the
notification is posted.

**sr\_cpump** can be used, like [sr\_winnow(8)](sr_winnow.8.md), to
trim messages from [sr\_post(1)](sr_post.1.md),
[sr\_poll(1)](sr_poll.1.html) or [sr\_watch(1)](sr_watch.1.md) etc...
It is used when there are multiple sources of the same data, so that
clients only download the source data once, from the first source that
posted it.

The **sr\_cpump** command takes two argument: an action
startrestartstatus... (self described) followed by a configuration file.

The **foreground** action is used when debugging a configuration, when
the user wants to run the program and its configfile interactively...
The **foreground** instance is not concerned by other actions. The user
would stop using the **foreground** instance by simply \<ctrl-c\> on
linux or use other means send SIGINT or SIGTERM to the process.

The actions **cleanup**, **declare**, **setup** can be used to manage
resources on the rabbitmq server. The resources are either queues or
exchanges. **declare** creates the resources. **setup** creates and
additionally does the bindings of queues.

The actions **add**, **remove**, **edit**, **list**, **enable**,
**disable** act on configurations.

### CONFIGURATION

In general, the options for this component are described by the
[sr\_subscribe(1)](sr_subscribe.1.md) page which should be read first.
It fully explains the option configuration language, and how to find the
option settings.

**NOTE**: The regular expression library used in the C implementation is
the POSIX one, and the grammar is slightly different from the python
implementation. Some adjustments may be needed.

### ENVIRONMENT VARIABLES

if the SR\_CONFIG\_EXAMPLES variable is set, then the *add* directive
can be used to copy examples into the user's directory for use and/or
customization.

An entry in the \~/.config/sarra/default.conf (created via sr\_subscribe
edit default.conf ) could be used to set the variable:

    declare env SR_CONFIG_EXAMPLES=/usr/lib/python3/dist-packages/sarra/examples

the value should be available from the output of a list command from the
python implementation.

### SEE ALSO

[sr\_report(7)](sr_report.7.md) - the format of report messages.

[sr\_report(1)](sr_report.1.md) - process report messages.

[sr\_post(1)](sr_post.1.md) - post announcemensts of specific files.

[sr\_post(7)](sr_post.7.md) - The format of announcements.

[sr\_subscribe(1)](sr_subscribe.1.md) - the download client.

[sr\_watch(1)](sr_watch.1.md) - the directory watching daemon.

[dd\_subscribe(1)](dd_subscribe.1.md) - the http-only download client.
