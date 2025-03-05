from qgis.processing import alg
from qgis.core import QgsProcessing, QgsFields, QgsFeature, QgsCoordinateTransform

@alg( name='transform', label='Zmiana układu współrzędnych', group='umcs', group_label='UMCS 2024/2025')
@alg.input(type=alg.SOURCE, name='SOURCE', label='Warstwa źródłowa', types=[QgsProcessing.TypeVectorAnyGeometry])
@alg.input(type=alg.CRS, name='CRS', label='Docelowy układ współrzędnych', default = "EPSG:4326")
@alg.input(type=alg.SINK, name='TARGET', label='Warstwa docelowa')
def transform(instance, parameters, context, feedback, inputs):
    """ Transformacja warstwy do innego układu współrzędnych. """
    
    source = instance.parameterAsSource(parameters, 'SOURCE', context)
    crs = instance.parameterAsCrs(parameters, 'CRS', context)
    
    table = QgsFields(source.fields())
    sink, target_id = instance.parameterAsSink(parameters, 'TARGET', context,
        table, 
        source.wkbType(),
        crs
        )
        
    ct = QgsCoordinateTransform(source.sourceCrs(), crs, context.project())
    total = source.featureCount()
    for i, feature in enumerate(source.getFeatures()):
        if feedback.isCanceled():
            break
        
        new_feature = QgsFeature(table)
        
        attributes = feature.attributes()
        new_feature.setAttributes(attributes)
        
        geometry = feature.geometry()
        geometry.transform(ct)
        new_feature.setGeometry(geometry)
        
        sink.addFeature(new_feature)
        
        progress = (i/total)*100
        feedback.setProgress(int(progress))
        
    return {'TARGET': target_id}