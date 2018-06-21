SR\_Sarra
=========

Subscribe, Acquire and Recursively Re-announce Ad nauseam
---------------------------------------------------------

Manual section

:   8

Date

:   @Date@

Version

:   @Version@

Manual group

:   MetPx Sarracenia Suite

### SYNOPSIS

**sr\_sarra** foregroundstopreload\|status configfile

**sr\_sarra** cleanupsetup configfile

### DESCRIPTION

**sr\_sarra** is a program that Subscribes to file notifications,
Acquires the files and ReAnnounces them at their new locations. The
notification protocol is defined here [sr\_post(7)](sr_post.7.md)

**sr\_sarra** connects to a *broker* (often the same as the remote file
server itself) and subscribes to the notifications of interest. It uses
the notification information to download the file on the local server
its running on. It then posts a notification for the downloaded files on
a broker (usually on the local server).

**sr\_sarra** can be used to acquire files from
[sr\_post(1)](sr_post.1.md) or [sr\_watch(1)](sr_watch.1.md) or to
reproduce a web-accessible folders (WAF), that announce its' products.

The **sr\_sarra** is an [sr\_subscribe(1)](sr_subscribe.1.md) with the
following presets:

    mirror True

#### Specific consuming requirements

If the messages are posted directly from a source, the exchange used is
'[xs]()\<brokerSourceUsername\>'. Such message may not contain a source
nor an origin cluster, or a malicious user may set the values
incorrectly. To protect against malicious settings, administrators
should set *source\_from\_exchange* to **True**.

-   **source\_from\_exchange \<boolean\> (default: False)**

Upon reception, the program will set these values in the parent class
(here cluster is the value of option **cluster** taken from
default.conf):

self.msg.headers\['source'\] = \<brokerUser\>
self.msg.headers\['from\_cluster'\] = cluster

overriding any values present in the message. This setting should always
be used when ingesting data from a user exchange.

### SEE ALSO

[sr\_subscribe(1)](sr_subscribe.1.md) - the format of configurations
for MetPX-Sarracenia.

[sr\_report(7)](sr_report.7.md) - the format of report messages.

[sr\_report(1)](sr_report.1.md) - process report messages.

[sr\_post(1)](sr_post.1.md) - post announcemensts of specific files.

[sr\_post(7)](sr_post.7.md) - The format of announcements.

[sr\_subscribe(1)](sr_subscribe.1.md) - the download client.

[sr\_watch(1)](sr_watch.1.md) - the directory watching daemon.

[dd\_subscribe(1)](dd_subscribe.1.md) - the http-only download client.
