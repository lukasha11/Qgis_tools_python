from qgis.processing import alg
from qgis.core import QgsProcessing, QgsFields, QgsFeature

@alg( name='filter_area', label='Filtrowanie poligonów wg powierzchni', group = 'umcs',group_label='UMCS 2024/2025')
@alg.input( type = alg.SOURCE, name='SOURCE', label = 'Warstwa źródłowa', types =[QgsProcessing.TypeVectorPolygon] )
@alg.input( type = alg.SINK, name='TARGET', label = 'Warstwa docelowa' )
@alg.input( type = alg.NUMBER, name='TOLERANCE', label = 'Minimalna powierzchnia', default = 1000 )

def filter_area(instance, parameters, context, feedback, inputs):
    """ Filtrowanie obiektów warstwy poligonowej wg ich powierzchni. """

    feedback.pushInfo(str(parameters))

    source = instance.parameterAsSource(parameters, 'SOURCE',context)
    feedback.pushInfo(str(source))
    
    tolerance = instance.parameterAsDouble(parameters, 'TOLERANCE', context) * 1000000
    
    table = QgsFields( source.fields() )
    sink, target_id = instance.parameterAsSink(parameters, 'TARGET',context,
        table,
        source.wkbType(),
        source.sourceCrs()

    )
    
    total = source.featureCount()
    for i, feature in enumerate(source.getFeatures()):
        if feedback.isCanceled():
            break
        
        new_feature = QgsFeature( table )

        attributes = feature.attributes()
        new_feature.setAttributes( attributes )

        geometry = feature.geometry()
        new_feature.setGeometry( geometry )
        
        if geometry.area() >= tolerance:
            sink.addFeature( new_feature )

        progress = (i/total)*100
        feedback.setProgress( int(progress) )



    return {'TARGET': target_id}