Voici quelques conventions de nommage et bonnes pratiques de KNACSS, cette liste est non exhaustive :

Priorité aux classes : Privilégiez au maximum l'usage de classes plutôt que des sélecteurs basés sur les noms des balises ou leur id
Nommage des classes : Choisissez des noms de composants fonctionnels réutilisables (ex. alert), des noms de sous-éléments préfixés par leur parent (ex. alert-title) et des variantes facilement distinguables (ex. alert-title--alternate)
Pas de mélange : Séparez la structure de l’apparence (une règle CSS ne doit pas comporter à la fois padding et background par exemple). Prévoyez des styles de base réutilisables, puis des classes de variantes graphiques
Autonomie des composants : Séparez le conteneur du contenu (un composant ne doit jamais être ciblé par un sélecteur qui tient compte de son parent) Par exemple, n'écrivez pas .sidebar .button mais .button-primary
Variables : les variables de KNACSS sont rédigées en minuscule, en anglais et les mots composés sont séparés d'un trait d'union. De préférence, le nom du composant apparaît en premier dans le nom d'une variable (ex. $checkbox-size plutôt que $size-checkbox), à l'exception des couleurs globales de texte ou de fond ( $color-primary, $background-base, etc.)
Couleurs : Employez systématiquement une variable pour désigner vos couleurs au sein des projets.
Points de rupture : optez pour la méthodologie "Mobile First" et appliquez de préférence des media queries de ce type : @media (min-width: $breakpoint). Si vous deviez choisir un intervalle maximum, optez pour @media (max-width: ($breakpoint - 1)) pour éviter les chevauchements
Classes utilitaires : KNACSS propose quelques classes utilitaires telles que .mt0, .txtcenter, .fl, etc. mais il est préférable de ne pas en abuser. Évitez d'accumuler les classes sur un même élément
Réutilisez : Utilisez au maximum les modèles et composants réutilisables tels que les objet "media" et "autogrid." (voir fichiers dans /sass/components/)
couleurs
Ci-dessous, la palette de couleurs employée de base sur KNACSS, ainsi que les noms de variables Scss associées.

color names
#fff
$white
#f8f9fa
$gray-100
#e7e9ed
$gray-200
#dee2e6
$gray-300
#ced4da
$gray-400
#acb3c2
$gray-500
#727e96
$gray-600
#454d5d
$gray-700
#333
$gray-800
#212529
$gray-900
#000
$black
#5BC0DE
$blue-300
#0275D8
$blue-500
#5CB85C
$green-500
#F0AD4E
$orange-500
#D9534F
$red-500
semantic colors
$green-500
$color-brand
$blue-500
$color-primary
$green-500
$color-success
$blue-300
$color-info
$orange-500
$color-warning
$red-500
$color-danger
$gray-800
$color-inverse
transparent
$color-ghost
$gray-200
$color-muted
$gray-900
$color-base
$white
$background-base
$gray-800
$link-color
darken($link-color, 15%)
$link-color-hover
$gray-800
$forms-color
fontes
Trois variables sont prévues pour les familles de police. La première, $font-stack-common, est appliquée par défaut sur le contenu. Il s'agit de ce que l'on appelle la System Font Stack, déjà adoptée par des sites tels que Medium, Booking, WordPress, Alsacréations, etc.

Les voici en oeuvre :

Ici un texte de contenu en $font-stack-common. Lorem Elsass Ipsum mitt picon bière munster du ftomi! Ponchour bisame. Bibbeleskaas jetz here's some code rossbolla sech choucroute un schwanz geburtstàg

$font-stack-common: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;
Ici un texte de contenu en $font-stack-headings. Lorem Elsass Ipsum mitt picon bière munster du ftomi! Ponchour bisame. Bibbeleskaas jetz here's some code rossbolla sech choucroute un schwanz geburtstàg

$font-stack-headings: sans-serif;
Ici un texte de contenu en $font-stack-monospace. Lorem Elsass Ipsum mitt picon bière munster du ftomi! Ponchour bisame. Bibbeleskaas jetz here's some code rossbolla sech choucroute un schwanz geburtstàg

$font-stack-monospace: consolas, courier, monospace;
titres
Les six niveaux de titre sont stylés avec leurs éléments respectifs : h1 à h6, ou (recommandé) les classes .h1-like à .h6-like.

titre niveau 1
titre niveau 2
titre niveau 3
titre niveau 4
titre niveau 5
titre niveau 6
paragraphe stylé comme un titre 1

<h1>titre niveau 1</h1>
<h2>titre niveau 2</h2>
<h3>titre niveau 3</h3>
<h4>titre niveau 4</h4>
<h5>titre niveau 5</h5>
<h6>titre niveau 6</h6>
<p class="h1-like">paragraphe stylé comme un titre 1</p>
paragraphes et textes
Lorem Elsass Ipsum mitt picon bière munster du ftomi! Je suis un lien Ponchour bisame. Bibbeleskaas je suis marqué jetz rossbolla sech je suis un <em> choucroute un schwanz geburtstàg, Je suis une touche du clavier Chinette dû, ìch bier deppfele schiesser. Flammekueche de knèkes Seppele gal! a hopla geburtstàg, je suis un <strong> alles fraü Chulia Roberts je suis du code oder knäckes dûû blottkopf.

<p>Lorem Elsass Ipsum mitt picon bière munster du ftomi! <a href="#">Je suis un lien</a> Ponchour bisame. Bibbeleskaas <mark>je suis marqué</mark> jetz rossbolla sech <em>je suis un <em></em> choucroute un schwanz geburtstàg, Je suis une touche <kbd>du clavier</kbd> Chinette dû, ìch bier deppfele schiesser. Flammekueche de knèkes Seppele gal! a hopla geburtstàg, <strong>je suis un <strong></strong> alles fraü Chulia Roberts <code>je suis du code</code> oder knäckes dûû blottkopf.</p>
listes
Liste non ordonnée
Salade
Tomate
Oignon
Choucroute
Liste ordonnée
Salade
Tomate
Oignon
Choucroute
Liste .unstyled ou .is-unstyled
Salade
Tomate
Oignon
Choucroute
<ul>
    <li>Liste non ordonnée</li>
    <li>Salade</li>
    <li>Tomate</li>
    <li>Oignon</li>
    <li>Choucroute</li>
</ul>

<ol>
    <li>Liste ordonnée</li>
    <li>Salade</li>
    <li>Tomate</li>
    <li>Oignon</li>
    <li>Choucroute</li>
</ol>

<ul class="unstyled">
    <li>Liste <code>.unstyled</code></li>
    <li>Salade</li>
    <li>Tomate</li>
    <li>Oignon</li>
    <li>Choucroute</li>
</ul>
tableaux
Les tableaux de données disposent de styles de base. Ceux munis d'une classe .table bénéficient en sus de propriétés graphiques définies selon des variables de projet dédiées : couleur de fond, des titres, etc. La classe additionnelle .table--zebra colorie une rangée sur deux.

.table
Fruit	Note	Prix
Kiwi	★★★	13.37€
Banane	★★	0.42€
Voici la structure HTML permettant d'obtenir ce résultat :

<table class="table" summary="">
	<caption>.table</caption>
	<thead>
		<tr>
			<th scope="col">Fruit</th>
			<th scope="col">Note</th>
			<th scope="col">Prix</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Kiwi</td>
			<td>★★★</td>
			<td>13.37€</td>
		</tr>
    <tr>
			<td>Banane</td>
			<td>★★</td>
			<td>0.42€</td>
		</tr>
	</tbody>
</table>
citations
Lorem Elsass Ipsum mitt picon bière munster du ftomi! Ponchour bisame. Bibbeleskaas jetz here's some code rossbolla sech choucroute un schwanz geburtstàg

<blockquote>
   <p>Lorem Elsass Ipsum mitt picon bière munster du ftomi! Ponchour bisame. Bibbeleskaas jetz here's some code rossbolla sech choucroute un schwanz geburtstàg</p>
</blockquote>
alertes
Une alerte est une boîte d'information disposant de la classe .alert (pour les styles par défaut) ou une classe commençant par .alert-- pour les différentes variantes .alert--primary, .alert--success, .alert--warning, .alert--danger, .alert--info, .alert--inverse, .alert--ghost.

Les variantes sont gérées par un ensemble (thème) de variables comprenant : couleur de fond, couleur de texte et bordure optionnelle.

Alert Default
Primary
Success
Warning
Danger
Info
Inverse
Ghost
<div class="alert">Alert Default</div>
<div class="alert--primary">Primary</div>
<div class="alert--success">Success</div>
<div class="alert--warning">Warning</div>
<div class="alert--danger">Danger</div>
<div class="alert--info">Info</div>
<div class="alert--inverse">Inverse</div>
<div class="alert--ghost">Ghost</div>
inputs
text
 
search
 
number
 
email
 
••••••••
 
<input type="text" placeholder="text">
<input type="search" placeholder="search">
<input type="number" placeholder="number">
<input type="email" placeholder="email">
<input type="password" value="password">
<progress></progress>
checkboxes
KNACSS prend en compte les styles de base des cases à cocher, il suffit d'appliquer la classe .checkbox sur l'élément input afin de le voir en action.

Voici le code HTML recommandé : <input type="checkbox" class="checkbox" id="c1"><label for="c1">click here</label>

 Salade
 Tomate
 Oignon
<form action="#">
  <ul class="is-unstyled">
    <li>
      <input type="checkbox" class="checkbox" id="c1">
      <label for="c1">Salade</label>
    </li>
    <li>
      <input type="checkbox" class="checkbox" id="c2" checked="checked">
      <label for="c2">Tomate</label>
    </li>
    <li>
      <input type="checkbox" class="checkbox" id="c3" checked="checked" disabled="disabled">
      <label for="c3">Oignon</label>
    </li>
    <li>
      <input type="checkbox" class="checkbox" id="c4" disabled="disabled">
      <label for="c4">Choucroute</label>
    </li>
  </ul>
</form>
radios
KNACSS prend en compte les styles de base des boutons radio, il suffit d'appliquer la classe .radio sur l'élément input afin de le voir en action.

Voici le code HTML recommandé : <input type="radio" class="radio" name="radio" id="r1"><label for="r1">Click here</label>

 Salade
 Tomate
 Oignon
<form action="#">
  <ul class="is-unstyled">
    <li>
      <input type="radio" class="radio" name="radio" id="r1">
      <label for="r1">Salade</label>
    </li>
    <li>
      <input type="radio" class="radio" name="radio" id="r2" checked="checked">
      <label for="r2">Tomate</label>
    </li>
    <li>
      <input type="radio" class="radio" name="radio" id="r3" checked="checked" disabled="disabled">
      <label for="r3">Oignon</label>
    </li>
    <li>
      <input type="radio" class="radio" name="radio" id="r4" disabled="disabled">
      <label for="r4">Choucroute</label>
    </li>
  </ul>
</form>
switchs
Les boutons de switch (ou toggle) sont gérés à l'aide de la classe .switch sur l'élément input checkbox.

Voici le code HTML recommandé : <input type="checkbox" class="switch" id="switch">
<label for="switch" class="label">slide to unlock</label>

 slide to unlock
<input type="checkbox" class="switch" id="switch">
<label for="switch" class="label">slide to unlock</label>
selects
Les éléments <select> sont automatiquement stylés dans KNACSS. Vous pouvez adapter les styles de base en modifiant les variables du projet.


Salade
<select>
  <option value="valeur1">Salade</option>
  <option value="valeur2">Tomate</option>
  <option value="valeur3">Oignon</option>
</select>
flèches / arrows
Quatre classes sont prévues pour afficher des flèches décoratives à droite de n'importe quel élément. Il s'agit de icon-arrow--down, icon-arrow--up, icon-arrow--right et icon-arrow--left. Si vous souhaitez que la flèche apparaisse à gauche, appliquez la classe .flex-row-reverse sur le parent.

Attention, les flèches "arrows" se basent sur les masques CSS, actuellement incompatibles avec IE / Edge.

arrow down 

arrow up 

arrow right 

arrow left 

arrow left
<p>icon-arrow down <i class="icon-arrow--down"></i></p>
<p>icon-arrow up <i class="icon-arrow--up"></i></p>
<p>icon-arrow right <i class="icon-arrow--right"></i></p>
<p>icon-arrow left <i class="icon-arrow--left"></i></p>
<p class="flex-row-reverse">icon-arrow left <i class="icon-arrow--left"></i></p>
boutons
Les boutons, comme les alertes disposent d'un ensemble de thème de couleurs (couleur de fond, couleur de texte et bordure optionnelle).

Il est recommandé d'utiliser l'élément HTML <button>, mais rien n'empêche d'opter pour d'autres types d'éléments, tant qu'ils sont associés à l'attribut ARIA role="button"

Un bouton dispose de la classe .btn ou .button (pour les styles par défaut) ou une classe commençant par .btn-- ou .button-- pour les différentes variantes, par exemple .btn--primary, .btn--success, .btn--warning, .btn--danger, .btn--info, .btn--inverse, .btn--ghost.

      
<button class="btn">Button Default</button>
<button class="btn--primary">Primary</button>
<button class="btn--success">Success</button>
<input  class="btn--warning" type="button" role="button" value="Warning">
<span class="btn--danger" role="button">Danger</span>
<span class="btn--info" role="button">Info</span>
<span class="btn--inverse" role="button">Inverse</span>
<button class="btn--ghost">Ghost</button>
burger button
Un élément possédant la classe .nav-button et contenant un élément vide devient un bouton de navigation stylé et prêt à l'action (avec un peu de renfort de JavaScript ou CSS pour déclencher l'événement bien sûr).

Pour des raisons d'accessibilité, il est fortement recommandé d'utiliser la structure HTML ci-dessous pour votre bouton.

<button class="nav-button" type="button" role="button" aria-label="open/close navigation"><i></i></button>
Voici le bout de code JavaScript employé pour activer ce bouton 

<script>
/**!
Navigation Button Toggle class
*/
(function() {

// old browser or not ?
if ( !('querySelector' in document && 'addEventListener' in window) ) {
return;
}
window.document.documentElement.className += ' js-enabled';

function toggleNav() {

// Define targets by their class or id
var button = document.querySelector('.nav-button');
var target = document.querySelector('body > nav');

// click-touch event
if ( button ) {
  button.addEventListener('click',
  function (e) {
      button.classList.toggle('is-active');
    target.classList.toggle('is-opened');
    e.preventDefault();
  }, false );
}
} // end toggleNav()

toggleNav();
}());
</script>
tags (étiquette)
Un tag dispose de la classe .tag (pour les styles par défaut) ou une classe commençant par .tag-- pour les différentes variantes, par exemple .tag--primary, .tag--success, .tag--warning, .tag--danger, .tag--info, .tag--inverse, .tag--ghost.

   Warning Danger Info Inverse
<button class="tag">Badge Default</button>
<button class="tag--primary">Primary</button>
<button class="tag--success">Success</button>
<span class="tag--warning">Warning</span>
<span class="tag--danger">Danger</span>
<span class="tag--info">Info</span>
<span class="tag--inverse">Inverse</span>
badges (arrondis)
Un badge est systématiquement rond et s'adapte à son contenu. Il dispose de la classe .badge (pour les styles par défaut) ou une classe commençant par .badge-- pour les différentes variantes, par exemple .badge--primary, .badge--success, .badge--warning, .badge--danger, .badge--info, .badge--inverse, .badge--ghost.

   Warning Danger Info Inverse 
<button class="badge">Badge Default</button>
<button class="badge--primary">Primary</button>
<button class="badge--success">Success</button>
<span class="badge--warning">Warning</span>
<span class="badge--danger">Danger</span>
<span class="badge--info">Info</span>
<span class="badge--inverse">Inverse</span>
tabs / onglets
KNACSS prévoit des styles pour une navigation à base d'onglets accessibles (fonctionnels aux flèches du clavier et à la souris). Le principe général est de placer la classe .js-tabs sur le conteneur global.
Les instructions complètes, le code HTML et JavaScript se trouvent sur le projet d'Alsacréations Pepin .

Attention : pour fonctionner, les onglets nécessitent un code JavaScript (à récupérer sur Pepin).

Salade Tomate Oignons
Contenu 1.
Lorem Elsass Ipsum mitt picon bière munster du ftomi! Ponchour bisame. Bibbeleskaas jetz rossbolla sech choucroute un schwanz geburtstàg, Chinette dû, ìch bier deppfele schiesser.


<div class="tabs js-tabs">
  <nav class="tabs-menu">
    <a href="#tab1" class="tabs-menu-link is-active">Salade</a>
    <a href="#tab2" class="tabs-menu-link">Tomate</a>
    <a href="#tab3" class="tabs-menu-link">Oignons</a>
  </nav>

  <div class="tabs-content">
    <div id="tab1" class="tabs-content-item">Contenu 1. <br>Lorem Elsass Ipsum mitt picon bière munster du ftomi! Ponchour bisame. Bibbeleskaas jetz rossbolla sech choucroute un schwanz geburtstàg, Chinette dû, ìch bier deppfele schiesser.</div>
    <div id="tab2" class="tabs-content-item">Contenu 2. <br>Flammekueche de knèkes Seppele gal! a hopla geburtstàg, alles fraü Chulia Roberts oder knäckes dûû blottkopf. Noch bredele schissabibala, yeuh e schmutz.</div>
    <div id="tab3" class="tabs-content-item">Contenu 3. <br>E gewurtztraminer doch Carola schneck, schmutz a riesling de chambon eme rucksack Roger dû hopla geiss, jetz Chorchette de Scharrarbergheim.</div>
  </div>
</div>
alignements
span link
<div class="txtleft">
    <span>span</span>
    <a href="#">link</a>
</div>
span link
<div class="txtcenter">
    <span>span</span>
    <a href="#">link</a>
</div>
span link
<div class="txtright">
    <span>span</span>
    <a href="#">link</a>
</div>
div.left
<div style="width: 30%" class="left">div.left</div>
div.center
<div style="width: 30%" class="center">div.center</div>
div.right
<div style="width: 30%" class="right">div.right</div>
flottants
div.fldiv.fr
<div class="clearfix">
        <div style="width: 20%" class="fl">div.fl</div>
        <div style="width: 20%" class="fr">div.fr</div>
    </div>
flexbox
div
span
…
<section class="flex-container">
  <div>div</div>
  <span>span</span>
  <em>…</em>
</section>
div
span
…
<div class="flex-container--column">
<div>div</div>
<span>span</span>
<em>…</em>
</div>
.w33
.w150p
.item-fluid
<div class="flex-container">
  <div class="w33">.w33</div>
  <span class="w150p">.w150p</span>
  <span class="item-fluid">.item-fluid</span>
</div>
item
item
.item-first
<div class="flex-container">
  <div>item</div>
  <span>item</span>
  <span class="item-first">.item-first</span>
</div>
.item-last
item
item
<div class="flex-container">
  <div class="item-last">.item-last</div>
  <span>item</span>
  <span>item</span>
</div>
.item-center
<div class="flex-container" style="height: 200px;">
  <span class="item-center">.item-center</span>
</div>
Grillade
Grillade, le système de grille principal de KNACSS a été entièrement repensé pour les navigateurs modernes. Il est dorénavant bâti sur Grid Layout et non plus Flexbox. Grid Layout n'est pleinement compatible qu'à partir de Edge 16, même si Autoprefixer est activé et devrait rendre la grille compatible sur IE10.

Par défaut, le nouveau système de grilles est automatiquement importé au sein de KNACSS, cependant les deux versions (nouvelle et ancienne en Flexbox) co-existent toujours pour des raisons de compatibilité :

grillade-grid.scss (nouvelle version en Grid Layout)
grillade-flex.scss (ancienne version en Flexbox)
Ainsi, il est possible, en Sass, de remplacer le fichier importé "grillade-grid.scss" par l'ancienne version "grillade-flex.scss" pour assurer un support jusqu'à IE10 minimum. Les fichiers CSS compilés peuvent également être utilisés de manière autonome :

grillade-grid.css (3ko)
grillade-flex.css (11ko)
Grillade n'est pas un "framework", il s'agit simplement de fonctionnalités basiques pour réaliser des grilles simples et courantes (et responsive).

Si vous avez besoin de grilles complexes :

Utilisez la spécification CSS Grid Layout (c'est fait pour ça)
Utilisez la grille de Bootstrap (bonne chance)
Les grilles ne s'activent qu'à partir d'un breakpoint minimum ( $tiny = 480px par défaut). En deça, les éléments s'affichent en blocs, les uns sous les autres.

comparaison entre Grillade v6 et Grillade v7
Grillade v6	Grillade v7
Techno CSS employée	Flexbox	Grid Layout
Poids fichier CSS	11 Ko	3 Ko
Compatibilité	IE10+	Edge 16+ sûr
IE10 à tester
Fonctionnalités	Mobile first
Largeurs fluides
Gouttières
Fusion de colonnes
Fusion de rangées
Gestion des écrans intermédiaires
Tailles d'enfants responsive
Ordonnancement des enfants	Mobile first
Largeurs fluides
Gouttières
Fusion de colonnes
Fusion de rangées
Gestion des écrans intermédiaires
Tailles d'enfants responsive
Ordonnancement des enfants
Voici quelques exemples de grilles réalisées avec KNACSS v7…

.autogrid (ou .grid)
Une "autogrid" (classe .autogrid ou .grid) est une micro-grille où les enfants demeurent toujours sur une seule ligne et se répartissent de façon équitable quel que soit leur nombre. Il est possible d'appliquer une gouttière avec les classes .has-gutter, .has-gutter-l, .has-gutter-xl.

1
2
3
4
5
<section class="autogrid">
    <div>1</div>
    <div>2</div>
    <div>3</div>
    <div>4</div>
    <div>5</div>
</section>
.grid-6
Une grille de 6 colonnes, avec retour à la ligne possible, et sans gouttière

1
2
3
4
5
6
7
8
<section class="grid-6">
    <div>1</div>
    <div>2</div>
    <div>3</div>
    <div>4</div>
    <div>5</div>
    <div>6</div>
    <div>7</div>
    <div>8</div>
</section>
.grid-6 .has-gutter
Une grille de 6 colonnes avec une gouttière. Les classes prévues sont .has-gutter, .has-gutter-l, .has-gutter-xl

1
2
3
4
5
6
7
8
<section class="grid-6 has-gutter">
    <div>1</div>
    <div>2</div>
    <div>3</div>
    <div>4</div>
    <div>5</div>
    <div>6</div>
    <div>7</div>
    <div>8</div>
</section>
.grid-4 .has-gutter
Une grille de 4 colonnes avec une gouttière. Certains enfants s'étendent sur plusieurs colonnes ou rangées.

1
.col-2
.row-2
4
5
6
<section class="grid-4 has-gutter">
    <div>1</div>
    <div class="col-2">.col-2</div>
    <div class="row-2">.row-2</div>
    <div>4</div>
    <div>5</div>
    <div>6</div>
</section>
.grid-6-small-3
Une grille de 6 colonnes sur grand écran, et 3 colonnes sur écran moyen.

1
2
3
4
5
6
7
8
<section class="grid-6-small-3">
<div>1</div>
<div>2</div>
<div>3</div>
<div>4</div>
<div>5</div>
<div>6</div>
<div>7</div>
<div>8</div>
</section>
.grid-7-small-4
Une grille de 7 colonnes sur grand écran, et 4 colonnes sur écran moyen. Quelques enfants changent de taille sur écran moyen

1
2
.col-2-small-1
4
5
.col-1-small-2
7
.col-2-small-all
<section class="grid-7-small-4">
    <div>1</div>
    <div>2</div>
    <div class="col-2-small-1">.col-2-small-1</div>
    <div>4</div>
    <div>5</div>
    <div class="col-1-small-2">.col-1-small-2</div>
    <div>7</div>
    <div class="col-2-small-all">.col-2-small-all</div>
</section>
.grid-6-small-3 .has-gutter
Panachage des possibilités de grilles

1
2
(3) item-first
4
5
6
7
col-3-small-2
col-2-small-1
col-2-small-1
col-4-small-2
row-2
13
14
15
16
col-3
18
19
col-all
<section class="grid-6-small-3 has-gutter">
  <div>1</div>
  <div>2</div>
  <div class="item-first">(3) item-first</div>
  <div>4</div>
  <div>5</div>
  <div>6</div>
  <div>7</div>
  <div class="col-3-small-2">col-3-small-2</div>
  <div class="col-2-small-1">col-2-small-1</div>
  <div class="col-2-small-1">col-2-small-1</div>
  <div class="col-4-small-2">col-4-small-2</div>
  <div class="row-2">row-2</div>
  <div>13</div>
  <div>14</div>
  <div>15</div>
  <div>16</div>
  <div class="col-3">col-3</div>
  <div>18</div>
  <div>19</div>
  <div class="col-all">col-all</div>
</section>
