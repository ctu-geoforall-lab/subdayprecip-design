// GLOBAL VARIABLES
var map, wpsObj, urlWPS, obsPoint;

// URLs change according to needs
var urlWPS="https://rain1.fsv.cvut.cz/services/wps";

// OPTION GRITTER
$.extend($.gritter.options,{position:'top-left',fade_in_speed:'medium',fade_out_speed:2000,time:3000});

/*
 * CREATION OF WPS OBJECT, CALL OF WPS OBJECT
 * 
 */

function callWPS(){
    // Creation of WPS object
    // EVENTS: onSucceed and onFailed
    // EVENT LIST: "ProcessAccepted", "ProcessSucceeded", "ProcessFailed", "ProcessStarted", "ProcessPaused"
    triggerGritter("Spouštím výpočet");

    var lat = document.getElementById('lat').value;
    var lon = document.getElementById('lon').value;

    wpsObj = new OpenLayers.WPS(urlWPS, {onSucceeded: onExecuted, onFailed: onError});
    
    // Setting inputs
    var obsXInput = new OpenLayers.WPS.LiteralPut({
        identifier : "obs_x",
        value: lat // obsPoint.x 
    });
    var obsYInput = new OpenLayers.WPS.LiteralPut({
        identifier : "obs_y",
        value: lon // obsPoint.y
    });
    var layers = map.getLayersBy("visibility", true);
    var raster = new OpenLayers.WPS.LiteralPut({
        identifier : "return_period",
        value: document.getElementById('raster').value
    });
    var rainLength = new OpenLayers.WPS.LiteralPut({
        identifier : "rainlength",
        value: document.getElementById('rainlength').value
    });

    // Setting outputs
    var outputValue = new OpenLayers.WPS.LiteralPut({identifier:"output"});

    
    // Creating Process
    var processName = "d-rain-point"
    rainProcess = new OpenLayers.WPS.Process({identifier: processName,
                                                  inputs: [obsXInput, obsYInput, raster, rainLength],
                                                  async: false,
                                                  outputs: [outputValue]});

    // Adding process to WPS object - one WPS object may have multiple
    // processes
    wpsObj.addProcess(rainProcess);
    wpsObj.execute(processName);
}

/*
 * WPS events
 */

// Everything went ok 
function onExecuted(process) {
    result = process.getOutput("output").value;
    showResult(result);
}

// WPS exception
function onError(process){
    textData="Error Code:" + process.exception.code + "<br />" + "Text:" + process.exception.text;
    triggerGritter(textData);

    showResult(undefined);
};

/*
 * GENERIC FUNCTIONS
 */
function triggerGritter(text){
    $.gritter.add({title:"Status:",text:"<p align='center' class='textGitter'>"+text+"<\p>"});
};

function showResult(text){
    var div = document.getElementById('resultNote');
    var raster = document.getElementById('raster').value;
    var rainLength = document.getElementById('rainlength').value;
    var layers = map.getLayersBy("visibility", true);
    var lat = document.getElementById('lat').value;
    var lon = document.getElementById('lon').value;

    if (text == undefined) {
	div.innerHTML = 'Chyba ve výpočtu';
    }
    else {
	div.innerHTML = '<div align="center">Výsledek</div>';
	// '<table><tr><td>GPS:</td><td>' + obsPoint.x.toFixed(5) + ', ' + obsPoint.y.toFixed(5) +
	div.innerHTML += '<table><tr><td>GPS:</td><td>' + parseFloat(lat).toFixed(5) + ', ' + parseFloat(lon).toFixed(5) +
	    '</td></tr><tr><td>Doba opakování:</td><td>' + String(raster) +
	    '</td></tr><tr><td>Délka návrhové srážky:</td><td>' + parseFloat(rainLength).toFixed(0) + ' min' +
	    '</td></tr><tr><td>Hodnota návrhové srážky:</td><td><font size=+1 color="red">' + parseFloat(text).toFixed(1) +
	    '</font> mm</td></tr></table>';
    }
};

function setCoord(){
    document.getElementById('lat').value = obsPoint.x;
    document.getElementById('lon').value = obsPoint.y;
};

function setPoint(){
    var lat = document.getElementById('lat').value;
    var lon = document.getElementById('lon').value;

    obsPoint = new OpenLayers.Geometry.Point(lat, lon);

    obsLayer.removeAllFeatures();
    obsLayer.addFeatures([new OpenLayers.Feature.Vector(obsPoint, {icon: "./img/map-pointer.png"})]);
    
    map.setCenter(new OpenLayers.LonLat(lat, lon), 14);
};

/*
 *  ON DOM LOAD QUICKSTART EVERYTHING
 */

$(document).ready(function() {
    var switcher = new OpenLayers.Control.LayerSwitcher();
    
    var options = { projection: new OpenLayers.Projection('EPSG:4326'), 
                    units: 'deg',
                    controls: [ new OpenLayers.Control.Navigation(),
                                new OpenLayers.Control.PanPanel(),
				switcher],
                  };
    
    map = new OpenLayers.Map('map1', options);
    //switcher.maximizeControl();
    
    // base layer
    zm50Layer = new OpenLayers.Layer.WMS("ZM 50 (CUZK)",
                                         "https://geoportal.cuzk.cz/WMS_ZM50_PUB/WMService.aspx",
                                         {layers: "GR_ZM50", srs: "EPSG:4326"});
    zm50Layer.title = "ZM50";

    h002Layer = new OpenLayers.Layer.WMS("2 roky",
                                         "https://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_N2_24h", srs: "EPSG:4326"});
    h002Layer.title = "N2";

    h005Layer = new OpenLayers.Layer.WMS("5 let",
                                         "https://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_N5_24h", srs: "EPSG:4326"});
    h005Layer.title = "N5";

    h010Layer = new OpenLayers.Layer.WMS("10 let",
                                         "https://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_N10_24h", srs: "EPSG:4326"});
    h010Layer.title = "N10";
    
    h020Layer = new OpenLayers.Layer.WMS("20 let",
                                         "https://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_N20_24h", srs: "EPSG:4326"});
    h020Layer.title = "N20";
    
    h050Layer = new OpenLayers.Layer.WMS("50 let",
                                         "https://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_N50_24h", srs: "EPSG:4326"});
    h050Layer.title = "N50";
    
    h100Layer = new OpenLayers.Layer.WMS("100 let",
                                         "https://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_N100_24h", srs: "EPSG:4326"});
    h100Layer.title = "N100";

    // observation point layer
    obsLayer = new OpenLayers.Layer.Vector("Observační bod");
    obsPoint = new OpenLayers.Geometry.Point(15.474897, 49.803578);
    
    // style observation point map of obsLayer
    var vectorStyle= new OpenLayers.Style({externalGraphic:'${icon}', pointRadius: 15});
    obsLayer.styleMap = new OpenLayers.StyleMap({'default':vectorStyle}); 
    obsLayer.addFeatures([new OpenLayers.Feature.Vector(obsPoint, {icon: "./img/map-pointer.png"})]);
    
    // add everything to map
    map.addLayers([zm50Layer, h002Layer, h005Layer, h010Layer, h020Layer, h050Layer, h100Layer, obsLayer]);
    map.setCenter(new OpenLayers.LonLat(15.474897, 49.803578), 8);
    
    // drag feature control here is where wps is called
    controlDrag = new OpenLayers.Control.DragFeature(obsLayer,
                                                     {onComplete: function(featureObj, pixelObj) {
	                                                 setCoord();
	                                              } // end function
	                                             } // end onComplete
	                                            ); //end controlDrag
    
    // add control to map 
    map.addControl(controlDrag);
    controlDrag.activate();
}); //end of document ready
