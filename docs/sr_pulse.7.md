sr\_pulse
=========

Sarracenia v02 Pulse Message Format/Protocol
--------------------------------------------

Date

:   @Date@

Version

:   @Version@

Manual section

:   7

Manual group

:   MetPX-Sarracenia

### SYNOPSIS

**AMQP Topic: \<version\>.pulse.\[tick\|message\]**

**Body:** *\<message\>*

### DESCRIPTION

Sr\_pulse messages are sent out periodically (default is every minute)
so that subscribers with very low frequency of subscription matches will
well maintain a connection, across firewalls. Consumers can check every
heartbeat (10 minutes by default) if they have received any pulses. If
no pulse has been received, the consumer can try an operation on the
channel to confirm connection with the broker. If no connection is
present, then consumers should teardown and re-build the it.

### AMQP TOPIC

The topic of a pulse message is prefixed with v02.pulse. The sub-topic
is either: *tick* for an ordinary keep-alive message, or *message* for
an administrator message intended for all subscribers.

### THE BODY

The body of the message in a *tick* is the standard timestamp (as in an
[sr\_post(7)](sr_post.7.md) message) Format:
*YYYYMMDDHHMMSS.*\<decimalseconds\>\* (Note: The datestamp is always in
UTC timezone.)

In the case of a message with the *v02.pulse.message* topic. The body is
a message to be posted in the logs of all subscribers.

### FURTHER READING

<https://github.com/MetPX> - home page of metpx-sarracenia

<http://rabbitmq.net> - home page of the AMQP broker used to develop
Sarracenia.

### SEE ALSO

[sr\_subscribe(1)](sr_subscribe.1.md) - the http-only download client.

[sr\_post(1)](sr_post.1.md) - post announcements of specific files.

[sr\_post(7)](sr_post.7.md) - The format of announcement messages.

[sr\_report(1)](sr_report.1.md) - process report messages.

[sr\_sarra(8)](sr_sarra.8.md) - Subscribe, Acquire, and ReAdvertise
tool.

[sr\_watch(1)](sr_watch.1.md) - the directory watching daemon.
