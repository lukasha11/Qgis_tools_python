from qgis.processing import alg
from qgis.core import QgsProcessing, QgsFields, QgsFeature, QgsField, Qgis, QgsCoordinateTransform
from qgis.PyQt.QtCore import QVariant

@alg( name='raster', label='Zapis wartości rastra w punktach', group = 'umcs',group_label='UMCS 2024/2025')

@alg.input( type = alg.SOURCE, name='SOURCE', label = 'Warstwa źródłowa', types =[QgsProcessing.TypeVectorPoint] )

@alg.input( type = alg.RASTER_LAYER, name='RASTER', label = 'Warstwa rastrowa')

@alg.input( type = alg.SINK, name='TARGET', label = 'Warstwa docelowa' )


def raster(instance, parameters, context, feedback, inputs):
    """ Zapis wartości rastrów do obiektów wartstwy punktowej. """

    feedback.pushInfo(str(parameters))

    source = instance.parameterAsSource(parameters, 'SOURCE',context)
    raster = instance.parameterAsRasterLayer(parameters, 'RASTER', context)

    table = QgsFields( source.fields() )
    
    for band in range (raster.bandCount()):
        name = 'band_{}'.format(band+1)
        field = QgsField(name, QVariant.Double)
        table.append(field)
        
    sink, target_id = instance.parameterAsSink(parameters, 'TARGET',context,
        table,
        source.wkbType(),
        source.sourceCrs()

    )
    
    total = source.featureCount()
    dp = raster.dataProvider()
    ct = QgsCoordinateTransform(source.sourceCrs(),raster.crs(), context.project())
    for i, feature in enumerate(source.getFeatures()):
        if feedback.isCanceled():
            break

        new_feature = QgsFeature( table )

        attributes = feature.attributes()

        geometry = feature.geometry()
        new_feature.setGeometry( geometry )

        point = geometry.asPoint()
        point = ct.transform(point)
        values = dp.identify(point, Qgis.RasterIdentifyFormat.IdentifyFormatValue)
        values = values.results()
        
        for band in range (raster.bandCount()):
            value = values.get(band+1)
            attributes.append(value)
        
        new_feature.setAttributes( attributes )

        sink.addFeature( new_feature )

        progress = (i/total)*100
        feedback.setProgress( int(progress) )



    return {'TARGET': target_id}