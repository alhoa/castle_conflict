# Castle Conflict

Castle Conflict is a small strategy game written in python for the CS-A1121 -course.

![Game Title](/src/graphics/title.png)

### 1. Kansiorakenne

Kaikki ohjelmaan liittyvä dokumentaatio löytyy /docs kansiosta. 
Ohjelman lähdekood on kaikki /src kansiossa, minkä lisäksi /src alikansioissa on erilaisia pelin assetteja. Tarkka kuvaus kansiorakenteesta löytyy docs/loppuraportin kappaleesta 7. Peliä varten on luotu useita esimerkkitiedostoja, joista voi katsoa mallia halutessaan luoda lisää peliskenaarioita. 

### 2. Käyttöohje

Kuvat, joissa on selitetty er UI elementtien toiminta, löytyvät loppuraportin kappaleesta 2.
Pelin voi käynnistää suorittamalla main.py ohjelma. Tällöin käyttäjälle avautuu dialogi-ikkuna, josta hän voi avata haluamansa peliskenaarion. Pelin pelaaminen etenee seuraavassa järjestyksessä:

- Valittuaan skenaation pelaajan eteen avautuu pelikenttä, jossa hän ja tietokone valitsevat vuorotellen aloitussijaintinsa. Pelaajan aloituspisteet onmerkitty sinisillä portaaleilla, joita klikkaamalla pelaaja valitsee aloituspisteen ruudun alareunassa aktiivisena merkatulle hahmolle. Hahmon aktiivisuusmerkki on  vuorojärjestyksessä valkoinen pallo hahmon ikonin päällä. 

- Kun kaikki pelaajat on sijoitettu kentälle, peli alkaa ja hahmot tekevät toimintoja omina vuoroinaan. Graafisen ruudun alareunasta näkee vuorojärjestyksen sekä kullakin hetkellä aktiivisena olevan hahmon. Lisäksi vuorojärjestyksestä näkee nopeasti kaikkien hahmojen elämäpisteet. 

- Jos pelaaja haluaa saada tietää lisää informaatiota hahmoista, voi vuorojärjestysikoneita klikkaamalla saada lisää informaatiota hahmojen asetukista.

- Tämä informaatio tulostuu pelin tekstiruutuun, johon ilmestyy kaikki pelissä tapahtuvat tärkeät asiat. 

- Aktiivisen pelaajan elämä- (HP), toiminto- (AP) ja liikkumispisteet (MP) näkyvät ruudn alareunassa keskellä.

- Pisteiden oikealla puolella on pelaajan mahdolliset toiminnot. Kaikille pelaajille yhteisiä toimntoja ovat liikkuminen (kenkä) sekä vuoron päättäminen (nuoli). Näiden lisäksi jokaisella hahmolla voi olla eri määrä hyökkäyksiä, joita hän voi tehdä. Nämä hyökkäykset on merkitty omilla painikkeillaan. 

- Jos käyttäjä haluaa saada lisää informaatiota hyökkäyksistä tai muista toiminnoista, ilmestyy painikkeiden päälle informaatiolaatikko kun niiden päällä pitää hiirtä hetken. Tämä kertoo hyökkäyksen hinnan, maksimietäisyyden, vahinkolaskelman sekä mahdolliset muut vaikutukset. 

- Hahmon liikuttaminen tapahtuu painamalla liikkumisnappia ja valitsemalla ruutu johon pelaaja haluaa liikkua. Peli näyttää käveltävän reitin, jonka väristä näkee onko hahmolla riittävästä liikkumispisteitä liikkeen toteuttamiseen.

- Hyökkäysnappia painamalla pelikenttään korostetaan hyökkäyksen alue, josta pelaaja voi valita haluamansa kohderuudun.

- Peli päättyy kun kaikki toisen puolen hahmot ovat kuolleet. Tällä hetkellä pelin päättyessä ei ilmesty suurta fanfaaria vaan siitä ilmoitetaan ainoastaan pelin tekstiruudussa. Pelistä poistutaan painamalla ESC nappia pelin päätyttyä.



[Other information still in English]
### Saves

Currently the path of the game save is set in main.py, which determines all players and game map.

The save file is divided into block which are formed as follows:

\#<br/>
[BLOCK NAME] : ([AI if block is enemy])<br/>
[PARAM 1] : [VALUE 1]<br/>
[PARAM 2] : [VALUE 2]<br/>
/#<br/>

The save file must atleast include an Information block, which includes a map file name as well as one character. It is however recommended to add at least one player and one enemy to be able to play the game.


### Maps

The map files are included in the maps folder. ALl maps must be sved in .bmp for the parser to work.
In the maps the colors have the following designations:  
(255,0,0) = Wall  
(254,0,0) = Rock  
(253,0,0) = Sandstone  
(0,0,255) = Enemy spawn point  
(0,255,0) = Player spawn point  
(255,255,0) = Out of bounds (water)  

The colors must have the exact rgb value to be detected and all other colors will be interpreted as ground.
