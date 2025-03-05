from qgis.processing import alg
from qgis.core import QgsProcessing, QgsFields, QgsFeature, Qgis

@alg( name='centroids', label='Centroidy', group='umcs', group_label='UMCS 2024/2025')
@alg.input( type=alg.SOURCE, name='SOURCE', label='Warstwa źródłowa', types=[QgsProcessing.TypeVectorAnyGeometry])
@alg.input( type=alg.SINK, name='TARGET', label='Warstwa docelowa' )
def centroids(instance, parameters, context, feedback, inputs):
    """ Tworzenie centroidów wektorowych warstw przestrzennych. """
    
    source = instance.parameterAsSource(parameters, 'SOURCE', context)
    feedback.pushInfo(str(source))
    
    table = QgsFields(source.fields())
    sink, target_id = instance.parameterAsSink(parameters, 'TARGET', context,
        table, 
        Qgis.WkbType.Point, 
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
        centroid = geometry.centroid()
        new_feature.setGeometry(centroid)
        
        sink.addFeature(new_feature)
        
        progress = (i/total)*100
        feedback.setProgress(int(progress))
        
    return {'TARGET': target_id}