infoboard
=========

Installation
------------

Nova verzia infoboardu, ktora je zalozena na Qt a QML, potrebuje, aby boli
Qt a QML dostupne, rovnako ako aj Python bindingy.

**Pozor**: na to, aby bolo mozne pouzit Videoplayer, ktory je sucastou QML a
dolezitou sucastou infoboardu, je potrebne mat nainstalovany Debian/Ubuntu
balik `libdeclarative-multimedia`.

Pre prehravanie `.wmv` videi Qt potrebuje specialny Gstreamer codec (jeho
nepritomnost sa prejavi chybovou hlaskou `Your GStreamer installation is
missing a plugin`). Pre jeho instalaciu je vhodne konzultovat [tento
clanok](http://askubuntu.com/a/456259).

Infoboard potrebuje divnu verziu modulu watchdog. Existuju dve moznosti, ako ju
nainstalovat. Bud nasledovne:

        $ wget -c http://pypi.python.org/packages/source/w/watchdog/watchdog-0.6.0.tar.gz
        $ tar zxvf watchdog-0.6.0.tar.gz
        $ cd watchdog-0.6.0
        # python setup.py install

alebo spustenim `pip install -r requirements.txt` ako root.
