from qgis.processing import alg
from qgis.core import QgsProcessing, QgsFields, QgsFeature, QgsField
from qgis.PyQt.QtCore import QVariant

@alg( name='line_length', label='Długość linii', group = 'umcs',group_label='UMCS 2024/2025')
@alg.input( type = alg.SOURCE, name='SOURCE', label = 'Warstwa źródłowa', types =[QgsProcessing.TypeVectorLine] )
@alg.input( type = alg.SINK, name='TARGET', label = 'Warstwa docelowa' )
@alg.input( type = alg.STRING, name='FIELD NAME', label = 'Pole długości', default='length')

def line_length(instance, parameters, context, feedback, inputs):
    """ Wyliczanie długości linii. """

    feedback.pushInfo(str(parameters))

    source = instance.parameterAsSource(parameters, 'SOURCE',context)
    feedback.pushInfo(str(source))
    
    field_name = instance.parameterAsString(parameters, 'FIELD NAME', context)
    
    table = QgsFields( source.fields() )
    
    kolumna = QgsField(field_name, QVariant.Double)
    table.append(kolumna)
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

        geometry = feature.geometry()
        new_feature.setGeometry( geometry )
        
        attributes = feature.attributes()
        length = geometry.length()
        attributes.append(round(length, 2))
        new_feature.setAttributes( attributes )
        
        sink.addFeature( new_feature )

        progress = (i/total)*100
        feedback.setProgress( int(progress) )



    return {'TARGET': target_id}