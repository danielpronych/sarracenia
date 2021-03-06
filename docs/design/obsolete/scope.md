Status: Draft

SCOPE
=====

Scope was the logical name of a switching cluster, which must be unique
in a network. Each cluster has channels to connect to either other
scopes, or single accounts. account is the logical name of a source
and/or client, which must be unique in a network.

What Happenned
--------------

This design info is completely out of date. It is the original ideas,
before it went into development. Brifely, this section outlines where we
ended up with afterward. Options:

cluster

:   identifying the current node on which the component is running. the
    name to put into the *from\_cluster* setting of

cluster\_aliases

:   other names that messages arriving might use to refer to a given
    cluster, besides it's primary name. Example DD might be a cluster
    alias active on dd1, dd2, dd3, etc...

gateway\_for

:   represents other clusters that are reachable through the current
    cluster. This is how administrators implement static routing. In
    Sarra, when examining to\_clusters=... of a message, if the
    destinations includes one of the cluster in gateway\_for, then sarra
    will download (subject to accept/reject.)

The above options need to be interpreted by sarra and sender, and well
that's it for data routing. Log routing ended up being treated
independently by the log2cluster.conf file, which is read by the
log2cluster component.

As often happens, as we worked through what we were trying to
accomplish, it got simpler.

Original Ideas
--------------

account2scope.conf: -- maps accounts to scopes.

:   \<scope\> \<account\>,\<account\>, ...

    not sure how this is maintained, likely by spying on post messages
    as they go by?

    If we just do our routing by scopes, maybe we do not need to map
    channels?

scope2channel.conf -- maps scopes to channels

:   \<channel/scope\> \<scope\>,\<scope\>,...

    perhaps a manually configured file, changes rarely, involves inter
    cluster relationships?

This is a switch global account file, to be used by validation scripts.
don´t know how it is created yet, perhaps manual, perhaps auto.

There are two kinds of channels:

:   -   inter-cluster / inter-scope / inter-switch.
    -   source / account

For a source channel, validation will insist that all postings received
are from that source.

for an inter-cluster/inter-scope/inter-switch channel:

:   the scopes2channel.conf file indicates scopes are valid from that
    channel.

    all postings will need to be from accounts listed in one of the
    valid scopes, so search the scopes\_accounts.conf file for each
    valid scope for that channel

    when log messages are returned: The log2src process consults these
    files and determines where to route log messages.

forget scopes, just use account names to stand for 'everyone' ?
---------------------------------------------------------------

Switch looks for a given user on it's own account, it does not find it,
but then it sees that that user is accessible (via account2scope) and
posts to that scope.

Given the mapping of account names to scopes... users just list the
accounts they want to have access. We have stand-in accounts for
'everyone' in a given scope.

Example:

:   to make data available to everyone in the 'interdepartmentalHPCOZ'
    we make a fake account: 'InterdepartmentalHPCOZ' which gets
    interpreted as making stuff 'public' for anyone that can access a
    server in that zone.

    We have another fake account called 'public' to mean anyone...

    using the account2scope.conf file, you find that 'public' is on
    dd.science.gc.ca and so routing is arranged to get stuff for
    'public' send to that scope.

might have cases where many accounts should be given access, does this
inevitably lead to 'groups'?

Earlier Stuff
-------------

NOTe: SCOPE ... permanent dd.

:   permanent URL´s for use in DOI´s. archiving? backups? new scope.

    this destination strips out the dates from the tree on receipt.

    --strip=n

    strip-count as used in the patch command.

upshot:

Sources control who sees their data. There is a 'Routing' that sources
need to say 'where' it gets posted. to get things posted to ´internet´
vs. ´internal´ etc...

Is it better to:

:   -   post once, listing multiple scopes?
    -   post once for each scope?

answer: it feels like listing multiple scopes ensures that the data is
only transferred once from origin.

Each account has a home 'scope' which is the only place they can insert
messages in. Do not want common passwords used on inside and outside
(hence single scope for insertion.)

when receiving a log message, it will be sent to the appropriate
exchange on the home scope.

Users are ´scope-local´ but visible to other scopes. Downstream scopes
do not have pw for user Alice in scope A. Assumption is that someone
else might control account assignment in other scopes. So user name
clashes are possible. There might be an Alice in scope A, and in scope
AA.

Any one scope may not be able to ¨see¨ all other scopes, it has to know
´routes´ to other scopes.

what are distributions/scopes?

:   -   does each source have a permission per scope ?
    -   does each source have a disk space allocation per scope?
    -   if you just set the allocation to 0, that's a permission.

    some more examples: ec, science, internet, warning

    original ddi will be deployed in ec, but will be tied into

    :   science.gc.ca switches. and be able to push to ddi.science.gc.ca
        so all of GoC will be reachable.

    warnings: high priority queue. only very few able to post there.

    :   how this works is unclear.

Admin functions:

:   alias scope a to scope b. maintain a list of scope routes? or have
    it all be dynamic and learning?

internal servers, or internet facing?

for each layer of switching, a list of valid scopes is defined? scope
corresponds to an exchange to which a given switch posts (outputs of
validation)

> -   
>
>     validate distribution/scope list (header?)
>
>     :   internet vs. escience (comma separated list) vs. warning? is
>         scope is invalid: reject.
>
>         are there scope permissions ? some source can only send to
>
Inter Scope Channel
-------------------

to go from scope A to scope B, on scope A.

set up a an exchange: xto\_B, and xfrom\_B (log B)?

on B, the complementary exchanges are established: xto\_A and xfrom\_A

If the source has specified ´B´ as a destination scope, then SARRA
places the announcement on xto\_B.

If A ´knows´ that C is reachable through B, then also put on xto\_B.

either a sr\_sender on A or a sr\_subscribe on B is subscribed to xto\_B
and does the data transfer.

The sr\_sender on A will then re-announce... where?

:   as B(!) on from\_A ? on B ?? as A on from\_A ? ?? \<-- makes more
    sense:

        then a SARRA (with no fetch, since the file is delivered)
        picks it up from exchange from_A and posts to xPublic

        (since this is a destination scope for the message)
            or do this unconditionally.
        it makes sense from permission perspective,
        scope A should only be able to post to from_A...

        so admin/sender user on <scope> would be something 
        like sr<scope>.  ddA.

if a sr\_subscribe on b does the transfer, then it is logged as ddB on
B.

Scope as Priority Mechanism
---------------------------

> If we create a wxwarn scope, then warnings go through that scope. i
> think this is not good. have a priority mechanism per source.
>
> if send to a warning scope it might just set the priority when copied
> to the common exchange, not requiring separate exchanges downstream.

scope as username of switching layer
------------------------------------

is scope the username of each switching layer? ssc\_ddsr, ssc\_ddi,
ssc\_dd each scope has an exchange scope\_ssc\_ddsr, scope\_ssc\_ddi,
scope\_ssc\_dd. what about warnings?

Scenarios
---------

want to transport a really large file (terabytes.)

:   target scope of ddsr (the parallel switching array.)

why check scope/distribution?

:   scopes: science, internet, warnings?

    correspond to exchanges. where things get posted. most source cannot
    post

    if we have a 'warnings' scope, then limit who can post to it.

transitivity:

:   there is an switch in EC that hands off to a switch in SSC an sr,
    that hands off to a public facing switch.

    that means each switch that connects to another one needs to pass

    :   the list of known scopes back.

    v01.cfg.scopes.get issued from a client, requests the list of scopes
    of the server.
