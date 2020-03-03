var mosaic_image = function (col, channel, folder, resolution, shape) {
  /**
  Input:
    col: Image collection
    channel: VV/VH
    folder: drive folder
    resolution: S1A - 10m, LS8 - 30m
    shape: boundary shapefile cua DBSH
  **/
  var maxPixels = 10000000000000;
  var colList = col.toList(500);
  var col_length = colList.size().getInfo();
  
  var mosaic = ee.Image();
  var img1 = ee.Image();
  var img2 = ee.Image();

  for (var i = 0; i < col_length - 1 ; i = i+2) {// Anh Sentinel 1A can 2 anh de cover het DBSH

    img1 = ee.Image(colList.get(i));
    img2 = ee.Image(colList.get(i+1));

    var id = img1.id().getInfo();
    mosaic = ee.ImageCollection.fromImages([img1, img2]).mosaic().select(channel);

    console.log(mosaic);
    Map.addLayer(mosaic,{bands: [channel]}, id);
    export2drive(mosaic.clip(shape), folder, resolution, id, shape, maxPixels);

  }
}

var export2drive = function (img, folder, scale, id, shape, maxPixels){
  Export.image.toDrive({
        image:img,
        description: id,
        folder: folder,
        fileNamePrefix: id,
        region: shape.geometry().bounds(),
        scale: scale,
        crs: 'EPSG:4326',
        maxPixels: maxPixels})
}

//main
var img = ee.ImageCollection('COPERNICUS/S1_GRD');
var sentinel = img.filterDate('2018-2-1', '2018-5-30')// Download anh tu 1/2/2018 den 30/5/2018
                    .filterBounds(shape) // Loc anh ve khu vuc ĐBSH
                    .filter(ee.Filter.eq('relativeOrbitNumber_start', 91));

var sentinel_clip = sentinel.map(function(image) {return image.clip(shape);});// Cat anh ve khu vực ĐBSH
console.log(sentinel_clip);

var vv = 'VV';
var vh = 'VV';
var folder = "Sentinel-1A"; // Tao folder Sentinel-1A tren drive
//var shape = ee.FeatureCollection("users/hoangle12298/DBSH_Shape"); // Doan nay import shapefile cua DBSH

mosaic_image(sentinel_clip, vv, folder, 10, shape); // Xong VV thi chay cho VH cho de kiem soat anh do id anh trung nhau
Map.addLayer(shape, {color: 'FF0000'}, 'DBSH');
