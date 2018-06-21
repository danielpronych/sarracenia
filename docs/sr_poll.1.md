SR\_Poll
========

Poll products from a remote server
----------------------------------

Manual section

:   1

Date

:   @Date@

Version

:   @Version@

Manual group

:   MetPx Sarracenia Suite

### SYNOPSIS

**sr\_poll** foregroundstopreload\|status configfile

**sr\_poll** cleanupsetup configfile

### DESCRIPTION

**sr\_poll** is a component that connects to a remote server to check in
various directories for some files. When a file is present, modified or
created in the remote directory, the program will notify about the new
product.

The notification protocol is defined here [sr\_post(7)](sr_post.7.md)

**sr\_poll** connects to a *broker*. Every *sleep* seconds, it connects
to a *destination* (sftp, ftp, ftps). For each of the *directory*
defined, it lists the contents. When a file matches a pattern given by
*accept*, **sr\_poll** builds a notification for that product and sends
it to the *broker*. The matching content of the *directory* is kept in a
file for reference. Should a matching file be changed, or created at a
later iteration, a new notification is sent.

**sr\_poll** can be used to acquire remote files in conjunction with an
[sr\_sarra(8)](sr_sarra.8.md) subscribed to the posted notifications,
to download and repost them from a data pump.

The **sr\_poll** command takes two argument: a configuration file
described below, followed by an action startrestartstatus...

The actions **cleanup**, **declare**, **setup** can be used to manage
resources on the rabbitmq server. The resources are either queues or
exchanges. **declare** creates the resources. **setup** creates and
additionnaly does the bindings of queues.

### CONFIGURATION

In general, the options for this component are described by the
[sr\_subscribe(1)](sr_subscribe.1.md) page which should be read first.
It fully explains the option configuration language, and how to find the
option settings.

#### DESTINATION OPTIONS

The destination option specify what is needed to connect to the remote
server

**destination protocol://\<user\>@\<server\>\[:port\]**

::

:   (default: None and it is mandatory to set it )

The *destination* should be set with the minimum required information...
**sr\_poll** uses *destination* setting not only when polling, but also
in the sr\_post messages produced.

For example, the user can set :

**destination <ftp://myself@myserver>**

And complete the needed information in the credentials file with the
line :

**<ftp://myself:mypassword@myserver:2121> passive,binary**

#### POLLING SPECIFICATIONS

These options set what files the user wants to be notified for and where

:   it will be placed, and under which name.

-   **filename \<option\> (optional)**
-   **directory \<path\> (default: .)**
-   **accept \<regexp pattern\> \[rename=\] (must be set)**
-   **reject \<regexp pattern\> (optional)**
-   **chmod \<integer\> (default: 0o400)**

The option *filename* can be used to set a global rename to the
products. Ex.:

**filename rename=/naefs/grib2/**

For all posts created, the *rename* option would be set to
'/naefs/grib2/filename' because I specified a directory (path that ends
with /)

The option *directory* defines where to get the files on the server.
Combined with **accept** / **reject** options, the user can select the
files of interest and their directories of residence.

The **accept** and **reject** options use regular expressions (regexp)
to match URL. These options are processed sequentially. The URL of a
file that matches a **reject** pattern is not published. Files matching
an **accept** pattern are published. Again a *rename* can be added to
the *accept* option... matching products for that *accept* option would
get renamed as described... unless the *accept* matches one file, the
*rename* option should describe a directory into which the files will be
placed (prepending instead of replacing the file name.)

The directory can have some patterns. These supported patterns concern
date/time . They are fixed...

**${YYYY} current year** **${MM} current month** **${JJJ} current
julian** **${YYYYMMDD} current date**

**${YYYY-1D} current year - 1 day** **${MM-1D} current month - 1 day**
**${JJJ-1D} current julian - 1 day** **${YYYYMMDD-1D} current date - 1
day**

    ex.   directory /mylocaldirectory/myradars
          accept    .*RADAR.*

          directory /mylocaldirectory/mygribs
          reject    .*Reg.*
          accept    .*GRIB.*

          directory /mylocaldirectory/${YYYYMMDD}/mydailies
          accept    .*observations.*

The **chmod** option allows users to specify a linux-style numeric octal
permission mask:

    chmod 040

means that a file will not be posted unless the group has read
permission (on an ls output that looks like: ---r-----, like a chmod 040
\<file\> command.) The **chmod** options specifies a mask, that is the
permissions must be at least what is specified.

#### POSTING SPECIFICATIONS

These options set what files the user wants to be notified for and where
**sr\_poll** polls the availability of file on a remote server by
creating an announcment for it. Subscribers use
[sr\_subscribe](sr_subscribe.1.md) to consume the announcement and
download the file (or **sr\_sarra**). To make files available to
subscribers, **sr\_poll** sends the announcements to an AMQP server,
also called a broker. Format of argument to the *broker* option:

    [amqp|amqps]://[user[:password]@]host[:port][/vhost]

The announcement will have its url built from the *destination* option,
with the product's path (*directory*/"matched file"). There is one post
per file. The file's size is taken from the directory "ls"... but it's
checksum cannot be determined, so the "sum" header in the posting is set
to "0,0."

By default, sr\_poll sends its post message to the broker with default
exchange is the prefix *[xs]()* followed by the broker username. The
*broker* is mandatory. It can be given incomplete if, it is well defined
in the credentials.conf file.

Refer to [sr\_post(1)](sr_post.1.md) - to understand the complete
notification process. Refer to [sr\_post(7)](sr_post.7.md) - to
understand the complete notification format.

Here it is important to say that :

The *sum=0,0* is used because no checksum computation was performed. It
is often desirable use the *sum=z,s* to have downloaders calculate a
useful checksum as they download for use by others.

The *parts=1,fsiz,1,0,0* is used and the file's size is taken from the
ls of the file. Under **sr\_sarra** these fields could be reset.

#### ADVANCED FEATURES

There are ways to insert scripts into the flow of messages and file
downloads: Should you want to implement tasks in various part of the
execution of the program:

-   **on\_line \<script\> (default: line\_mode)**
-   **do\_poll \<script\> (default: None)**
-   **on\_post \<script\> (default: None)**
-   **on\_html\_page \<script\> (default: html\_page)**

The **on\_line** plugin gives scripts that can read each line of an 'ls'
on the polled site, to interpret it further. return True, if the line
should be further processed, or False to reject it. By default, there is
a line\_mode plugin included with the package which implements the
comparison of file permission on the remote server against the **chmod**
mask. The program assumes that the very last word of the ls line is the
filename. This might not be the case if filenames might contains spaces.
For this purpose, the option **ls\_file\_index** can be used to set the
first word where the filename starts.

If the poll fetches using the http protocol, the 'ls' like entries must
be derived from an html page. The default plugin **html\_page** provided
with the package, gives an idea how to parse such a page into a python
directory managable by **sr\_poll**.

A do\_nothing.py script for **on\_post** could be:

class Transformer(object):

:   

    def \_\_init\_\_(self):

    :   pass

    def perform(self,parent):

    :   logger = parent.logger

        logger.info("I have no effect but adding this log line")

        return True

transformer = Transformer() self.on\_post = transformer.perform

The only arguments the script receives it **parent**, which is an
instance of the **sr\_poll** class

The **do\_poll** script could be written to support other protocol than
ftp,ftps,sftp. Again this script would be responsible to determine what
to do under its protocol with the various options **destination**,
**directory**, and should it determine to post a file, it would need to
build its url, partstr, sumstr and use

**parent.poster.post(parent.exchange,url,parent.to\_clusters, \*\***
partstr,sumstr,rename,remote\_file)\*\*

to post the message, applying accept/reject clauses and triggering
on\_post processing.

### DEPRECATED

The *get* option is a deprecated synonym for accept. Please use
*accept*.

**get \<regexp pattern\> \[rename=\] (must be set)**

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
