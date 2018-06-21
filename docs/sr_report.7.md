sr\_report
==========

Sarracenia v02 Report Message Format/Protocol
---------------------------------------------

Date

:   @Date@

Version

:   @Version@

Manual section

:   7

Manual group

:   MetPX-Sarracenia

### SYNOPSIS

\**AMQP Topic: \<version\>.report.{\<dir\>.}*\<filename\>\*\*

**AMQP Headers:** *\<series of key-value pairs\>*

**Body:** *\<first line\>*

*\<first line\> == \<date stamp\> \<base\_url\> \<relpath\>
\<statuscode\> \<consuminghost\> \<consuminguser\> \<duration\>
\<newline\>*

*\<rest of body is reserved for future use\>*

### DESCRIPTION

Sources create messages in the *sr\_post* format to announce file
changes. Subscribers read the post to decide whether a download of the
content being announced is warranted. Subscribers may provide
information to sources by sending a report message indicating the result
of processing a post. The report message format, described by this
specification, is the posting echoed back to the source with a few small
changes. Please consult the sr\_post(7) man page for a full explanation
of the fields which are shared with the posting format.

A sr\_report message consists of four parts:

    AMQP TOPIC, First Line, Rest of Message, AMQP HEADERS.

### AMQP TOPIC

The topic of a report message is similar to sr\_post except that the
second sub-topic is 'report' rather than 'post'.

### THE FIRST LINE

the first line of a message contains all mandatory elements of an
sr\_post(7) announcement. There is a series of white space separated
fields:

    *<date stamp>* : the date the posting was emitted.
    Format: *YYYYMMDDHHMMSS.*<decimalseconds>*
    Note: The datestamp is always in UTC timezone.

*\<base\_url\>* : -- the base URL used to retrieve the data.

This should be the URL consumers will use to download the data. Example
of a complete URL:

> <sftp://afsiext@cmcdataserver/data/NRPDS/outputs/NRPDS_HiRes_000.gif>

In the case where the URL does not end with a path separator ('/'), the
src path is taken to be the complete source of the file to retrieve.

> Static URL: <sftp://afsiext@cmcdataserver/>

If the URL ends with a path separator ('/'), then the src URL is
considered a prefix for the variable part of the retrieval URL.

*\<relativepath\>* : the variable part of the URL, usually appended to
*\<base\_url\>*

The above are the fields taken from the sr\_post(7) format. There are
additional fields in the sr\_report:

*\<statuscode\>* a three digit status code, adopted from the HTTP
protocol (w3.org/IETF RFC 2616)

As per the RFC, any code returned should be interpreted as follows:

> -   2xx indicates successful completion,
> -   3xx indicates further action is required to complete the
>     operation.
> -   4xx indicates a permanent error on the client prevented a
>     successful operation.
> -   5xx indicates a problem on the server prevented successful
>     operation.

Note

FIXME: need to validate whether our use of error codes co-incides with
the general intent expressed above... does a 3xx mean we expect the
client to do something? does 5xx mean that the failure was on the
broker/server side?

The specific error codes returned, and their meaning are implementation
dependent. For the sarracenia implementation, the following codes are
defined:

<table>
<colgroup>
<col style="width: 10%" />
<col style="width: 89%" />
</colgroup>
<thead>
<tr class="header">
<th>Code</th>
<th>Corresponding text and meaning for sarracenia implementation</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><blockquote>
<p>201</p>
</blockquote></td>
<td>Download successful. (variations: Downloaded, Inserted, Published, Copied, or Linked)</td>
</tr>
<tr class="even">
<td><blockquote>
<p>205</p>
</blockquote></td>
<td>Reset Content: truncated. file is shorter than originally expected (changed length during transfer) This only arises during multi-part transfers.</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>205</p>
</blockquote></td>
<td>Reset Content: checksum recalculated on receipt.</td>
</tr>
<tr class="even">
<td><blockquote>
<p>304</p>
</blockquote></td>
<td>not modified (Checksum validated, unchanged, so no download resulted.)</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>307</p>
</blockquote></td>
<td>insertion deferred (writing to temporary part file for the moment.)</td>
</tr>
<tr class="even">
<td><blockquote>
<p>417</p>
</blockquote></td>
<td>Expectation Failed: invalid message (corrupt headers)</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>499</p>
</blockquote></td>
<td>Failure: Not Copied. SFTP/FTP/HTTP download problem</td>
</tr>
<tr class="even">
<td><blockquote>
<p>503</p>
</blockquote></td>
<td>Service unavailable. delete (File removal not currently supported.)</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>503</p>
</blockquote></td>
<td>Unable to process: Service unavailable,</td>
</tr>
<tr class="even">
<td><blockquote>
<p>503</p>
</blockquote></td>
<td>unsupported transport protocol specified in posting.</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>xxx</p>
</blockquote></td>
<td>message and file validation status codes are script dependent</td>
</tr>
</tbody>
</table>

*\<consuminghost\>* hostname from which the retrieval was initiated.

*\<consuminguser\>* broker username from which the retrieval was
initiated.

*\<duration\>* how long processing took, in (decimal) seconds

*\<newline\>* signals the end of the first line of the message and is
denoted by a single line feed character.

### THE REST OF MESSAGE

Use of only the first line of the AMQP payload is currently defined. The
rest of the payload body is reserved for future use.

### AMQP HEADERS

In addition to the first line of the message containing all mandatory
fields, optional elements are stored in AMQP headers (key-value pairs),
included in messages when appropriate. In addition to the headers
specified in the sr\_post(7) manual page, the following report-specific
headers are defined:

message=\<msgstring\>

An English textual representation of the status code. as per w3.org/IETF
RFC 2616 Status Code Definitions.

### EXAMPLE

    topic: v02.report.NRDPS.GIF.NRDPS_HiRes_000.gif
    first line: 201506011357.345 sftp://afsiext@cmcdataserver/data/NRPDS/outputs/NRDPS_HiRes_000.gif NRDPS/GIF/ 201 castor anonymous 0.0006767
    headers: parts=p,457,1,0,0 sum=d,<md5sum> flow=exp13 message=Downloaded source=ec_cmc from_cluster=ddi.cmc.ec.gc.ca to_clusters=ddi.science.gc.ca,bunny.nrcan.gc.ca


      v02 - version of protocol
      report - indicates the type of message

           version and type together specify the format of the message.

      ec_cmc - the account used to issue the post (unique in a network).

      ddi.cmc.ec.gc.ca - the originating cluster for that product

      ddi.science.gc.ca,bunny.nrcan.gc.ca - the destination clusters for that product

             -- blocksize is 457  (== file size)
             -- block count is 1
             -- remainder is 0.
             -- block number is 0.
             -- d - checksum was calculated on the body of the file.
             -- flow is an argument after the relative path.
             -- complete source URL specified (does not end in '/')
             -- relative path specified for

      pull from:
                   sftp://afsiext@cmcdataserver/data/NRPDS/outputs/NRDPS_HiRes_000.gif

      complete relative download path:
                   NRDPS/GIF/NRDPS_HiRes_000.gif

                   -- takes file name from base_url.
                   -- may be modified by validation process.

      message download succeeded (201) from host castor, as user anonymous, and took 0.006767 seconds.

### FURTHER READING

<https://github.com/MetPX> - home page of metpx-sarracenia

<http://rabbitmq.net> - home page of the AMQP broker used to develop
Sarracenia.

### SEE ALSO

[sr\_post(1)](sr_post.1.md) - post announcements of specific files.

[sr\_post(7)](sr_post.7.md) - The format of announcement messages.

[sr\_pulse(7)](sr_pulse.7.md) - The format of pulse messages.

[sr\_report(1)](sr_report.1.md) - process report messages.

[sr\_sarra(8)](sr_sarra.8.md) - Subscribe, Acquire, and ReAdvertise
tool.

[sr\_subscribe(1)](sr_subscribe.1.md) - the http-only download client.

[sr\_watch(1)](sr_watch.1.md) - the directory watching daemon.
