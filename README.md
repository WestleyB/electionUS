# Elections US
Réalisation d'un tableau de bord de présentation en temps réel des résultats des élections américaines.

## Contraintes
<ul>
  <li> Les résultats sont stockés dans une des bases de données MongoDB (replica set  de composé de 3 members et 1 arbiter) hébergé sur AWS.</li>
  <li> Chargement des résultats en temps réel.</li>
  <li> Une visualisation cartographique</li>
</ul>

## Données
<ul>
1 fichier par état. Chaque ligne correspond à 1 suffrage. Lorsque l’information est disponible, les bulletins blancs figurent dans le fichier. Une ligne se compose:
      
  <li> moment du dépouillement</li>
  <li> état</li>
  <li> nom du candidat</li>
Les résultats s’échelonnent sur 1 heure entre 20 heure et 21 heure.
Les fichiers sont disponibles sur Hadoop (Terralab).
</ul>
