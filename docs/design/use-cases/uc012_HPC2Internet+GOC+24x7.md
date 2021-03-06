HPC2Internet+GOC+24x7
=====================

> Overview: Edmond from Environment Canada, from the climate research
> wants to make data available both to the public and colleagues within
> government in a reliable way (24x7)
>
> AMQP layer:
>
> :   sr\_post to ddsr.science.gc.ca to xclimate\_research
>     sr\_sara/validates & dispatch.
>
>     svrddsr1 fetchs a file via sftp to post on local http svr.
>
>     :   (assuming possible ... see data layer)
>
>     works as uddsr on the AMQP level...
>
>     readvertises as ddsr1 to: xto\_ddi, xto\_dd
>
>     ddi1, ddi2, are subscribed to xto\_ddi, and they pull the data
>     down.
>
>     sr\_sender is subscribed to put the files on dd.collab.
>
>     :   
>
>         posts to xfrom\_ddsr on dd.collab ?
>
>         :   or just straight to xPublic? as amqp user uddsr?
>
>         or as amqp user udd ?
>
> Data Layer:
>
>     .1 switch in EC
>
> ddsr initiates an sftp retrieval from the EC to Science system
>
> :   (will not work, blocked by fw) this does work if there is a
>     switching level within EC.
>
> .0 no switching layer within EC:
>
> :   EC user uses sr\_send to upload.
>
>     once on svrDDSRx ddiX will pull via http from svrDDSRx svrDDSRx
>     will sftp to dd.collab.
>
> clients pull from dd and ddi via http
>
> Log Layer:
>
> .1
>
> :   v01.log.uclimate\_research.uddsr 200 -- retrieved by ddsr
>
> .0
>
> :   v01.log.uclimate\_research.uclimate\_research 200 -- delivered by
>     client.
>
>     (dispatch is silent?)
>
>     v01.log.uclimate\_research.uddi 200 -- delivered to ddi
>     v01.log.uclimate\_research.udd 200 -- delivered to dd
>
FIXME:

:   

    so when uploaded by client you see log message v01.log.u.u 200

    :   something watches the xac\_u exchange, and when it sees that, it
        triggers a validation step (pre and post), and if it is OK, it
        moves it to a waf accessible directory and re-announce as
        normal.

    1. Storage Distribution

    :   user EC auth on EC server at source.

    .1

    :   copies directly to the right place by ddsr (trusted process)

    .0

    :   client copies to sftp upload area (not trusted) \<this needs to
        move to a ´trusted´ area (ie. www visible.)

    2\. Server s/w Distribution. remote host has sr-sarracenia clients,
    sr\_post (.0) and sr\_send (.1) ddsr needs sftp server, and one (H/A)
    rabbit per cluster?

    3. Authentication Distribution.

    :   

        EC auth on EC system. (.0) EC assigns auth for ddsr to connect to EC system.

        :   in (.1) ddsr assigns auth for EC user on ddsr for upload

    in .0

    :   

        once on the switch, it somehow becomes ddsr property (a chown?)

        :   then needs to pu

    1.  Naming/Scopes
    2.  Retention/Quota strategy.
    3.  bandwidth/scaling

    Observations: While Edmond makes a single post, this could result in
    many different servers copying the data. It is simply an injection
    into a file propagation network.
