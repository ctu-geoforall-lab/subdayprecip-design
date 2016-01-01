// GLOBAL VARIABLES
var map, wpsObj, urlWPS, obsPoint;

// URLs change according to needs
var urlWPS="http://rain1.fsv.cvut.cz/services/wps";

// OPTION GRITTER
$.extend($.gritter.options,{position:'bottom-right',fade_in_speed:'medium',fade_out_speed:2000,time:2000});

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
    var raster = new OpenLayers.WPS.LiteralPut({
        identifier : "raster",
        value: "H_002" 
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
    
    div.innerHTML = '<div align="center">Výsledek</div>';
    div.innerHTML += '<table>' + '<tr><td>GPS:</td><td>' + obsPoint.x.toFixed(5) + ', ' + obsPoint.y.toFixed(5) + 
    '</td></tr><tr><td>Délka návrhové srážky:</td><td>' + parseFloat(rainLength).toFixed(0) + 
    '</td></tr><tr><td>Hodnota návrhové srážky:</td><td>' + parseFloat(text).toFixed(1) + '</td></tr>' +  '</table>';
};

/*
 *  ON DOM LOAD QUICKSTART EVERYTHING
 */

$(document).ready(function() {
    var options = { projection: new OpenLayers.Projection('EPSG:4326'), 
                    units: 'm',
                    controls: [ new OpenLayers.Control.Navigation(),
                                new OpenLayers.Control.PanPanel() ],
                  };

    map = new OpenLayers.Map('map1', options);

    // base layer
    gphyLayer = new OpenLayers.Layer.WMS("H_002",
                                         "http://rain1.fsv.cvut.cz/services/wms",
                                         {layers: "H_002", srs: "EPSG:4326"});

    // observation point layer
    obsLayer = new OpenLayers.Layer.Vector("Observation Point");
    obsPoint = new OpenLayers.Geometry.Point(15.474897, 49.803578);
    
    // style observation point map of obsLayer
    var vectorStyle= new OpenLayers.Style({externalGraphic:'${icon}', pointRadius: 15});
    obsLayer.styleMap = new OpenLayers.StyleMap({'default':vectorStyle}); 
    obsLayer.addFeatures([new OpenLayers.Feature.Vector(obsPoint, {icon: "./img/map-pointer.png"})]);
    
    // add everything to map
    map.addLayers([gphyLayer, obsLayer]);
    map.setCenter(new OpenLayers.LonLat(15.474897, 49.803578), 8);
    
    // drag feature control here is where wps is called !!!!
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
