# PluginChoucas

Ce plug-in a été développé pour le logiciel QGis, au cours d'un stage de développement informatique à l'ENSG (http://ensg.eu). Il s'intègre plus globalement dans le cadre d’un projet ANR, en collaboration  avec le Peloton de Gendarmerie de Haute-Montagne (PGHM) de Grenoble, l’université de Pau, et l’université de Grenoble, dont le but est l'aide à la localisation de victimes en montagne. 

Le but de ce plug-in est de faciliter l'accès et la visualisation de données de type point (refuges, plans d’eau...) et de type ligne (itinéraires de randonnée), provenant essentiellement de sites collaboratifs (camptocamp.org, refugesinfo...). Il s’agit d’exploiter les fichiers JSON retournés par leur API respective pour afficher les données sous QGis. 

Un mode Hors-Ligne est aussi disponible, mais nécessite une base de données.


Gestion du catalogue
-----
Les catalogues de données du plug-in permettent de référencer toutes les métadonnées. Il en existe deux : 

- un premier, utilisé lorsque le mode <b>« en ligne »</b> est activé et qui référence les métadonnées relatives aux API, c’est-à-dire les attributs, la projection, la zone à visualiser (par bbox sur refuges.info et par zone administrative pour camptocamp) ainsi que le type de données (point, ligne, surface…).
-  un second catalogue pour le mode <b>« hors ligne » </b>ou est listé dans le fichier XML l’emplacement dans la base de données des différentes données. Le format XML permet d'y ajouter des informations sans pour autant devoir modifier notre code python. Nous décrirons dans cette partie comment procéder pour ajouter une source de données au catalogue.

#### Le catalogue en ligne

Dans cette partie est présenté de manière synthétique ce que comporte le catalogue « en ligne ».

```XML
<?xml version="1.0" encoding='UTF-8'?>
<data> 
    <source name="refuges.info">    
        <bbox>0</bbox>   
        <couleur>blue</couleur>    
        <projection>epsg:4326</projection>    
        <type data-id="refuges">      
	        <id>id</id>      
	        <nom>nom</nom>      
	        <lat>lat</lat>      
	        <long>long</long>      
	        <alt>alt</alt>      
	        <geom>Point</geom>      
	        <forme>square</forme>      
	        <svg>home_full</svg>      
	        <size>3</size>      
	        <url>https://www.refuges.info/api/bbox?type_points=refuge</url>    
        </type>    
        <type data-id="points d eau">      
	        <id>id</id>      
	        <nom>nom</nom>      
	        <lat>lat</lat>      
	        <long>long</long>      
	        <alt>alt</alt>      
	        <geom>Point</geom>      
	        <forme>circle</forme>      
	        <svg>circular_shape</svg>      
	        <size>2</size>      
	        <url>https://www.refuges.info/api/bbox?type_points=pt_eau</url>    
	   </type>
	   <!-- ... -->
	</source>  
	<source name="camptocamp">    
		<bbox>1</bbox>    
		<couleur>orange</couleur>
		<projection>epsg:3857</projection>
		<type data-id="refuges">
			<id>id</id>      
			<nom>nom</nom>      
			<lat>lat</lat>      
			<long>long</long>      
			<alt>alt</alt>  
			<geom>Point</geom>   
			<forme>square</forme>  
			<svg>home_full</svg>   
			<size>3</size>   
			<param>hut</param>
			<type_elem>waypoints</type_elem>
			<url>https://api.camptocamp.org/waypoints?wtyp=gite,hut,shelter</url>    	
		</type>
    </source>
</data>
```

Les balises <b>&lt;source&gt;</b> référencent les différentes sources de données que l’on peut afficher dans le plug-in QGis, par exemple « refuges.info » ou « camptocamp ». Sous la balise « source » on retrouve d’autres balises indiquant les paramètres généraux à utiliser pour une même source (projection, type de bbox…).

Le type de bbox dépend de la source d’où provient les données, en effet les requêtes sur les différentes API ne se construisent pas toutes de la même façon. Par exemple, pour l’API refuges.info la bbox s’obtient avec quatre coordonnées, le site http://boundingbox.klokantech.com permet de déterminer les coordonnées de la bbox en fonction de la région ou du département choisi. Pour l’API camptocamp, le fonctionnement n’est pas identique car l’emprise sur laquelle on veut afficher les données est sous forme de code administratif dans la requête URL. Par exemple le code administratif pour le département de l’Isère est 14328. Comme pour la bbox de refuges.info, on a créé dans le code une liste de département avec le code administratif correspondant.

Ensuite, chaque balise <b>&lt;type&gt;</b> référence un type de données disponible sur l’API source et que l’on peut visualiser dans le plug-in CHOUCAS. Comme on le voit sur la capture ci-dessus, la source refuges.info permet de visualiser cinq types de données : refuges, points d’eau, sommets, points de passage et lacs. Et pour chaque type de données on a les informations dépendant de cette donnée. La principale est l’URL qui fait l’appel vers l’API, le type de géométrie (point, string…) mais encore le nom de l’imagette au format svg à charger pour afficher cette donnée sous QGis afin de la repérer plus facilement, sa taille etc…

#### Ajout d’une nouvelle source de données :
L’ajout d’une nouvelle source de données à visualiser lors du mode « en ligne » de notre plug-in est envisageable. Cependant notre code et notre catalogue ne sont pas assez généraux pour gérer cet ajout de manière totalement autonome. En effet, dans le catalogue du mode « en ligne » les attributs ne sont pas les mêmes d’une source à l’autre. Ce qui implique dans le code python du plug-in de gérer chaque source de données en fonction de ses propres attributs. 

La solution envisageable que nous n’avons pas eu le temps d’implémenter serait de définir qu’une seule balise « attribut » dans le catalogue pour chaque source de données et de placer à l’intérieur de cette même et unique balise l’ensemble des attributs nécessaire à la visualisation des données.

Toutefois, dans l’état actuel du code python, l’ajout d’une nouvelle source de données au catalogue est possible. Il faut suivre le schéma des sources de données déjà complétées dans le catalogue, en indiquant le nom de chacun des attributs spécifique à la source ainsi qu’au différents types de données (type : points ou lignes etc…).


![Description des blocs du catalogue](https://github.com/ANRChoucas/PluginChoucas/tree/master/doc/Catalogue.png)


Installation
----

Ce guide d’installation pour système d’exploitation Windows liste les différentes étapes à suivre pour l’installation de notre plug-in. Avant toute opération vérifiez que le logiciel QGis ne soit pas déjà lancé.

1) Télécharger le plug-in à l’adresse Github suivante : https://github.com/ANRChoucas/PluginChoucas/archive/master.zip
2) Dé-zipper le fichier et le renommer afin d’obtenir le dossier « PluginChoucas »
3) Copier le dossier et coller au chemin suivant :
     C:&#92;Users&#92;username&#92;.qgis2&#92;python&#92;plugins
4) Lancer Qgis, dans l’onglet « Extension » / « «Installer/Gérer les extensions ». La fenêtre ci-dessous s’ouvre.

![Afficher les extensions expérimentales](https://github.com/ANRChoucas/PluginChoucas/tree/master/doc/Install_01.png)

Dans le dernier onglet « Paramètres » s’assurer que la case « Afficher les extensions expérimentales » soit bien cochée

5) Toujours sur cette même fenêtre, aller sous l’onglet « Toutes ». Taper dans la barre derecherche « choucas » et sélectionner l’extension comme sur la capture suivante.

![Sélection du plug-in Choucas](https://github.com/ANRChoucas/PluginChoucas/tree/master/doc/Install_02.png)

6) Fermer la fenêtre « Extensions », sur le Desktop de QGis un nouveau symbole apparait. Cliquer dessus pour utiliser le plug-in CHOUCAS.


Sources des données :
-------
* l'API CampToCamp : https://www.camptocamp.org/articles/838875/en/api-c2c-v6
* L'API Refuges.info : https://www.refuges.info/api/doc/
* Les API Geotrek (http://geotrek.fr/) :
	* http://rando.vanoise.com/
	* http://rando.parc-du-vercors.fr/
	* http://rando.ecrins-parcnational.fr/fr/


Auteurs
--------- 
* Eva Chen-Yen-Su 
* Sylvain Jourdan
* Coline Hallier

	
	
> Written with [StackEdit](https://stackedit.io/).
