MAP
  NAME           "Rain"
  STATUS         ON
  SIZE           640 480
  EXTENT         -907000 -1230000 -429000 -933000
  UNITS          meters
  IMAGECOLOR     255 255 255
  IMAGETYPE      png
 
  PROJECTION
    "init=epsg:5514"
  END # PROJECTION

  WEB
    IMAGEPATH "/var/tmp/ms_tmp/"
    IMAGEURL "/tmp/"
    METADATA
      "wfs_title"                        "Rain WFS server"
      "wfs_onlineresource"               "#URL#"
      "wfs_abstract"                     "WFS server projektu Rain, vice informaci na http://rain.fsv.cvut.cz"
      "wfs_srs"                          "EPSG:5514 EPSG:2065 EPSG:102067"
      "wfs_encoding"                     "UTF-8"
      "wfs_contactelectronicmailaddress" "martin.landa@fsv.cvut.cz"
      "wfs_contactperson"                "Martin Landa"
      "wfs_contactorganization"          "CVUT v Praze, Fakulta stavebni"
      "wfs_contactvoicetelephone"        "+420 224 354 644"
      "wfs_enable_request"               "*"
    END # METADATA
  END # WEB

  LAYER
    NAME "bpej"
    METADATA
      "wfs_title"           "Celostátní databáze BPEJ"
      "wfs_abstract"        "Celostátní databáze BPEJ, https://www.spucr.cz/bpej/celostatni-databaze-bpej"
      "wfs_onlineresource"  "#URL#"
      "wfs_srs"             "EPSG:5514 EPSG:2065 EPSG:102067"
      "wfs_enable_request"  "*"
      "wfs_extent"           "-907000 -1230000 -429000 -933000"
    END # METADATA
    PROJECTION
	"init=epsg:5514"
    END # PROJECTION
    TYPE VECTOR
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "host=localhost dbname=bpej user=mapserver password=XXX"
    DATA "wkb_geometry from bpej"
  END # LAYER
END # MAP
