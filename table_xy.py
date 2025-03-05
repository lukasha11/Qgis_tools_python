from qgis.processing import alg
from qgis.core import QgsProcessing, QgsFields, QgsFeature, QgsField, QgsCoordinateTransform
from qgis.PyQt.QtCore import QVariant

@alg( name='table_xy', label='Dodaj pola XY', group = 'umcs',group_label='UMCS 2024/2025')

@alg.input( type = alg.SOURCE, name='SOURCE', label = 'Warstwa źródłowa', types =[QgsProcessing.TypeVectorPoint] )

@alg.input(type=alg.CRS, name='CRS', label='Układ współrzędnych', default = "EPSG:4326")

@alg.input( type = alg.SINK, name='TARGET', label = 'Warstwa docelowa' )


def table_xy(instance, parameters, context, feedback, inputs):
    """ Dodanie pól ze współrzednymi do tabeli atrybutów. """
    
    feedback.pushInfo(str(parameters))

    source = instance.parameterAsSource(parameters, 'SOURCE',context)
    crs = instance.parameterAsCrs(parameters, 'CRS', context)
    feedback.pushInfo(str(source))

    table = QgsFields( source.fields() )
    x_field = QgsField('X', QVariant.Double)
    y_field = QgsField('Y', QVariant.Double)
    table.append(x_field)
    table.append(y_field)
    sink, target_id = instance.parameterAsSink(parameters, 'TARGET',context,
        table,
        source.wkbType(),
        source.sourceCrs()

    )
    
    ct = QgsCoordinateTransform(source.sourceCrs(), crs, context.project())
    total = source.featureCount()
    for i, feature in enumerate(source.getFeatures()):
        if feedback.isCanceled():
            break

        new_feature = QgsFeature( table )
        
        geometry = feature.geometry()
        new_feature.setGeometry( geometry )
        
        attributes = feature.attributes()
        point = geometry.asPoint()
        point = ct.transform(point)
        attributes.append( point.x() )
        attributes.append( point.y() )
        new_feature.setAttributes( attributes )

        sink.addFeature( new_feature )

        progress = (i/total)*100
        feedback.setProgress( int(progress) )



    return {'TARGET': target_id}