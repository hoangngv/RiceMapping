var export2drive = function (img, folder, scale, id, shape, maxPixels){
  Export.image.toDrive({
        image:img,
        description: img.id().getInfo(),
        folder: folder,
        fileNamePrefix: id + '_' + img.id().getInfo(),
        region: shape.geometry().bounds(),
        scale: scale,
        crs: 'EPSG:4326',
        maxPixels: maxPixels})
}
function maskS2clouds(image) {
  var qa = image.select('QA60');

  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));

  return image.updateMask(mask).divide(10000);
}

function get_dataset(date1, date2, shape) {
  var dataset = ee.ImageCollection('COPERNICUS/S2')
                  .filterDate(date1, date2)
                  .filterBounds(shape)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 90))
                  .map(maskS2clouds);
  var dataset_clip = dataset.map(function (image) {return image.clip(shape)})
  var ndvi = dataset_clip.map(function (image) {
    var nir = image.select('B8');
    var red = image.select('B4')
    return nir.subtract(red).divide(nir.add(red)).rename('NDVI');
  });

  return ndvi.mean();
}

var dbsh = ee.FeatureCollection('users/nvhoang191/DBSH_Shape10');

var list_date = ['2018-2-1',
                  '2018-2-15',
                  '2018-2-28',
                  '2018-3-15',
                  '2018-3-31',
                  '2018-4-15',
                  '2018-4-30',
                  '2018-5-15',
                  '2018-5-31'];

var ndviParams = {min: -1, max: 1, palette: ['blue', 'white', 'green']};

Map.addLayer(dbsh);

//mosaicking and downloading
for (var i = 0; i < list_date.length - 1 ; i++) {
  var img = get_dataset(list_date[i], list_date[i+1], dbsh);
  var id = list_date[i] + "-" + list_date[i+1]
  Map.addLayer(img.select('NDVI'), ndviParams, id);
  export2drive(img.select('NDVI'), "Sentinel2", 10, id, dbsh, 10000000000000)
}