# PluginChoucas

Ce plug-in a �t� d�velopp� pour le logiciel QGis, au cours d'un stage de d�veloppement informatique � l'ENSG (http://ensg.eu). Il s'int�gre plus globalement dans le cadre d�un projet ANR, en collaboration  avec le Peloton de Gendarmerie de Haute-Montagne (PGHM) de Grenoble, l�universit� de Pau, et l�universit� de Grenoble, dont le but est l'aide � la localisation de victimes en montagne. 

Le but de ce plug-in est de faciliter l'acc�s et la visualisation de donn�es de type point (refuges, plans d�eau...) et de type ligne (itin�raires de randonn�e), provenant essentiellement de sites collaboratifs (camptocamp.org, refugesinfo...). Il s�agit d�exploiter les fichiers JSON retourn�s par leur API respective pour afficher les donn�es sous QGis. 

Un mode Hors-Ligne est aussi disponible, mais n�cessite une base de donn�es.


Gestion du catalogue
-----
Les catalogues de donn�es du plug-in permettent de r�f�rencer toutes les m�tadonn�es. Il en existe deux : 

- un premier, utilis� lorsque le mode <b>� en ligne �</b> est activ� et qui r�f�rence les m�tadonn�es relatives aux API, c�est-�-dire les attributs, la projection, la zone � visualiser (par bbox sur refuges.info et par zone administrative pour camptocamp) ainsi que le type de donn�es (point, ligne, surface�).
-  un second catalogue pour le mode <b>� hors ligne � </b>ou est list� dans le fichier XML l�emplacement dans la base de donn�es des diff�rentes donn�es. Le format XML permet d'y ajouter des informations sans pour autant devoir modifier notre code python. Nous d�crirons dans cette partie comment proc�der pour ajouter une source de donn�es au catalogue.

#### Le catalogue en ligne

Dans cette partie est pr�sent� de mani�re synth�tique ce que comporte le catalogue � en ligne �.

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

Les balises <b>&lt;source&gt;</b> r�f�rencent les diff�rentes sources de donn�es que l�on peut afficher dans le plug-in QGis, par exemple � refuges.info � ou � camptocamp �. Sous la balise � source � on retrouve d�autres balises indiquant les param�tres g�n�raux � utiliser pour une m�me source (projection, type de bbox�).

Le type de bbox d�pend de la source d�o� provient les donn�es, en effet les requ�tes sur les diff�rentes API ne se construisent pas toutes de la m�me fa�on. Par exemple, pour l�API refuges.info la bbox s�obtient avec quatre coordonn�es, le site http://boundingbox.klokantech.com permet de d�terminer les coordonn�es de la bbox en fonction de la r�gion ou du d�partement choisi. Pour l�API camptocamp, le fonctionnement n�est pas identique car l�emprise sur laquelle on veut afficher les donn�es est sous forme de code administratif dans la requ�te URL. Par exemple le code administratif pour le d�partement de l�Is�re est 14328. Comme pour la bbox de refuges.info, on a cr�� dans le code une liste de d�partement avec le code administratif correspondant.

Ensuite, chaque balise <b>&lt;type&gt;</b> r�f�rence un type de donn�es disponible sur l�API source et que l�on peut visualiser dans le plug-in CHOUCAS. Comme on le voit sur la capture ci-dessus, la source refuges.info permet de visualiser cinq types de donn�es : refuges, points d�eau, sommets, points de passage et lacs. Et pour chaque type de donn�es on a les informations d�pendant de cette donn�e. La principale est l�URL qui fait l�appel vers l�API, le type de g�om�trie (point, string�) mais encore le nom de l�imagette au format svg � charger pour afficher cette donn�e sous QGis afin de la rep�rer plus facilement, sa taille etc�

#### Ajout d�une nouvelle source de donn�es :
L�ajout d�une nouvelle source de donn�es � visualiser lors du mode � en ligne � de notre plug-in est envisageable. Cependant notre code et notre catalogue ne sont pas assez g�n�raux pour g�rer cet ajout de mani�re totalement autonome. En effet, dans le catalogue du mode � en ligne � les attributs ne sont pas les m�mes d�une source � l�autre. Ce qui implique dans le code python du plug-in de g�rer chaque source de donn�es en fonction de ses propres attributs. 

La solution envisageable que nous n�avons pas eu le temps d�impl�menter serait de d�finir qu�une seule balise � attribut � dans le catalogue pour chaque source de donn�es et de placer � l�int�rieur de cette m�me et unique balise l�ensemble des attributs n�cessaire � la visualisation des donn�es.

Toutefois, dans l��tat actuel du code python, l�ajout d�une nouvelle source de donn�es au catalogue est possible. Il faut suivre le sch�ma des sources de donn�es d�j� compl�t�es dans le catalogue, en indiquant le nom de chacun des attributs sp�cifique � la source ainsi qu�au diff�rents types de donn�es (type : points ou lignes etc�).


![Description des blocs du catalogue](https://github.com/ANRChoucas/PluginChoucas/tree/master/doc/Catalogue.png)


Installation
----

Ce guide d�installation pour syst�me d�exploitation Windows liste les diff�rentes �tapes � suivre pour l�installation de notre plug-in. Avant toute op�ration v�rifiez que le logiciel QGis ne soit pas d�j� lanc�.

1) T�l�charger le plug-in � l�adresse Github suivante : https://github.com/ANRChoucas/PluginChoucas/archive/master.zip
2) D�-zipper le fichier et le renommer afin d�obtenir le dossier � PluginChoucas �
3) Copier le dossier et coller au chemin suivant :
     C:&#92;Users&#92;username&#92;.qgis2&#92;python&#92;plugins
4) Lancer Qgis, dans l�onglet � Extension � / � �Installer/G�rer les extensions �. La fen�tre ci-dessous s�ouvre.

![Afficher les extensions exp�rimentales](https://github.com/ANRChoucas/PluginChoucas/tree/master/doc/Install_01.png)

Dans le dernier onglet � Param�tres � s�assurer que la case � Afficher les extensions exp�rimentales � soit bien coch�e

5) Toujours sur cette m�me fen�tre, aller sous l�onglet � Toutes �. Taper dans la barre derecherche � choucas � et s�lectionner l�extension comme sur la capture suivante.

![S�lection du plug-in Choucas](https://github.com/ANRChoucas/PluginChoucas/tree/master/doc/Install_02.png)

6) Fermer la fen�tre � Extensions �, sur le Desktop de QGis un nouveau symbole apparait. Cliquer dessus pour utiliser le plug-in CHOUCAS.


Sources des donn�es :
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
