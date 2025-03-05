from qgis.processing import alg
from qgis.core import QgsProcessing, QgsFields, QgsFeature, Qgis

@alg( name='buffer', label='Bufor', group='umcs', group_label='UMCS 2024/2025')
@alg.input( type=alg.SOURCE, name='SOURCE', label='Warstwa źródłowa', types=[QgsProcessing.TypeVectorAnyGeometry])
@alg.input( type=alg.NUMBER, name='DISTANCE', label='Odległość', default = 1000)
@alg.input( type=alg.INT, name='SEGMENTS', label='Odcinki', default = 5, minValue=1)
@alg.input( type=alg.SINK, name='TARGET', label='Warstwa docelowa' )
def buffer(instance, parameters, context, feedback, inputs):
    """ Generowanie otoczki powierzchniowej. """
    
    source = instance.parameterAsSource(parameters, 'SOURCE', context)
    
    distance = instance.parameterAsDouble(parameters, 'DISTANCE', context)
    segments = instance.parameterAsInt(parameters, 'SEGMENTS', context)
    
    feedback.pushInfo(str(source))
    
    table = QgsFields(source.fields())
    sink, target_id = instance.parameterAsSink(parameters, 'TARGET', context,
        table, 
        Qgis.WkbType.Polygon, 
        source.sourceCrs()
        )
    
    total = source.featureCount()
    for i, feature in enumerate(source.getFeatures()):
        if feedback.isCanceled():
            break
        
        new_feature = QgsFeature(table)
        
        attributes = feature.attributes()
        new_feature.setAttributes(attributes)
        
        geometry = feature.geometry()
        buffer = geometry.buffer(distance, segments)
        new_feature.setGeometry(buffer)
        
        sink.addFeature(new_feature)
        
        progress = (i/total)*100
        feedback.setProgress(int(progress))
        
    return {'TARGET': target_id}