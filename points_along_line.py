from qgis.processing import alg
from qgis.core import QgsProcessing, QgsFields, QgsFeature, QgsField, Qgis
from qgis.PyQt.QtCore import QVariant

@alg( name='points_along_line', label='Interpolacja punktów wzdłuż linii', group = 'umcs',group_label='UMCS 2024/2025')

@alg.input( type = alg.SOURCE, name='SOURCE', label = 'Warstwa źródłowa', types =[QgsProcessing.TypeVectorLine] )
@alg.input( type = alg.NUMBER, name = 'DISTANCE', label = 'Odległość między punktami', default = 10000, minValue = 0.01)
@alg.input( type = alg.SINK, name='TARGET', label = 'Warstwa docelowa')


def points_along_line(instance, parameters, context, feedback, inputs):
    """Interpolacja punktów wzdłuż linii. """

    feedback.pushInfo(str(parameters))

    source = instance.parameterAsSource(parameters, 'SOURCE',context)
    distance = instance.parameterAsDouble(parameters, 'DISTANCE', context)

    table = QgsFields()
    line_field = QgsField('Line ID', QVariant.Int)
    distance_field = QgsField('Distance', QVariant.Double, prec=2)
    table.append(line_field)
    table.append(distance_field)
    sink, target_id = instance.parameterAsSink(parameters, 'TARGET',context,
        table,
        Qgis.WkbType.Point,
        source.sourceCrs()
        
    )

    total = source.featureCount()
    for i, feature in enumerate(source.getFeatures()):
        if feedback.isCanceled():
            break

        geometry = feature.geometry()
        from_start = 0
        
        while from_start <= geometry.length():
        
            new_feature = QgsFeature( table )
            
            point = geometry.interpolate(from_start)
            new_feature.setGeometry( point )
            
            new_feature[line_field.name()] = feature.id()
            new_feature[distance_field.name()] = from_start

            sink.addFeature( new_feature )
            
            from_start += distance

        progress = (i/total)*100
        feedback.setProgress( int(progress) )



    return {'TARGET': target_id}