SR\_post
========

Sarracenia v02 Post Message Format/Protocol
-------------------------------------------

Manual section

:   7

Date

:   @Date@

Version

:   @Version@

Manual group

:   MetPX-Sarracenia

### SYNOPSIS

The format of file change announcements for sr\_post.

A sr\_post message consists of four parts: **AMQP TOPIC, First Line,
Rest of Message, AMQP HEADERS.**

**AMQP Topic:** *\<version\>.post.{\<dir\>.}*

    <version> = "v02" the version of the protocol or format.
    "post" = the type of message within the protocol.
    <dir> = a sub-directory leading to the file (perhaps many directories deep)
    <filename> = the name of the file on the server.

**AMQP Headers:** *\<series of key-value pairs\>*

::

:   "parts" = size and partitioning information. "sum" = checksum
    algorithm and value.

**Body:** *\<first line\> = \<date stamp\> \<base\_url\> \<relpath\>
\<newline\>*

    <date stamp> - YYYYMMDDHHMMSS.ss - UTC date/timestamp.
    <base_url>   - root of the url to download.
    <relpath>    - relative path perhaps catenated to <base_url>
                   may instead be a rename.

\<*rest of body is reserved for future use*\>

### DESCRIPTION

Sources create messages in the *sr\_post* format to announce file
changes. Subscribers read the post to decide whether a download of the
content being announced is warranted. This manual page completely
describes the format of those messages. The messages are payloads for an
Advanced Message Queuing Protocol (AMQP) message bus, but file data
transport is separate, using more common protocols such as SFTP, HTTP,
HTTPS, or FTP (or other?) Files are transported as pure byte streams, no
metadata beyond the file contents is transported (permission bits,
extended attributes, etc...) Permissions of files on the destination
system are upto the receiver to decide.

With this method, AMQP messages provide a 'control plane' for data
transfers. While each post message is essentially point to point, data
pumps can be transitively linked together to make arbitrary networks.
Each posting is consumed by the next hop in the chain. Each hop
re-advertises (creates a new post for) the data for later hops. The
posts flow in the same direction as the data. If consumers permit it,
report messages (see sr\_report(7)) also flow through the control path,
but in the opposite direction, allowing sources to know the entire
disposition of their files through a network.

The minimal layer over raw AMQP provides more complete file transfer
functionality:

Source Filtering (use of [AMQP TOPIC](#amqp-topic) exchanges)

:   The messages make use of *topic exchanges* from AMQP, where topics
    are hierarchies meant to represent subjects of interest to a
    consumer. A consumer may upload the selection criteria to the broker
    so that only a small subset of postings are forwarded to the client.
    When there are many users interested in only small subsets of data,
    the savings in traffic are large.

Fingerprint Winnowing (use of the [sum](#sum) header)

:   Each product has a checksum and size intended to identify it
    uniquely, referred to as a *fingerprint*. If two files have the same
    fingerprint, they are considered equivalent. In cases where multiple
    sources of equivalent data are available but downstream consumers
    would prefer to receive single announcements of files, intermediate
    processes may elect to publish notifications of the first product
    with a given fingerprint, and ignore subsequent ones. Propagating
    only the first occurrence of a datum received downstream, based on
    its fingerprint, is termed: *Fingerprint Winnowing*.

    *Fingerprint Winnowing* is the basis for a robust strategy for high
    availability: Setting up multiple sources for the same data,
    consumers accept announcements from all of them, but only forwarding
    the first one received downstream. In normal operation, one source
    may be faster than the others, and so the other sources' files are
    usually 'winnowed'. When one source disappears, the other sources'
    data is automatically selected, as the fingerprints are now *fresh*
    and used, until a faster source becomes available.

    The advantage of this method for high availability is that no A/B
    decision is required. The time to *switchover* is zero. Other
    strategies are subject to considerable delays in making the decision
    to switchover, and pathologies one could summarize as flapping,
    and/or deadlocks.

    *Fingerprint Winnowing* also permits *mesh-like*, or *any to any*
    networks, where one simply interconnects a node with others, and
    messages propagate. Their specific path through the network is not
    defined, but each participant will download each new datum from the
    first node that makes it available to them. Keeping the messages
    small and separate from data is optimal for this usage.

Partitioning (use of the [parts](#parts) Header)

:   In any store and forward data pumping network that transports entire
    files limits the maximum file size to the minimum available on any
    intervening node. To avoid defining a maximum file size, a
    segmentation standard is specified, allowing intervening nodes to
    hold only segments of the file, and forward them as they are
    received, rather than being forced to hold the entire file.

    Partitioning also permits multiple streams to transfer portions of
    the file in parallel. Multiple streams can provide an effective
    optimization over long links.

### AMQP TOPIC

In topic based AMQP exchanges, every message has a topic header. AMQP
defines the '.' character as a hierarchical separator (like '' in a
windows path name, or '/' on linux) there is also a pair of wildcards
defined by the standard: '\*' matches a single topic, '\#' matches the
rest of the topic string. To allow for changes in the message body in
the future, topic trees begin with the version number of the protocol.

AMQP allows server side topic filtering using wildcards. Subscribers
specify topics of interest (which correspond to directories on the
server), allowing them to pare down the number of notifications sent
from server to client.

The root of the topic tree is the version specifier: "v02". Next comes
the message type specifier. These two fields define the protocol that is
in use for the rest of the message. The message type for post messages
is "post". After the fixed topic prefix, the remaining sub-topics are
the path elements of the file on the web server. For example, if a file
is placed on <http://www.example.com/a/b/c/d/foo.txt>, then the complete
topic of the message will be: *v02.post.a.b.c.d* AMQP fields are limited
to 255 characters, and the characters in the field are utf8 encoded, so
actual length limit may be less than that.

### THE FIRST LINE

the first line of a message contains all mandatory elements of an
announcement. There is a series of white space separated fields:

*\<date stamp\>*: the date the posting was emitted. Format:
YYYYMMDDHHMMSS. *\<decimalseconds\>*

> Note: The datestamp is always in the UTC timezone.

*\<base\_url\>* -- the base URL used to retrieve the data.

The URL consumers will use to download the data. Example of a complete
URL:

    sftp://afsiext@cmcdataserver/data/NRPDS/outputs/NRPDS_HiRes_000.gif

*\<relativepath\>* the variable part of the URL, usually appended to
*base\_url*.

*\<newline\>* signals the end of the first line of the message and is
denoted by a single line feed character.

### THE REST OF MESSAGE

Use of only the first line of the AMQP payload is currently defined. The
rest of the payload body is reserved for future use.

### AMQP HEADERS

In addition to the first line of the message containing all mandatory
fields, optional elements are stored in AMQP headers (utf8 encoded
key-value pairs limited to 255 bytes in length), included in messages
when appropriate.

**from\_cluster=\<cluster\_name\>**

:   The from\_cluster defines the name of the source cluster where the
    data was introduced into the network. It is used to return the logs
    back to the cluster whenever its products are used.

**link=\<value of symbolic link\>**

:   when file to transfer is a symbolic link, the 'link' header is
    created to contain its value.

**parts=\<method\>,\<bsz\>,\<blktot\>,\<brem\>,\<bno\>**

> A header indicating the method and parameters for partitioning applied
> for the file. Partitioning is used to send a single file as a
> collection of segments, rather than as a single entity. Partitioning
> is used to accellerate transfers of large data sets by using multiple
> streams, and/or to reduce storage use for extremely large files.
>
> when transferring partitioned files, each partition is advertised and
> potentially transported independently across a data pumping network.
>
> *\<method\>*
>
> Indicates what partitioning method, if any, was used in transmission.
>
> <table>
> <colgroup>
> <col style="width: 14%" />
> <col style="width: 85%" />
> </colgroup>
> <tbody>
> <tr class="odd">
> <td><blockquote>
> <p>Method</p>
> </blockquote></td>
> <td>Description</td>
> </tr>
> <tr class="even">
> <td><blockquote>
> <p>p</p>
> </blockquote></td>
> <td>File is partitioned, individual part files are created.</td>
> </tr>
> <tr class="odd">
> <td><blockquote>
> <p>i</p>
> </blockquote></td>
> <td>file is partitioned, but blocks are read from a single file, rather than parts.</td>
> </tr>
> <tr class="even">
> <td><blockquote>
> <p>1</p>
> </blockquote></td>
> <td>file is in a single part (no partitioning)</td>
> </tr>
> </tbody>
> </table>
>
> -   analogous to rsync options: --inplace, --partial,
>
> *\<blocksize in bytes\>: bsz*
>
> The number of bytes in a block. When using method 1, the size of the
> block is the size of the file. Remaining fields only useful for
> partitioned files.
>
> *\<blocks in total\>: blktot* the integer total number of blocks in
> the file (last block may be partial)
>
> *\<remainder\>: brem* normally 0, on the last block, remaining bytes
> in the file to transfer.
>
> > -- if (fzb=1 and brem=0)
> >
> > :   then bsz=fsz in bytes in bytes. -- entire files replaced. --
> >     this is the same as rsync's --whole-file mode.
> >
> *\<block\#\>: bno* 0 origin, the block number covered by this posting.

**rename=\<relpath\>**

> *DEPRECATED* Do Not use. The relative path from the current directory
> in which to place the file.

**oldname=\<path\>** **newname=\<path\>**

> when a file is renamed at the source, to send it to subscribers, two
> posts result: One message is announced with the new name as the
> base\_url, and the oldname header set to the previous file name.
> Another message is send with the old name as the src path, and the
> *newname* as a header. This ensures that *accept/reject* clauses are
> correctly interpreted, as a *rename* may result in a download if the
> former name matches a *reject* clause, or a file removal if the new
> name is matches a *reject* clause.
>
> hard links are also handled as an ordinary post of the file with a
> *oldname* header set.

**source=\<sourceid\>**

:   a character field indicating the source of the data injected into
    the network. should be unique within a data pumping network. Usually
    is the same as the account used to authenticate to the broker.

**sum=\<method\>,\<value\>**

> The sum is a signature computed to allow receivers to determine if
> they have already downloaded the partition from elsewhere.
>
> *\<method\>* - character field indicating the checksum algorithm used.
>
> <table>
> <colgroup>
> <col style="width: 14%" />
> <col style="width: 85%" />
> </colgroup>
> <tbody>
> <tr class="odd">
> <td><blockquote>
> <p>Method</p>
> </blockquote></td>
> <td>Description</td>
> </tr>
> <tr class="even">
> <td><blockquote>
> <p>0</p>
> </blockquote></td>
> <td>no checksums (unconditional copy.) Skips reading file (faster)</td>
> </tr>
> <tr class="odd">
> <td><blockquote>
> <p>d</p>
> </blockquote></td>
> <td>checksum the entire data (MD-5 as per IETF RFC 1321)</td>
> </tr>
> <tr class="even">
> <td><blockquote>
> <p>L</p>
> </blockquote></td>
> <td>Linked: SHA512 sum of link value</td>
> </tr>
> <tr class="odd">
> <td><blockquote>
> <p>n</p>
> </blockquote></td>
> <td>checksum the file name (MD-5 as per IETF RFC 1321)</td>
> </tr>
> <tr class="even">
> <td><blockquote>
> <p>R</p>
> </blockquote></td>
> <td>Removed: SHA512 of file name.</td>
> </tr>
> <tr class="odd">
> <td><blockquote>
> <p>s</p>
> </blockquote></td>
> <td>checksum the entire data (SHA512 as per IETF RFC 6234)</td>
> </tr>
> <tr class="even">
> <td><blockquote>
> <p>z</p>
> </blockquote></td>
> <td>checksum on download, with algorithm as argument example: z,d means download, applying d checksum, and advertise with that calculated checksum when propagating further.</td>
> </tr>
> <tr class="odd">
> <td><blockquote>
> <p><em>&lt;name&gt;</em></p>
> </blockquote></td>
> <td>checksum with a some other algorithm, named <em>&lt;name&gt;</em> <em>&lt;name&gt;</em> should be <em>registered</em> in the data pumping network. registered means that all downstream subscribers can obtain the algorithm to validate the checksum.</td>
> </tr>
> </tbody>
> </table>
>
*\<value\>* The value is computed by applying the given method to the partition being transferred.

:   for algorithms for which no value makes sense, a random integer is
    generated to support checksum based load balancing.

**to\_clusters=\<cluster\_name1,cluster\_name2,...\>**

:   The to\_clusters defines a list of destination clusters where the
    data should go into the network. Each name should be unique within
    all exchanging rabbitmq clusters. It is used to do the transit of
    the products and their notices through the exchanging clusters.

All other headers are reserved for future use. Headers which are unknown
to a given client should be forwarded without modification.

### EXAMPLE

    Topic: v02.post.NRDPS.GIF.NRDPS_HiRes_000.gif
    first line: 201506011357.345 sftp://afsiext@cmcdataserver/data/NRPDS/outputs/NRDPS_HiRes_000.gif NRDPS/GIF/  
    Headers: parts=p,457,1,0,0 sum=d,<md5sum> source=ec_cmc

           - v02 - version of protocol
           - post - indicates the type of message
           - version and type together determine format of following topics and the message body.

           - blocksize is 457  (== file size)
           - block count is 1
           - remainder is 0.
           - block number is 0.
           - d - checksum was calculated on the body of the file.
           - complete source URL specified (does not end in '/')
           - relative path specified for

           pull from:
                   sftp://afsiext@cmcdataserver/data/NRPDS/outputs/NRDPS_HiRes_000.gif

           complete relative download path:
                   NRDPS/GIF/NRDPS_HiRes_000.gif

                   -- takes file name from base_url.
                   -- may be modified by validation process.

### Another example

The post resulting from the following sr\_watch command, noticing
creation of the file 'foor':

    sr_watch -s sftp://stanley@mysftpserver.com//data/shared/products/foo -pb amqp://broker.com

Here, *sr\_watch* checks if the file /data/shared/products/foo is
modified. When it happens, *sr\_watch* reads the file
/data/shared/products/foo and calculates its checksum. It then builds a
post message, logs into broker.com as user 'guest' (default credentials)
and sends the post to defaults vhost '/' and exchange 'sx\_guest'
(default exchange)

A subscriber can download the file /data/shared/products/foo by logging
as user stanley on mysftpserver.com using the sftp protocol to
broker.com assuming he has proper credentials.

The output of the command is as follows :

    Topic: v02.post.20150813.data.shared.products.foo
    1st line of body: 20150813161959.854 sftp://stanley@mysftpserver.com/ /data/shared/products/foo
    Headers: parts=1,256,1,0,0 sum=d,25d231ec0ae3c569ba27ab7a74dd72ce source=guest

Posts are published on AMQP topic exchanges, meaning every message has a
topic header. The body consists of a time *20150813161959.854*, followed
by the two parts of the retrieval URL. The headers follow with firs the
*parts*, a size in bytes *256*, the number of block of that size *1*,
the remaining bytes *0*, the current block *0*, a flag *d* meaning the
md5 checksum is performed on the data, the checksum
*25d231ec0ae3c569ba27ab7a74dd72ce*,

### MetPX-Sarracenia

The Metpx project ( <https://github.com/MetPX> ) has a sub-project
called Sarracenia which is intended as a testbed and reference
implementation for this protocol. This implementation is licensed using
the General Public License (Gnu GPL v2), and is thus free to use, and
can be used to confirm interoperability with any other implementations
that may arise. While Sarracenia itself is expected to be very usable in
a variety of contexts, there is no intent for it to implement any
features not described by this documentation.

This Manual page is intended to completely specify the format of
messages and their intended meaning so that other producers and
consumers of messages can be implemented.

### AMQP Feature Selection

AMQP is a universal message passing protocol with many different options
to support many different messaging patterns. MetPX-sarracenia specifies
and uses a small subset of AMQP patterns. An important element of
sarracenia development was to select from the many possibilities a small
subset of methods are general and easily understood, in order to
maximize potential for interoperability.

Specifying the use of a protocol alone may be insufficient to provide
enough information for data exchange and interoperability. For example
when exchanging data via FTP, a number of choices need to be made above
and beyond the protocol.

> -   authenticated or anonymous use?
> -   how to signal that a file transfer has completed (permission bits?
>     suffix? prefix?)
> -   naming convention.
> -   text or binary transfer.

Agreed conventions above and beyond simply FTP (IETF RFC 959) are
needed. Similar to the use of FTP alone as a transfer protocol is
insufficient to specify a complete data transfer procedure, use of AMQP,
without more information, is incomplete. The intent of the conventions
layered on top of AMQP is to be a minimum amount to achieve meaningful
data exchange.

AMQP 1.0 standardizes the on the wire protocol, but leaves out many
features of broker interaction. As the use of brokers is key to
sarracenia´s use of, was a fundamental element of earlier standards, and
as the 1.0 standard is relatively controversial, this protocol assumes a
pre 1.0 standard broker, as is provided by many free brokers, such as
rabbitmq, often referred to as 0.8, but 0.9 and post 0.9 brokers are
also likely to inter-operate well.

In AMQP, many different actors can define communication parameters. in
RabbitMQ (the initial broker used), permissions are assigned using
regular expressions. So a permission model where AMQP users can define
and use *their* exchanges and queues is enforced by a naming convention
easily mapped to regular expressions (all such resources include the
username near the beginning.) Exchanges begin with: [xs]()\<user\>\_.
Queue names begin with: [q]()\<user\>\_.

Note

FIXME: other connection parameters: persistence, etc..

Topic-based exchanges are used exclusively. AMQP supports many other
types of exchanges, but sr\_post have the topic sent in order to support
server side filtering by using topic based filtering. The topics mirror
the path of the files being announced, allowing straight-forward
server-side filtering, to be augmented by client-side filtering on
message reception.

The root of the topic tree is the version of the message payload. This
allows single brokers to easily support multiple versions of the
protocol at the same time during transitions. *v02*, created in 2015, is
the third iteration of the protocol and existing servers routinely
support previous versions simultaneously in this way. The second
sub-topic defines the type of message. at the time of writing: v02.post
is the topic prefix for current post messages.

The AMQP messages contain announcements, no actual file data. AMQP is
optimized for and assumes small messages. Keeping the messages small
allows for maximum message throughtput and permits clients to use
priority mechanisms based on transfer of data, rather than the
announcements. Accomodating large messages would create many practical
complications, and inevitably require the definition of a maximum file
size to be included in the message itself, resulting in complexity to
cover multiple cases.

sr\_post is intended for use with arbitrarily large files, via
segmentation and multi-streaming. blocks of large files are announced
independently. and blocks can follow different paths between initial
pump and final delivery. The protocol is unidirectional, in that there
is no dialogue between publisher and subscriber. Each post is a
stand-alone item that is one message in a stream, which on receipt may
be spread over a number of nodes.

### CHARACTER SET & ENCODING

All messages are expected to use the UNICODE character set (ISO 10646),
represented by UTF-8 encoding (IETF RFC 3629.) URL encoding, as per IETF
RFC 1738, is used to escape unsafe characters where appropriate.

### FURTHER READING

<https://github.com/MetPX> - home page of metpx-sarracenia

<http://rabbitmq.net> - home page of the AMQP broker used to develop
Sarracenia.

#### SEE ALSO

[sr\_report(7)](sr_report.7.md) - the format of report messages.

[sr\_pulse(7)](sr_pulse.7.md) - The format of pulse messages.

[sr\_report(1)](sr_report.1.md) - process report messages.

[sr\_post(1)](sr_post.1.md) - post announcemensts of specific files.

[sr\_sarra(8)](sr_sarra.8.md) - Subscribe, Acquire, and ReAdvertise
tool.

[sr\_subscribe(1)](sr_subscribe.1.md) - the download client.

[sr\_watch(1)](sr_watch.1.md) - the directory watching daemon.

tree [dd\_subscribe(1)](dd_subscribe.1.md) - the http-only download
client.
