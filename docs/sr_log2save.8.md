SR\_Log2Save
============

Convert \_log Entries to .save Format for Reload
------------------------------------------------

Manual section

:   8

Date

:   @Date@

Version

:   @Version@

Manual group

:   Metpx-Sarracenia Suite

### SYNOPSIS

> **sr\_log2save**

### DESCRIPTION

In order to resend items to a given destination, one can recover the
advertisement for a given file given a standard log file entry for it.
*sr\_log2save* reads log files from standard input, and write them to
standard output converted into the save format usable by *sr\_shovel*
with *-restore\_to\_queue*.

#### EXAMPLE

Example usage::

:   cat \~/test/save.conf \<\<EOT

    broker amqp://<tfeed@localhost>/ topic\_prefix v02.post exchange
    xpublic

    post\_rate\_limit 5 on\_post post\_rate\_limit

    post\_broker amqp://<tfeed@localhost>/

    EOT

    sr\_log2save
    \<log/sr\_sarra\_download\_0003.log \>shovel/save/sr\_shovel\_save\_0000.save
    sr\_shovel -restore\_to\_queue
    q\_tsub.sr\_subscribe.t.99524171.43129428 foreground save.conf

#### SEE ALSO

[sr\_shovel(8)](sr_shovel.8.md) - copies messages between pumps.
