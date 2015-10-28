####################################################################
# QJ1520265 project - source code and support files for OGC WMS and
# WPS implementation http://rain.fsv.cvut.cz
#
# Purpose: MapFile for MapServer
# Author: Martin Landa <martin.landa fsv.cvut.cz>
# Licence: see LICENCE file for details
####################################################################

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
      "wms_title"                        "Rain WMS server"
      "wms_onlineresource"               "#URL#"
      "wms_abstract"                     "WMS server projektu QJ1520265, vice informaci na http://rain.fsv.cvut.cz/webove-sluzby/wms/"
      "wms_srs"                          "EPSG:5514"
      "wms_encoding"                     "UTF-8"
      "wms_contactelectronicmailaddress" "martin.landa@fsv.cvut.cz"
      "wms_contactperson"                "Martin Landa"
      "wms_contactorganization"          "CVUT v Praze, Fakulta stavebni"
      "wms_contactvoicetelephone"        "+420 224 354 644"
      "wms_enable_request"               "*"
    END # METADATA
  END # WEB

  LAYER
    NAME "H_002"
    METADATA
      "wms_title"           "H_002"
      "wms_abstract"        "H_002"
      "wms_onlineresource"  "#URL#"
      "wms_srs"             "EPSG:5514"
      "wms_enable_request"  "*"
      "wms_extent"           "-907000 -1230000 -429000 -933000"
    END # METADATA
    TYPE RASTER
    STATUS ON
    DATA "#DATADIR#/grassdata/subdayprecip/H_002.tif" # "#DATADIR#/grassdata/subdayprecip/PERMANENT/cellhd/H_002"
    CLASS NAME "H_002"
    END # CLASS
  END # LAYER

  LAYER
    NAME "H_005"
    METADATA
      "wms_title"           "H_005"
      "wms_abstract"        "H_005"
      "wms_onlineresource"  "#URL#"
      "wms_srs"             "EPSG:5514"
      "wms_enable_request"  "*"
      "wms_extent"           "-907000 -1230000 -429000 -933000"
    END # METADATA
    TYPE RASTER
    STATUS ON
    DATA "#DATADIR#/grassdata/subdayprecip/H_005.tif" # "#DATADIR#/grassdata/subdayprecip/PERMANENT/cellhd/H_005"
    CLASS NAME "H_005"
    END # CLASS
  END # LAYER

  LAYER
    NAME "H_010"
    METADATA
      "wms_title"           "H_010"
      "wms_abstract"        "H_010"
      "wms_onlineresource"  "#URL#"
      "wms_srs"             "EPSG:5514"
      "wms_enable_request"  "*"
      "wms_extent"           "-907000 -1230000 -429000 -933000"
    END # METADATA
    TYPE RASTER
    STATUS ON
    DATA "#DATADIR#/grassdata/subdayprecip/H_010.tif" # "#DATADIR#/grassdata/subdayprecip/PERMANENT/cellhd/H_010"
    CLASS NAME "H_010"
    END # CLASS
  END # LAYER

  LAYER
    NAME "H_020"
    METADATA
      "wms_title"           "H_020"
      "wms_abstract"        "H_020"
      "wms_onlineresource"  "#URL#"
      "wms_srs"             "EPSG:5514"
      "wms_enable_request"  "*"
      "wms_extent"          "-907000 -1230000 -429000 -933000"
    END # METADATA
    TYPE RASTER
    STATUS ON
    DATA "#DATADIR#/grassdata/subdayprecip/H_020.tif" # "#DATADIR#/grassdata/subdayprecip/PERMANENT/cellhd/H_020"
    CLASS NAME "H_020"
    END # CLASS
  END # LAYER

  LAYER
    NAME "H_050"
    METADATA
      "wms_title"           "H_050"
      "wms_abstract"        "H_050"
      "wms_onlineresource"  "#URL#"
      "wms_srs"             "EPSG:5514"
      "wms_enable_request"  "*"
      "wms_extent"          "-907000 -1230000 -429000 -933000"
    END # METADATA
    TYPE RASTER
    STATUS ON
    DATA "#DATADIR#/grassdata/subdayprecip/H_050.tif" # "#DATADIR#/grassdata/subdayprecip/PERMANENT/cellhd/H_050"
    CLASS NAME "H_050"
    END # CLASS
  END # LAYER

  LAYER
    NAME "H_100"
    METADATA
      "wms_title"           "H_100"
      "wms_abstract"        "H_100"
      "wms_onlineresource"  "#URL#"
      "wms_srs"             "EPSG:5514"
      "wms_enable_request"  "*"
      "wms_extent"          "-907000 -1230000 -429000 -933000"
    END # METADATA
    TYPE RASTER
    STATUS ON
    DATA "#DATADIR#/grassdata/subdayprecip/H_100.tif" # "#DATADIR#/grassdata/subdayprecip/PERMANENT/cellhd/H_100"
    CLASS NAME "H_100"
    END # CLASS
  END # LAYER

END # MAP