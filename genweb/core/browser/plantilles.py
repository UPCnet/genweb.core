# -*- coding: utf-8 -*-


def get_plantilles():
    """
    Declaració de les pàgines que es faràn servir com plantilles
    """
    plantilles = []
    titol = u"Índex de contingut"
    resum = u"Per definir un índex amb enllaços al contingut de la mateixa pàgina. Enllaços definits amb àncores."
    cos = u"""<div class="llistatIndex">
<h2>Títol de l'índex [opcional]</h2>
<ul>
<li><a href="#">JDuis tellus</a></li>
<li><a href="#">Maecenas elit orci</a></li>
<li><a href="#">At ipsum vitae est lacinia tincidunt</a></li>
<li><a href="#">Eget suscipit eros purus in ante</a></li>
<li><a href="#">Sed ultricies cursus lectus</a></li>
<li><a href="#">FusceLli tincidunt</a></li>
</ul>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})    

    titol = u"Text amb tots els titulars"
    resum = u"Com utilitzar la jerarquia de títols. És  important respectar aquesta jerarquia si volem ser accessibles i millorar el nostre posicionament a Internet."
    cos = u"""<h2>In aliquam rhoncus sem</h2>
<p>Morbi dictum. Vestibulum adipiscing pulvinar quam.  In aliquam rhoncus sem. In mi erat, sodales eget, pretium interdum, malesuada  ac, augue. Aliquam sollicitudin, massa ut vestibulum posuere, massa arcu  elementum purus, eget vehicula lorem metus vel libero. Sed in dui id lectus  commodo elementum. Etiam rhoncus tortor. Proin a lorem. Ut nec velit. Quisque  varius. Proin nonummy justo dictum sapien tincidunt iaculis. Duis lobortis  pellentesque risus.</p>
<h3>In aliquam rhoncus sem</h3>
<p>Morbi dictum. Vestibulum adipiscing pulvinar quam.  In aliquam rhoncus sem. In mi erat, sodales eget, pretium interdum, malesuada  ac, augue. Aliquam sollicitudin, massa ut vestibulum posuere, massa arcu  elementum purus, eget vehicula lorem metus vel libero. Sed in dui id lectus  commodo elementum. Etiam rhoncus tortor. Proin a lorem. Ut nec velit. Quisque  varius. Proin nonummy justo dictum sapien tincidunt iaculis. Duis lobortis  pellentesque risus.</p>
<h4>In aliquam rhoncus sem</h4>
<p>Morbi dictum. Vestibulum adipiscing pulvinar quam.  In aliquam rhoncus sem. In mi erat, sodales eget, pretium interdum, malesuada  ac, augue. Aliquam sollicitudin, massa ut vestibulum posuere, massa arcu  elementum purus, eget vehicula lorem metus vel libero. Sed in dui id lectus  commodo elementum. Etiam rhoncus tortor. Proin a lorem. Ut nec velit. Quisque  varius. Proin nonummy justo dictum sapien tincidunt iaculis. Duis lobortis  pellentesque risus.</p>
<h5>In aliquam rhoncus sem</h5>
<p>Morbi dictum. Vestibulum adipiscing pulvinar quam.  In aliquam rhoncus sem. In mi erat, sodales eget, pretium interdum, malesuada  ac, augue. Aliquam sollicitudin, massa ut vestibulum posuere, massa arcu  elementum purus, eget vehicula lorem metus vel libero. Sed in dui id lectus  commodo elementum. Etiam rhoncus tortor. Proin a lorem. Ut nec velit. Quisque  varius. Proin nonummy justo dictum sapien tincidunt iaculis. Duis lobortis  pellentesque risus.</p>
<h6>In hac habitasse platea dictumst</h6>
<p>Nulla non orci. In egestas porttitor quam. Duis nec diam eget nibh mattis  tempus. Curabitur accumsan pede id odio. Nunc vitae libero. Aenean condimentum  diam et turpis. Vestibulum non risus. Ut consectetuer gravida elit. Aenean est  nunc, varius sed, aliquam eu, feugiat sit amet, metus. Sed venenatis odio id  eros. Phasellus placerat purus vel mi. In hac habitasse platea dictumst. Donec  aliquam porta odio. Ut facilisis. Donec ornare ipsum ut massa.</p>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})    

    titol = u"Dues columnes de text"
    resum = u"A cada columna s'hi poden afegir altres plantilles."
    cos = u"""<h2>Columnat 2 columnes</h2>
<div class="fila">
<div class="cella w1:2 p0">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</div>
<div class="cella w1:2 p1:2">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</div>
</div>
<div class="clearBoth"></div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})    

    titol = u"Combinacions de columnes"
    resum = u"Podeu fer d'1 a 4 columnes i fusionar-les entre elles. Elimineu les combinacions que no us interessin i treballeu amb el columnat que us agradi més."
    cos = u"""<h2>Columnat 4 columnes</h2>
<div class="fila">
<div class="cella w1:4 p0">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
<div class="cella w1:4 p1:4">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
<div class="cella w1:4 p2:4">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
<div class="cella w1:4 p3:4">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
</div>
<div class="visualClear"></div>
<h2>Columnat de 4 columnes amb 2 i 3 fusionades</h2>
<div class="fila">
<div class="cella w1:4 p0">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
<div class="cella w2:4 p1:4">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500.</div>
<div class="cella w1:4 p3:4">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
</div>
<div class="visualClear"></div>
<h2>Columnat de 3 columnes</h2>
<div class="fila">
<div class="cella w1:3 p0">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
<div class="cella w1:3 p1:3">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
<div class="cella w1:3 p2:3">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
</div>
<div class="visualClear"></div>
<h2>Columnat de 2 columnes amb 1, 2 i 3 fusionades</h2>
<div class="fila">
<div class="cella w3:4 p0">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type book.</div>
<div class="cella w1:4 p3:4">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</div>
</div>
<div class="visualClear"></div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})    

    titol = u"Destacat"
    resum = u"Text destacat."
    cos = u"""<div class="textDestacat">
<p>In aliquam rhoncus sem. Morbi dictum. Vestibulum adipiscing pulvinar quam.  In aliquam rhoncus sem. In mi erat, sodales eget, pretium interdum, malesuada  ac, augue. Aliquam sollicitudin, massa ut vestibulum posuere, massa arcu  elementum purus, eget vehicula lorem metus vel libero. Sed in dui id lectus  commodo elementum. Etiam rhoncus tortor. Proin a lorem. Ut nec velit. Quisque  varius. Proin nonummy justo dictum sapien tincidunt iaculis. Duis lobortis  pellentesque risus.</p>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})    

    titol = u"Destacat de color"
    resum = u"Destacat amb text més gran i color."
    cos = u"""<div class="destacatBandejat">
<p>In aliquam rhoncus sem. Morbi dictum. Vestibulum adipiscing pulvinar  quam. In aliquam rhoncus sem. In mi erat, sodales eget, pretium  interdum, malesuada ac, augue.</p>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})    

    titol = u"Destacat ratllat"
    resum = u"Destacat amb text petit i contorn ratllat."
    cos = u"""<div class="destacatQuadres">
<div class="destacatQuadresDins">
<p>In aliquam rhoncus sem. Morbi dictum. Vestibulum adipiscing pulvinar quam. In aliquam rhoncus sem. In mi erat, sodales eget, pretium interdum, malesuada ac, augue. Aliquam sollicitudin, massa ut vestibulum posuere, massa arcu elementum purus, eget vehicula lorem metus vel libero. Sed in dui id lectus commodo elementum. Etiam rhoncus tortor. Proin a lorem. Ut nec velit. Quisque varius. Proin nonummy justo dictum sapien tincidunt iaculis. Duis lobortis pellentesque risus.</p>
</div>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})    
    
    titol = u"Columna de suport"
    resum = u"Afegiu enllaços i contingut de suport a la columna de la dreta."
    cos = u"""<h2>Titular del bloc de text</h2>
<div class="colSupContenidor">
<div class="colSupDreta">
<div class="dalt200"></div>
<div class="caixaPortlet">
<h2>Enllaços relacionats</h2>
<ul>
<li><a href="#">Primer</a></li>
<li><a href="#">Segon</a></li>
<li><a href="#">Tercer</a></li>
</ul>
<br />
<h2>Bàners</h2>
<a href="#"><img alt="mostra" src="bn_1.gif" /></a> <a href="#"><img alt="mostra" src="bn_2.gif" /></a></div>
<div class="baix200"></div>
</div>
<div class="colSupEsq">
<p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
</div>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})    

    titol = u"Llistat"
    resum = u"Llistat d'ítems o enllaços."
    cos = u"""<div class="llistat">
<h2>Sed ultricies cursus lectus</h2>
<ul>
<li>Duis tellus. Donec ante dolor, iaculis nec, gravida ac, cursus in, eros.</li>
<li>Mauris vestibulum, felis et egestas ullamcorper, purus nibh vehicula sem, eu egestas ante nisl non justo.</li>
<li>Fusce tincidunt, lorem nec dapibus consectetuer, leo orci mollis ipsum, eget suscipit eros purus in ante.</li>
<li>At ipsum vitae est lacinia tincidunt. Maecenas elit orci, gravida ut, molestie non, venenatis vel, lorem.</li>
<li><a href="http://gw4.beta.upcnet.es">Sed lacinia. Suspendisse potenti. Sed ultricies cursus lectus. In id magna sit amet nibh suscipit euismod.</a></li>
<li>Fusce tincidunt, lorem nec dapibus consectetuer, leo orci mollis ipsum, eget suscipit eros purus in ante.</li>
<li><a href="http://gw4.beta.upcnet.es">At ipsum vitae est lacinia tincidunt. Maecenas elit orci, gravida ut, molestie non, venenatis vel, lorem.</a></li>
</ul>
</div>
<p> </p>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Enllaços relacionats"
    resum = u"Per afegir manualment un apartat d'enllaços relacionats a qualsevol contingut."
    cos = u"""<div class="llistatEnllacos">
<h2>Enllaços relacionats</h2>
<ul>
<li><a href="#">JDuis tellus</a></li>
<li><a href="#">Maecenas elit orci</a></li>
<li><a href="#">At ipsum vitae est lacinia tincidunt</a></li>
</ul>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})    

    titol = u"Enllaços destacats"
    resum = u"Per afegir manualment un apartat d'enllaços destacats a qualsevol contingut."
    cos = u"""<div class="llistatDestacat">
<h2>Llistat destacat</h2>
<ul>
<li><a href="#">JDuis tellus</a></li>
<li><a href="#">Maecenas elit orci</a></li>
<li><a href="#">At ipsum vitae est lacinia tincidunt</a></li>
</ul>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Contenidor"
    resum = u"Caixa per encabir-hi elements i limitar-los visualment."
    cos = u"""<div class="gb">
<h2>Titular de l'apartat</h2>
<p>Lorem ipsum dolor sit amet, consectetuer adipiscing  elit. Duis tellus. Donec ante dolor, iaculis nec, gravida ac, cursus in, eros.  Mauris vestibulum, felis et egestas ullamcorper, <a href="javascript:;">purus nibh vehicula sem</a>, eu  egestas ante nisl non justo. Fusce tincidunt, lorem nec dapibus consectetuer,  leo orci mollis ipsum, eget suscipit eros purus in ante.</p>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Taula de registres per files"
    resum = u"Per definir una taula de registres estructurada per columnes. Es pot ampliar en files i columnes."
    cos = u"""<h2>Titular de la taula</h2>
<div class="taulaRegistres">
<table summary="Detall d'estructura de la taula de registres">
<caption>Taula registres</caption> 
<tbody>
<tr class="cap">
<td>Item A<br /></td>
<td>Item B<br /></td>
<td>Total</td>
</tr>
<tr>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
<tr>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
<tr>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
<tr>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
<tr>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
</tbody>
</table>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Taula de registres per files i columnes"
    resum = u"Per definir una taula de registres estructurada per files i columnes. Es pot ampliar en files i columnes."
    cos = u"""<h2>Titular de la taula</h2>
<div class="taulaRegistres">
<table summary="Detall d'estructura de la taula de registres">
<caption>Taula resgistres</caption> 
<tbody>
<tr class="cap">
<td></td>
<td>Item A<br /></td>
<td>Item B<br /></td>
<td>Item C<br /></td>
<td>Item D<br /></td>
<td>Total</td>
</tr>
<tr>
<td class="fonsDestacat1">DL</td>
<td>34</td>
<td>43</td>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
<tr>
<td class="fonsDestacat1">DT</td>
<td>34</td>
<td>43</td>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
<tr>
<td class="fonsDestacat1">DC</td>
<td>34</td>
<td>43</td>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
<tr>
<td class="fonsDestacat1">DJ</td>
<td>34</td>
<td>43</td>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
<tr>
<td class="fonsDestacat1">DV</td>
<td>34</td>
<td>43</td>
<td>34</td>
<td>43</td>
<td>77</td>
</tr>
</tbody>
</table>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Calendari"
    resum = u"Per representar gràficament els esdeveniments o activitats d'un mes determinat. Es pot representar tot un any afegint successivament un mes darrera l'altre."
    cos = u"""<div class="calendari">
<p class="titular2">Febrer 2012</p>
<table summary="Detall d'estructura del calendari">
<caption>Calendari</caption> 
<tbody>
<tr>
<td class="fonsDestacat2">dl</td>
<td class="fonsDestacat2">dm</td>
<td class="fonsDestacat2">dc</td>
<td class="fonsDestacat2">dj</td>
<td class="fonsDestacat2">dv</td>
<td class="fonsDestacat2">ds</td>
<td class="fonsDestacat2">dg</td>
</tr>
<tr>
<td></td>
<td></td>
<td>1</td>
<td>2</td>
<td>3</td>
<td>4</td>
<td>5</td>
</tr>
<tr>
<td>6</td>
<td>7</td>
<td>8</td>
<td>9</td>
<td>10</td>
<td>11</td>
<td>12</td>
</tr>
<tr>
<td>13</td>
<td>14</td>
<td>15</td>
<td>16</td>
<td>17</td>
<td>18</td>
<td>19</td>
</tr>
<tr>
<td>20</td>
<td>21</td>
<td>22</td>
<td>23</td>
<td>24</td>
<td>25</td>
<td>26</td>
</tr>
<tr>
<td>27</td>
<td>28</td>
<td>29</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>
</div>
<div class="notesCalendari"><span class="titular2">dijous 4.</span> inauguració centre<br /> <span class="titular2">dimecres 17.</span> lliurament premis fotografia tecnociència<br /> <span class="titular2">dilluns 29.</span> conferència</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Fitxa amb imatge a l'esquerra"
    resum = u"Per definir fitxes amb un títol, una imatge, una descripció o determinats atributs destacables."
    cos = u"""<div class="fletxa_fitxa"></div>
<div class="fitxa">
<h2>Títol de la fitxa</h2>
<h3>At ipsum vitae est lacinia tincidunt</h3>
<div class="align_left"><img alt="fotoMostra" src="mostra.jpg" /></div>
<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Duis tellus. Donec ante dolor, iaculis nec, gravida ac, cursus in, eros. Mauris vestibulum, felis et egestas ullamcorper, purus nibh vehicula sem, eu egestas ante nisl non justo.</p>
<br />
<h4>Lorem Ipsum</h4>
<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</p>
<br />
<div class="separadorH"></div>
<h5>Duis tellus</h5>
<p>Donec ante dolor, iaculis nec, gravida ac, cursus in, eros.</p>
<br />
<div class="separadorH"></div>
<h6>Mauris Vestibulum</h6>
<p>Felis et egestas ullamcorper, purus nibh vehicula sem, eu egestas ante nisl non justo.</p>
<div class="separadorH"></div>
<h6>gravida ac</h6>
<p>Donec ante dolor, iaculis nec, gravida ac, cursus in, eros.</p>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Fitxa amb imatge a la dreta"
    resum = u"Per definir fitxes amb un títol, una imatge, una descripció o determinats atributs destacables."
    cos = u"""<div class="fletxa_fitxa"></div>
<div class="fitxa">
<h2>Títol de la fitxa</h2>
<h3>At ipsum vitae est lacinia tincidunt</h3>
<div class="align_right"><img alt="fotoMostra" src="mostra.jpg" /></div>
<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Duis tellus. Donec ante dolor, iaculis nec, gravida ac, cursus in, eros. Mauris vestibulum, felis et egestas ullamcorper, purus nibh vehicula sem, eu egestas ante nisl non justo.</p>
<br />
<h4>Lorem Ipsum</h4>
<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</p>
<br />
<div class="separadorH"></div>
<h5>Duis tellus</h5>
<p>Donec ante dolor, iaculis nec, gravida ac, cursus in, eros.</p>
<br />
<div class="separadorH"></div>
<h6>Mauris Vestibulum</h6>
<p>Felis et egestas ullamcorper, purus nibh vehicula sem, eu egestas ante nisl non justo.</p>
<div class="separadorH"></div>
<h6>gravida ac</h6>
<p>Donec ante dolor, iaculis nec, gravida ac, cursus in, eros.</p>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Àlbum de fotografies"
    resum = u"Crea un àlbum amb les miniatures de fotografies."
    cos = u"""<h2>Àlbum de Fotografies</h2>
<div>
<div class="photoAlbumEntry"><a href="sampleimg1.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg1.jpg" class="estilImgPhotoAlbum3" src="sampleimg1.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg1.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg2.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg2.jpg" class="estilImgPhotoAlbum1" src="sampleimg2.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg2.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg3.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg3.jpg" class="estilImgPhotoAlbum1" src="sampleimg3.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg3.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg4.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg4.jpg" class="estilImgPhotoAlbum1" src="sampleimg4.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg4.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg5.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg5.jpg" class="estilImgPhotoAlbum1" src="sampleimg5.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg5.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg6.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg6.jpg" class="estilImgPhotoAlbum1" src="sampleimg6.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg6.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg7.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg7.jpg" class="estilImgPhotoAlbum1" src="sampleimg7.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg7.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg8.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg8.jpg" class="estilImgPhotoAlbum1" src="sampleimg8.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg8.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg9.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg9.jpg" class="estilImgPhotoAlbum1" src="sampleimg9.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg9.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg10.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg10.jpg" class="estilImgPhotoAlbum2" src="sampleimg10.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg10.jpg</span> </a></div>
<div class="photoAlbumEntry"><a href="sampleimg11.jpg"> <span class="photoAlbumEntryWrapper"> <img alt="sampleimg11.jpg" class="estilImgPhotoAlbum1" src="sampleimg11.jpg" /> </span> <span class="photoAlbumEntryTitle">sampleimg11.jpg</span> </a></div>
<div class="visualClear"><!-- --></div>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Imatge amb text lateral"
    resum = u"Imatge damunt la qual hi apareix un text."
    cos = u"""<h2>Títol [opcional]</h2>
<div id="FCKTdiv1imatgedamunttext"><img alt="foto mostra" src="sampleimg9.jpg" />
<div id="FCKTdiv2imatgedamunttext">
<div id="FCKTdiv3imatgedamunttext">Lorem ipsum dolor sit amet consectetuer Vestibulum neque dolor felis malesuada. Id dolor magna enim pellentesque condimentum ante ullamcorper urna tellus id. At non Ut commodo consequat gravida sem vel tempus metus eleifend. Ridiculus pretium sit mauris pellentesque interdum tellus at id ante see interdum tellus at id ante semper.</div>
</div>
</div>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})

    titol = u"Assenyalar enllaços"
    resum = u"Classes que es poden afegir als enllaços per indicar el tipus d'element enllaçat."
    cos = u"""<h2>Classes especials per assenyalar enllaços</h2>
<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore <a class="pdf" href="#">magna</a> aliquam erat volutpat. Ut wisi enim ad minim veniam, ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse <a class="doc" href="#">molestie</a> consequat, vel illum dolore eu  te feugait nulla facilisi. Nam liber tempor nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non <a class="ppt" href="#">habent claritatem</a> insitam; est usus legentis in iis qui. Investigationes demonstraverunt lectores legere me lius  <a class="xlsdf" href="#">quod ii</a> legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. <a class="down" href="#">Mirum est notare</a> quam littera gothica, parum claram, anteposuerit litterarum formas humanitatis <a class="txt" href="#">per seacula</a> quarta decima et quinta decima. <a class="https" href="#"> Eodem modo typi</a>, qui nunc nobis  <a class="vid" href="#">videntur</a> parum clari, fiant  <a class="img" href="#">sollemnes</a> in futurum.</p>
<p><strong>Les classes són: pdf, doc, ppt, xls, down, txt, https, down, vid, img.</strong></p>"""
    plantilles.append({'titol':titol, 'resum':resum, 'cos':cos})


    return plantilles
