from qgis.processing import alg
from qgis.core import QgsProcessing, QgsFields, QgsFeature

@alg( name='copy_layer', label='Kopiowanie warstwy', group = 'umcs',group_label='UMCS 2024/2025')

@alg.input( type = alg.SOURCE, name='SOURCE', label = 'Warstwa źródłowa', types =[QgsProcessing.TypeVector] )

@alg.input( type = alg.SINK, name='TARGET', label = 'Warstwa docelowa' )


def copy_layer(instance, parameters, context, feedback, inputs):
    """ Kopiowanie warstw wektorowych. """

    feedback.pushInfo(str(parameters))

    source = instance.parameterAsSource(parameters, 'SOURCE',context)

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

        sink.addFeature( new_feature )

        progress = (i/total)*100
        feedback.setProgress( int(progress) )



    return {'TARGET': target_id}