SR\_Winnow
==========

Suppress Redundant Messages
---------------------------

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

**sr\_winnow** is a program that Subscribes to file notifications, and
reposts the notifications, suppressing the redundant ones by comparing
their fingerprints (or checksums.) The **sum** header stores a file's
fingerprint as described in the [sr\_post(7)](sr_post.7.md) man page.

**sr\_winnow** is an [sr\_subscribe(1)](sr_subscribe.1.md) with the
following options forced:

    no-download True  
    suppress_duplicates on
    accept_unmatch True

The suppress\_duplicates lifetime can be adjusted, but it is always on.

**sr\_winnow** connects to a *broker* (often the same as the posting
broker) and subscribes to the notifications of interest. On reception if
a notification, it looks up its **sum** in its cache. if it is found,
the file has already come through, so the notification is ignored. If
not, then the file is new, and the **sum** is added to the cache and the
notification is posted.

**sr\_winnow** can be used to trim messages from
[sr\_post(1)](sr_post.1.md), [sr\_poll(1)](sr_poll.1.md) or
[sr\_watch(1)](sr_watch.1.html) etc... It is used when there are
multiple sources of the same data, so that clients only download the
source data once, from the first source that posted it.

The **sr\_winnow** command takes two argument: an action
startrestartstatus... (self described) followed by a configuration file
described below.

The **foreground** is used when debugging a configuration, when the user
wants to run the program and its configfile interactively.

The actions **cleanup**, **declare**, **setup** can be used to manage
resources on the rabbitmq server. The resources are either queues or
exchanges. **declare** creates the resources. **setup** creates and
additionnaly does the bindings of queues.

### CONFIGURATION

In general, the options for this component are described by the
[sr\_subscribe(1)](sr_subscribe.1.md) page which should be read first.
It fully explains the option configuration language, and how to find the
option settings.

See [sr\_subscribe(1)](sr_subscribe.1.md) for more details.

### SEE ALSO

[sr\_report(7)](sr_report.7.md) - the format of report messages.

[sr\_report(1)](sr_report.1.md) - process report messages.

[sr\_post(1)](sr_post.1.md) - post announcemensts of specific files.

[sr\_post(7)](sr_post.7.md) - The format of announcements.

[sr\_subscribe(1)](sr_subscribe.1.md) - the download client.

[sr\_watch(1)](sr_watch.1.md) - the directory watching daemon.

[dd\_subscribe(1)](dd_subscribe.1.md) - the http-only download client.
