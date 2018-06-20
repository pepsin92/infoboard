infoboard
=========

Installation
------------


### Qt5

Nova verzia infoboardu, ktora je zalozena na Qt5 a PyQt. Odporucane distro je Debian.
Je potrebne mat bindingy na QtMultimedia a QtWebEngine.

**Pozor**: na to, aby bolo mozne pouzit Videoplayer, ktory je sucastou QML a
dolezitou sucastou infoboardu, je potrebne mat nainstalovany Debian/Ubuntu
balik `libdeclarative-multimedia`.

Pre prehravanie `.wmv` videi Qt potrebuje specialny Gstreamer codec (jeho
nepritomnost sa prejavi chybovou hlaskou `Your GStreamer installation is
missing a plugin`). Pre jeho instalaciu je vhodne konzultovat [tento
clanok](http://askubuntu.com/a/456259).

### XMonad a unclutter

QML verziu Infoboardu je velmi vhodne pouzivat s xmonad-om. Jednak preto, ze v
nom dobre vyzera a druhak preto, ze tento repozitar obsahuje custom
`xmonad.hs`. Je ho mozne najst v priecinku `misc/xmonad` spolu so scriptom,
ktory ma byt spustany automaticky pri spusteni xmonad-u (autostart). Ten
zabezpeci, ze ziadny Infoboard nebude bezat a spusti jeho novu instanciu.

**Poznamka:** aj ked to nieje priamo nutne, je velmi doporucovane nainstalovat
balik `unclutter`, ktory je spustany pri spusteni xmonad-u a zabezpeci, ze sa
na obrazovke nebude objavovat kurzor.

Nainstalovat custom konfiguracne scripty je mozne nasledovne:

1. Premiestnime subory z `misc/xmonad` do `~/.xmonad`, kde `~` oznacuje
   domovsky priecinok pouzivatela ($HOME).


   cp -R misc/xmonad/ ~/.xmonad


2. xmonad zrekompilujeme a znova spustime


    xmonad --recompile
    xmonad --restart


3. Vysledkom by mal byt xmonad bez cervenych okrajov ktory uz stihol spustit
   novu instanciu Infoboardu.

#### Nastavenie rozlisenia

Pri deploymentoch infoboardu byva casto problem, ze v case, kedy sa server
spusta este nemusi pre X server fyzicky existovat zobrazovaci device (od
slovenskeho 'divaj sa'). V subore `~/.xmonad/autostart` je preto funkcia, ktora
sa na pozadi kazdych 5 sekund snazi enforcovat rozlisenie 1920x1080 na
zariadeni VGA1. Pre zmenu rozlisenia teda treba upravit prave tento subor.
