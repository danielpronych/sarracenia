MetPX-Sarracenia
================

**Documentation**

-   Guides: \[ [Guides](doc/sr_subscribe.1.md#documentation) \] \[ [en
    français](doc/fr/sr_subscribe.1.md#documentation) \]
-   Reference: \[ [Manual Pages](doc/sr_subscribe.1.md#see-also) \] \[
    [en français](doc/fr/sr_subscribe.1.md#aussi-voir) \]

<table>
<colgroup>
<col style="width: 49%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td><blockquote>
<p>Overview</p>
</blockquote></td>
<td><blockquote>
<p>Survol</p>
</blockquote></td>
</tr>
<tr class="even">
<td><p>MetPX-Sarracenia is a data duplication or distribution pump that leverages existing standard technologies (web servers and the <a href="http://www.amqp.org">AMQP</a> brokers) to achieve real-time message delivery and end to end transparency in file transfers. Data sources establish a directory structure which is carried through any number of intervening pumps until they arrive at a client. The client can provide explicit acknowledgement that propagates back through the network to the source. Whereas traditional file switching is a point-to-point affair where knowledge is only between each segment, in Sarracenia, information flows from end to end in both directions.</p>
<p>At it's heart, sarracenia exposes a tree of web accessible folders (WAF), using any standard HTTP server (tested with apache). Weather applications are soft real-time, where data should be delivered as quickly as possible to the next hop, and minutes, perhaps seconds, count. The standard web push technologies, ATOM, RSS, etc... are actually polling technologies that when used in low latency applications consume a great deal of bandwidth an overhead. For exactly these reasons, those standards stipulate a minimum polling interval of five minutes. Advanced Message Queueing Protocol (AMQP) messaging brings true push to notifications, and makes real-time sending far more efficient.</p></td>
<td><p>MetPX-Sarracenia est un engin de copie et de distribution de données qui utilise des technologies standards (tel que les services web et le courtier de messages AMQP) afin d'effectuer des transferts de données en temps réel tout en permettant une transparence de bout en bout. Alors que chaque commutateur Sundew est unique en soit, offrant des configurations sur mesure et permutations de données multiples, Sarracenia cherche à maintenir l'intégrité de la structure des données, tel que proposée et organisée par la source jusqu'à destination. Le client peut fournir des accusés de réception qui se propagent à travers tous les noeuds de la chaîne, en sens inverse jusqu'à la source. Tandis qu'un commutateur traditionnel échange les données de point à point, Sarracenia permet le passage des données d'un bout à l'autre du réseau, tant dans une direction que dans l'autre.</p>
<p>Sarracenia, à sa plus simple expression, expose une arborescence de dossiers disponibles sur la toile (&quot;Web Accessible Folders&quot;). Le temps de latence est une composante névralgique des applications météo: les minutes, et parfois les secondes, sont comptées. Les technologies standards, telles que ATOM et RSS, sont des technologies qui consomment beaucoup de bande passante et de ressouces lorsqu'elles doivent répondre à ces contraintes. Ces standards limitent la fréquence maximale de vérification du serveur à cinq minutes. Le protocole de séquencement de messages avancés (Advanced Message Queuing Protocol, AMQP) est une approche beaucoup plus efficace pour la livraison d'annonces de nouveaux produits.</p></td>
</tr>
<tr class="odd">
<td>An initiave of Shared Services Canada <a href="http://ssc-spc.gc.ca" class="uri">http://ssc-spc.gc.ca</a> in support of internal needs of the Government of Canada</td>
<td>Une initiative de Services partagés Canada <a href="https://ssc-spc.gc.ca" class="uri">https://ssc-spc.gc.ca</a> pour appuyer les opérations du gouvernement du Canada</td>
</tr>
</tbody>
</table>

page web / homepage: <http://github.com/MetPX/sarracenia>

Concepts: [Sarracenia in 10 Minutes Video (anglais
seulement)](https://www.youtube.com/watch?v=G47DRwzwckk)

Documentation *master* location:
<https://github.com/MetPX/sarracenia/blob/master/doc/sr_subscribe.1.md#documentation>

Endroit principale pour la documentation:
<https://github.com/MetPX/sarracenia/blob/master/doc/fr/sr_subscribe.1.md#documentation>
