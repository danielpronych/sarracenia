SR\_Report
==========

Select and Process Posted Reports
---------------------------------

Manual section

:   1

Date

:   @Date@

Version

:   @Version@

Manual group

:   Metpx-Sarracenia Suite

### SYNOPSIS

> **sr\_report** foregroundstopreload\|status configfile
>
> **sr\_report** cleanupsetup configfile

### DESCRIPTION

sr\_report is a program to efficiently process reports of file transfers
from sarracenia. The format of the reports is shown in the
[sr\_report(7)](sr_report.7.md) manual page. When clients download a
message from a site running sarracenia, they post information about
their success in doing so.

The **sr\_report** command takes two arguments: a configuration file
described below, followed by an action, one of: startrestartstatus or
foreground... (self described). sr\_report is sr\_subscribe with the
following settings changed:

    no-download True
    topic-prefix v02.report
    cache off
    accept_unmatch True
    report_back False

The **foreground** action is different. It is used when building a
configuration or debugging things, when the user wants to run the
program and its configfile interactively... The **foreground** instance
is not concerned by other actions, but should the configured instances
be running, it shares the same (configured) message queue.

The actions **cleanup**, **declare**, **setup** can be used to manage
resources on the rabbitmq server. The resources are either queues or
exchanges. **declare** creates the resources. **setup** creates and
additionnaly does the bindings of queues.

### CONFIGURATION

In general, the options for this component are described by the
[sr\_subscribe(1)](sr_subscribe.1.md) page which should be read first.
It fully explains the option configuration language, and how to find the
option settings.

#### EXAMPLES

Here is a short complete example configuration file:

    broker amqp://dd.weather.gc.ca/

    subtopic model_gem_global.25km.grib2.#
    accept .*

This above file will connect to the dd.weather.gc.ca broker, connecting
as anonymous with password anonymous (defaults) to obtain announcements
about files in the <http://dd.weather.gc.ca/model_gem_global/25km/grib2>
directory. All reports of downloads of those files present on the pump
will be accepted for processing by sr\_report.

#### SEE ALSO

[sr\_report(7)](sr_report.7.md) - the format of report messages.

[sr\_post(1)](sr_post.1.md) - post announcemensts of specific files.

[sr\_post(7)](sr_post.7.md) - The format of announcement messages.

[sr\_sarra(8)](sr_sarra.8.md) - Subscribe, Acquire, and ReAdvertise
tool.

[sr\_subscribe(1)](sr_subscribe.1.md) - Selectively Download files.

[sr\_watch(1)](sr_watch.1.md) - the directory watching daemon.

[<https://github.com/MetPX/>](https://github.com/MetPX/) - sr\_report is
a component of MetPX-Sarracenia, the AMQP based data pump.
