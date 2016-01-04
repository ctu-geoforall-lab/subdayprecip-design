// GLOBAL VARIABLES
var map, wpsObj, urlWPS, obsPoint;

// URLs change according to needs
var urlWPS="http://rain1.fsv.cvut.cz/services/wps";

// OPTION GRITTER
$.extend($.gritter.options,{position:'top-left',fade_in_speed:'medium',fade_out_speed:2000,time:2000});

/*
 * CREATION OF WPS OBJECT, CALL OF WPS OBJECT
 * 
 */

function callWPS(){
    // Creation of WPS object
    // EVENTS: onSucceed and onFailed
    // EVENT LIST: "ProcessAccepted", "ProcessSucceeded", "ProcessFailed", "ProcessStarted", "ProcessPaused"
    wpsObj = new OpenLayers.WPS(urlWPS, {onSucceeded: onExecuted, onFailed: onError});
    
    // Setting inputs
    var obsXInput = new OpenLayers.WPS.LiteralPut({
        identifier : "obs_x",
        value: obsPoint.x 
    });
    var obsYInput = new OpenLayers.WPS.LiteralPut({
        identifier : "obs_y",
        value: obsPoint.y
    });
    var layers = map.getLayersBy("visibility", true);
    var raster = new OpenLayers.WPS.LiteralPut({
        identifier : "raster",
        value: layers[0].title
    });
    var rainLength = new OpenLayers.WPS.LiteralPut({
        identifier : "rainlength",
        value: document.getElementById('rainlength').value
    });

    // Setting outputs
    var outputValue = new OpenLayers.WPS.LiteralPut({identifier:"output"});

    
    // Creating Process
    var processName = "subdayprecip-design-point"
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
};

/*
 * GENERIC FUNCTIONS
 */
function triggerGritter(text){
    $.gritter.add({title:"Status:",text:"<p align='center' class='textGitter'>"+text+"<\p>"});
};

function showResult(text){
    var div = document.getElementById('resultNote');
    var rainLength = document.getElementById('rainlength').value;
    var layers = map.getLayersBy("visibility", true);
    
    div.innerHTML = '<div align="center">Výsledek</div>';
    div.innerHTML += '<table><tr><td>GPS:</td><td>' + obsPoint.x.toFixed(5) + ', ' + obsPoint.y.toFixed(5) +
	'</td></tr><tr><td>Doba opakování:</td><td>' + layers[0].name +
	'</td></tr><tr><td>Délka návrhové srážky:</td><td>' + parseFloat(rainLength).toFixed(0) + ' (minuty)' +
	'</td></tr><tr><td>Hodnota návrhové srážky:</td><td><font color="red">' + parseFloat(text).toFixed(1) +
	'</font> (milimetry)</td></tr></table>';
};

/*
 *  ON DOM LOAD QUICKSTART EVERYTHING
 */

$(document).ready(function() {
    var switcher = new OpenLayers.Control.LayerSwitcher();
    
    var options = { projection: new OpenLayers.Projection('EPSG:4326'), 
                    units: 'm',
                    controls: [ new OpenLayers.Control.Navigation(),
                                new OpenLayers.Control.PanPanel(),
				switcher],
                  };
    
    map = new OpenLayers.Map('map1', options);
    switcher.maximizeControl();
    
    // base layer
    h002Layer = new OpenLayers.Layer.WMS("2 roky",
                                         "http://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_002", srs: "EPSG:4326"});
    h002Layer.title = "H_002";

    h005Layer = new OpenLayers.Layer.WMS("5 let",
                                         "http://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_010", srs: "EPSG:4326"});
    h005Layer.title = "H_005";

    h010Layer = new OpenLayers.Layer.WMS("10 let",
                                         "http://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_020", srs: "EPSG:4326"});
    h010Layer.title = "H_010";
    
    h020Layer = new OpenLayers.Layer.WMS("20 let",
                                         "http://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_020", srs: "EPSG:4326"});
    h020Layer.title = "H_020";
    
    h050Layer = new OpenLayers.Layer.WMS("50 let",
                                         "http://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_050", srs: "EPSG:4326"});
    h050Layer.title = "H_050";
    
    h100Layer = new OpenLayers.Layer.WMS("100 let",
                                         "http://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_100", srs: "EPSG:4326"});
    h100Layer.title = "H_100";

    // observation point layer
    obsLayer = new OpenLayers.Layer.Vector("Observační bod");
    obsPoint = new OpenLayers.Geometry.Point(15.474897, 49.803578);
    
    // style observation point map of obsLayer
    var vectorStyle= new OpenLayers.Style({externalGraphic:'${icon}', pointRadius: 15});
    obsLayer.styleMap = new OpenLayers.StyleMap({'default':vectorStyle}); 
    obsLayer.addFeatures([new OpenLayers.Feature.Vector(obsPoint, {icon: "./img/map-pointer.png"})]);
    
    // add everything to map
    map.addLayers([h002Layer, h005Layer, h010Layer, h020Layer, h050Layer, h100Layer, obsLayer]);
    map.setCenter(new OpenLayers.LonLat(15.474897, 49.803578), 8);
    
    // drag feature control here is where wps is called
    controlDrag = new OpenLayers.Control.DragFeature(obsLayer,
                                                     {onComplete: function(featureObj, pixelObj) {
	                                                 triggerGritter("Spouštím WPS proces");
	                                                 callWPS();
	                                             } // end function
	                                             } // end onComplete
	                                            ); //end controlDrag
    
    // add control to map 
    map.addControl(controlDrag);
    controlDrag.activate();
}); //end of document ready
