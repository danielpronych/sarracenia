Notes de Traduction
===================

La traduction n´est pas tellement poli en ce moment. Il y a des termes
dont le mot juste en français n´est pas tellement claire. On a commencé
avec www.deepl.com, et ajuster après avec un peu de révision, mais ce
n´est pas super réussi. Il faut un peu plus de travail.

Placement
---------

Il y a un répertoire fr/ sous doc dans le répository git. Il y a
seulement sr\_subscribe.1.md là pour l´instant. Il n´est pas linké par
d´autres pages en ce moment. On rajoutera d´autres page dans la même
place, et comme cela les lien relatifs vont marcher pareil que
l´anglais. On songera a comment arriver au francais quand ca sera plus
complète.

Méthode
-------

On prend www.deepl.com/translate comme point de départ. Il fait bien la
job, mais il ne peut pas savoir que *then sends a post* ne veut pas dire
*envoie ensuite un poteau.* En particulier il faut s'attarder aux
exemples d'execution:

> -   *sr\_subscribe foreground first.conf \# your first configuration*
>     n'équivaut pas à
> -   *sr\_subscribe premier plan premier.conf \# votre premier
>     configuration.*

Il faut laisser les exemples, incluant les messages d´erreurs en
anglais, et seulement traduire les commentaires et le text. Alors on
prend un ou deux paragraphes à la fois, et on revise. Il y a un
glossaire plus bas, la plupart des mots sont évident, mais j´aimerais
que des francophones révise les choix, parce que mon oreille carrée
n´est pas toute à faite apte pour cette tâche.

Glossaire
---------

<table>
<colgroup>
<col style="width: 21%" />
<col style="width: 28%" />
<col style="width: 23%" />
<col style="width: 26%" />
</colgroup>
<thead>
<tr class="header">
<th>Term</th>
<th>literal translations</th>
<th>Pick</th>
<th>reasoning</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>binding</td>
<td>liaison reliure?</td>
<td>association? liaison?</td>
<td>I liked Liaison...</td>
</tr>
<tr class="even">
<td>checksum</td>
<td>somme de contrôle</td>
<td></td>
<td>um, ok will french people get that?</td>
</tr>
<tr class="odd">
<td>Exchange</td>
<td>échange, bourse?</td>
<td>échange?</td>
<td>probable plain English <em>exchange</em> is better?</td>
</tr>
<tr class="even">
<td>publish post announce notifications</td>
<td>publier, annoncer poteau, afficher publication notifications</td>
<td>annoncer/publier (verbe) avis (nom)</td>
<td>It is supposed to be fast. should noun be a dépêche?</td>
</tr>
<tr class="odd">
<td>subscribe</td>
<td>abonner</td>
<td></td>
<td>good.</td>
</tr>
<tr class="even">
<td>topic</td>
<td>sujet, thème, objet</td>
<td>thème</td>
<td>Daniel used it</td>
</tr>
<tr class="odd">
<td>shim as in library</td>
<td>cale?</td>
<td>cale</td>
<td>deepl, does not seem right to me.</td>
</tr>
<tr class="even">
<td>library</td>
<td>bibliothèue - deepl librarie?</td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td>partitions blocks</td>
<td>cloisons partitions pièces blocs</td>
<td>parties</td>
<td>Peter...</td>
</tr>
</tbody>
</table>

### Publish/Post/Announced

Un des problèmes, même en anglais, est qu´on n´a pas choisi un seul mot
pour l´activité d´envoyer un message à un courtier. Il y a au moins
trois familles de mots:

Des fois, *post* qui devrait être compris dans le sense *dépêche*, mais
qui est des fois traduit comme *poteau.*

On utilise *advertised* qui devient *annoncer*, ce qui n´est pas pire.

On utilse *publish* qui devient *publier*.

des fois on vois *affiché*.

Il me semble qu´on devrait choisir un mot pour facilité la
compréhension, et il me semble que *dépêche* est le plus juste.

conseils bienvenus.
