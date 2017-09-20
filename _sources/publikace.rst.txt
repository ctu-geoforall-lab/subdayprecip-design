Publikace projektu
==================

Pro publikaci je nutné do programu QGIS doinstalovat zásuvný modul
**Gisquick plugin**. Podobně jako v případě WPS klienta jej
nainstalujeme standardním způsobem (:menuselection:`Zásuvné moduly -->
Spravovat a instalovat zásuvné moduly`).

.. figure:: img/qgis-gisquick-plugin.svg

   Instalace Gisquick zásuvného modulu.

Před publikací ještě nastavíme ve vlastnostech projektu
(:menuselection:`Projekt --> Vlastnosti projektu`) v záložce
``Obecné`` **Název projektu**.

.. figure:: img/qgis-project-name.svg

   Nastavení názvu projektu před publikací.

Abychom mohli po publikaci jednotlivé prvky povodí identifikovat myší
je ještě nutno v záložce ``OWS Server`` aktivovat **WFS schopnosti**.

.. figure:: img/qgis-project-wfs.svg

   Aktivace WFS pro identifikaci prvků povodí.

Změny v projektu uložíme a spustíme Gisquick plugin
(:menuselection:`Web --> Gisquick --> Publish in Gisquick`). Pro
nastavení publikace se otevře jednoduchý průvodce, kde můžeme nastavit
vlastnosti projektu, podkladové vrstvy, témata a pod.

.. figure:: img/qgis-gisquick-publish-0.png

   Nejprve nastavíme podkladové vrstvy, vlastnosti projektu.

.. note:: Pokud máte v projektu vrstvy s různým rozsahem (typicky
   např. WMS vrstvu), tak je vhodné nastavit výchozí rozsah
   publikovaného projektu podle zájmové vrstvy, v našem případě
   povodí IV. řádu.

   .. figure:: img/qgis-gisquick-extent.svg

      Nastavení výchozího rozsahu publikovaného projektu.
	  
.. figure:: img/qgis-gisquick-publish-1.png

   Na další stránce průvodce lze nastavit jednotlivá témata, seskupin
   vrstvy do logických skupin.

.. figure:: img/qgis-gisquick-publish-2.png

   Na další stránce průvodce můžeme nastavení publikace zkontrolovat.
   
.. figure:: img/qgis-gisquick-publish-3.svg

   Na poslední stránce průvodce aktivujeme volbu **Create project zip
   for upload**.

Projekt publikujeme pomocí tlačítka ``Publish``. Výsledkem bude nově
vytvořený soubor ve formátu zip vytvořený v nadřazeném adresáři, kde
je uložen projekt. Tento soubor v následujícím kroku nahrajeme na
publikační server.
   
Nahrání projektu na publikační server
-------------------------------------

Předpokládáme, že máme vytvořen na publikační serveru :doc:`vlastní
učet <registrace>` a otevřen prázdný projekt. Otevřeme *User menu*
vpravo nahoře a vybereme položku **My profile**.

.. figure:: img/gisquick-user-menu.svg

V profilu uživatele vybereme ``Upload project``. Vybereme zip soubor
vytvořený zásuvným modulem Gisquick a pomocí tlačítka ``Upload``
nahrajeme na publikační server.

.. figure:: img/gisquick-upload-project.svg

   Nahraní projektu na publikační server.

Po nahrání projektu se přepneme do záložky ``My Projects``, kde by se
měl objevit nově nahraný projekt. Webovou mapovou aplikaci s tímto
projektem otevřeme jednoduše poklikáním na název projektu.

.. figure:: img/gisquick-my-project.svg

   Otevření publikovaného projektu.

Na následující stránce potvrdíme přihlašovací udaje pomocí tlačítka
``CONTINUE``. Poté se otevře nově publikovaný projekt.

.. figure:: img/gisquick-project-final.png

   Ukázka testovacího publikovaného projektu.

.. tip:: Pro podrobný popis uživatelského rozhraní webové mapové
   aplikace Gisquick v `oficiální dokumentaci
   <http://gisquick.readthedocs.io/en/latest/user-interface.html>`__.

Nezvývá nic jiného než otestovat Vaši první publikovaný projekt a
sdílet vytvořenou webovou mapovou aplikaci s Vašimi kolegy.
