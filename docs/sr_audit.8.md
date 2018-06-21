SR\_Audit
=========

Audit Broker State
------------------

Manual section

:   8

Date

:   @Date@

Version

:   @Version@

Manual group

:   Metpx-Sarracenia Suite

### SYNOPSIS

> **sr\_audit** configfile foregroundstopreload\|status
>
> **sr\_audit** --pump foreground configfile
>
> **sr\_audit** --users foreground configfile

### DESCRIPTION

Sr\_audit is a daemon that runs periodically to examine what is running
on a system to fixes issues it sees. When run as a non-administrative
user, it looks for components which state files indicate are running,
but for which the corresponding process is missing. It will restart
those. Any running process should also be writing at least a heartbeat
message to it´s log file periodically, so if the log file is too old,
the component will be assumed frozen, and restarted.

When run by an administrative user, Sr\_audit configures a broker to
reflect sarracenia configuration settings. **Sr\_audit** takes one
argument: the action to perform. One can also set a few option in a
configuration file: **debug**, **max\_queue\_size**.

When **Sr\_audit** is *started* in admin mode, it connects to the broker
using the **admin** account. It sleeps the time required to trigger the
next heartbeat.

The default behavior of **sr\_audit** is to manage and control the
queues on the broker. The queues are validated and deleted if there is
no client connected to it and has more than **max\_queue\_size**
messages waiting or if there are queues or exchanges that do not conform
to sarracenia naming conventions (queue names start with
**[q]()"brokerusername"** where "brokerusername" is a valid user on the
broker).

When configuring a pump, there are other ways of using **sr\_audit**.
When **sr\_audit** is invoked with **--pump** it helps configuring the
pump. When invoked with **--users** the program manages the users,
permissions and exchanges.

### OPTIONS

In general, the options for this component are described by the
[sr\_subscribe(1)](sr_subscribe.1.md) page which should be read first.
It fully explains the option configuration language, and how to find
option settings.

There are very few options that **sr\_audit** uses:

**admin \<user\> (Mandatory: broker admin user, detailed in
credentials.conf)**

**debug \<boolean\> (default: False)**

**reset \<boolean\> (default: False)**

**set\_passwords \<boolean\> (default: True)**

**max\_queue\_size \<int\> (default: 25000 nbr messages in queue)**

The **admin** option must be defined it normally be set in the file
**default.conf** and the credential details would be found in the file
**credentials.conf** Normally when users are created, the passwords for
communications with the broker are set based on the values found in the
credentials file.

When the *reset* option is given, user passwords and permissions will be
reset to their expected values. Normally, an existing user's permissions
are left untouched by an audit run.

### VERIFY PUMP SETTINGS

Use **sr\_audit** invoke with **--pump** to set up it's configuration.
It makes sure the **feeder** user credentials are given and the
**admin** user is defined and valid.

### MANAGING USERS

When **sr\_audit** is invoked with **--users**, the broker's users and
exchanges are verified. The program builds a list of users by their
**declare** roles. It checks that: **admin**, **feeder** administrative
roles are working. **sr\_audit** makes sure that users configured in
sarracenia configurations are present on the broker. Missing users are
added... with the permissions required for their role. Extra users, not
configured in sarracenia, are deleted.

To verify user exchanges, **sr\_audit** gets the list of exchanges
present on the broker. From the users and roles, it determines the
exchanges that should be present and creates the one missing. Extra
exchanges are deleted if their names do not start with 'x'.

When adding or deleting a user, the broker administrator adds or delete
the role declaration for a username and in the **default.conf** file.
Then he runs **sr\_audit --users foreground configfile**. The log on
standard output would tell the administrator what broker resources were
added/deleted (user,exchanges, queue, etc).

#### SEE ALSO

[sr\_subscribe(1)](sr_subscribe.1.md) - the format of configurations
for MetPX-Sarracenia.

[sr\_report(7)](sr_report.7.md) - the format of report messages.

[sr\_report(1)](sr_report.1.md) - process report messages.

[sr\_post(1)](sr_post.1.md) - post announcemensts of specific files.

[sr\_post(7)](sr_post.7.md) - The format of announcement messages.

[sr\_sarra(8)](sr_sarra.8.md) - Subscribe, Acquire, and ReAdvertise
tool.

[sr\_watch(1)](sr_watch.1.md) - the directory watching daemon.

[<https://github.com/MetPX/>](https://github.com/MetPX/) - sr\_subscribe
is a component of MetPX-Sarracenia, the AMQP based data pump.
