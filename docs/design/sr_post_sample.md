Status: Pre-Draft

Example of a Post message, with Discussion
==========================================

This example is for v01 syntax. Algorithms materially unchanged for v02,
but representation is different.

afsiext: user name assigned to us to retreive data on cmcdata server

:   client will not see this, private between source and ingest switch.

ec\_cmc: Account assigned for AMQP access. (rabbitmq username)

:   clients will see this... it is a public label for the source.

sr\_post -w exp13 NRDPS\_HiRes\_000.gif
<sftp://afsiext@cmcdataserver/data/NRDPS/outputs>
amqp://<ec_cmc@ddi/NRDPS/GIF>/

file is 457 bytes, blocksize is 0. flow is 'exp13' (by default, would be
'default') user settable, just passes through. DMS guys will appreciate
this, for labelling warning flows. checksum is done on actual data, not
the file name, or a script This is default behaviour.

sr\_post connects to the 'ec\_cmc' exchange with the ec\_cmc username on
bunny-op

posting is:

v01.post.ec\_cmc.NRDPS.GIF.NRDPS\_HiRes\_000.gif 201506011357.345 457 1
0 0 d \<md5sum\>
<sftp://afsiext@cmcdataserver/data/NRPDS/outputs/NRDPS_HiRes_000.gif>
NRDPS/GIF exp13

v01 - version of protocol post - indicates the type of message (defines
format of following topics and body)

> message types:
>
>     post - announce or notify that a new product block is available.
>          possible strings: post,ann(ounce), not(ify)
>     log  - report status of operations.
>     adm  - change settings 
>            'admin´, ´config´, etc...

> -- blocksize is 457 (== file size) -- block count is 1 -- remainder is
> 0. -- block number is 0. -- d - checksum was calculated on the body.
> -- Relative used to store relative destination directory -- flow is an
> argument after the relative path.

sr\_validate is subscribed to bunny-op (sr\_validate is perhaps just sr\_sarra with --prefetch )

:   -   checks that the block-size is legal.
    -   modifies the destination directory to
        YYYYMMDD/ec\_cmc/NRDPS/GIF/
    -   

        runs validscript on the data.

        :   -   IT Sec may want arbitrary scanning of data depending on
                source.
            -   only after the scan is complete do we post to the next
                hop.
            -   so the timing between post and accept can be
                significant.

    -   posts the result to the normal exchange (xpublic?)

v01.post.ec\_cmc.NRDPS.GIF.NRDPS\_HiRes\_000.gif 201506011357.445 1 457
0 0 d \<md5sum\>
<sftp://afsiext@cmcdataserver/data/NRPDS/outputs/NRDPS_HiRes_000.gif>
YYYYMMDD/ec\_cmc/NRDPS/GIF/ exp13

also emits a log message to log exchange:
v01.log.ec\_cmc.ssc\_ddsr.NRDPS.GIF.NRDPS\_HiRes\_000.gif
20150601135701.345 457 1 0 0 d \<md5sum\>
<sftp://afsiext@cmcdataserver/data/NRPDS/outputs/NRDPS_HiRes_000.gif>
YYYYMMDD/ec\_cmc/NRDPS/GIF/ exp13 202 ddsr1.cmc.ec.gc.ca ssc\_ddsr 0.1

if we go with HTTP error codes, then...

:   -- 202 is HTTP status code for ''Accepted'' meaning accepted for
    processing.

other options:

:   -- 400 bad request, in case of bad blocksize or other issue.

based on the v01.post above the log one...,

then sr\_sarra pulls the file in, and puts it on a local disk, in

:   /apps/sr/db/YYYYMMDD/ec\_cmc/GIF/NRDPS\_HiRes\_000.gif and it knows
    the root of the web tree is /apps/sr/... ?

then it needs to re-announce:

v01.post.ec\_cmc.NRDPS.GIF.NRDPS\_HiRes\_000.gif 201506011357.545 457 1
0 0 d \<md5sum\> <http://ddsr1.cmc.ec.gc.ca/db>
YYYYMMDD/ec\_cmc/NRDPS/GIF/NRDPS\_HiRes\_000.gif

?

sr\_sarra then emits a log entry:
v01.log.ec\_cmc.ssc\_ddsr.NRDPS.GIF.NRDPS\_HiRes\_000.gif
201506011358.345 457 1 0 0 d \<md5sum\> <http://ddsr1.cmc.ec.gc.ca/db>
YYYYMMDD/ec\_cmc/NRDPS/GIF/ exp13 200 ddsr1.cmc.ec.gc.ca ssc\_ddsr 0.1

> -   fields as in post, log.\<source\>.\<dest\>
> -   flowid: 'exp13'
> -   status codes (http) 200 means successful, so at this point, the
>     file has made it to ddsr.
> -   host that retrieved.
> -   on whose behalf (ssc\_ddsr account is AMQP user used on ddsr, one
>     per layer of switching ?)
> -   duration of transfer in seconds.

then a client with sr\_subscribe pulls it down, based on the post above.

then there is another hop, similar to the above, to get to
dd1.weather.gc.ca

amqp user: weather\_underground

v01.log.ec\_cmc.weather\_underground.NRDPS.GIF.NRDPS\_HiRes\_000.gif
201506011359.345 457 1 0 0 d \<md5sum\> <http://dd1.weather.gc.ca/db>
YYYYMMDD/ec\_cmc/NRDPS/GIF/ exp13 200 sv121.wug.org weather\_underground
1.0
