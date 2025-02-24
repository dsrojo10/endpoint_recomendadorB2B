import json
import sys
import pandas as pd
import joblib
import warnings
import base64
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

warnings.filterwarnings("ignore")
sys.stderr.write("LOG: Iniciando predecir.py...\n")
sys.stderr.flush()

# Cargar los modelos (asegúrate de que la ruta sea correcta)
sys.stderr.write("LOG: Cargando modelos en predecir.py...\n")
sys.stderr.flush()
modelos = {
    'PRODUCTO_SD_WAN': joblib.load(os.path.join(current_dir, 'modelo_PRODUCTO_SD_WAN.joblib')),
    'PRODUCTO_Comunicaciones_Unificadas': joblib.load(os.path.join(current_dir, 'modelo_PRODUCTO_Comunicaciones_Unificadas.joblib')),
    'PRODUCTO_Cloud': joblib.load(os.path.join(current_dir, 'modelo_PRODUCTO_Cloud.joblib')),
    'PRODUCTO_Ciberseguridad': joblib.load(os.path.join(current_dir, 'modelo_PRODUCTO_Ciberseguridad.joblib')),
    'PRODUCTO_Data_Center': joblib.load(os.path.join(current_dir, 'modelo_PRODUCTO_Data_Center.joblib'))
}
sys.stderr.write("LOG: Modelos cargados en predecir.py.\n")
sys.stderr.flush()

class ProductRecommender:
    def __init__(self):
        self.models = modelos  # Usa los modelos cargados globalmente
        self.feature_names = [
            'CLIENTE_ID',
            'SECTOR_Construcción, materiales y recursos naturales',
            'SECTOR_Desarrollo de software y Servicios de internet',
            'SECTOR_Educación',
            'SECTOR_Energía',
            'SECTOR_Manufactura',
            'SECTOR_Mayoristas y detal',
            'SECTOR_Media y entretenimiento',
            'SECTOR_Procesamiento de alimentos y bebidas',
            'SECTOR_Productos de consumo',
            'SECTOR_Productos farmaceuticos y médicos',
            'SECTOR_Promedio',
            'SECTOR_Proveedores de servicios de salud',
            'SECTOR_Quimicos',
            'SECTOR_Seguros',
            'SECTOR_Servicios Financieros y de Banca',
            'SECTOR_Servicios profesionales',
            'SECTOR_Telecomunicaciones',
            'SECTOR_Transporte',
            'GERENCIA_Empresas',
            'GERENCIA_Gobierno',
            'GERENCIA_Large',
            'GERENCIA_Medianas Low',
            'GERENCIA_Micro/Small',
            'GERENCIA_Multinacionales',
            'GERENCIA_Wholesale International',
            'GERENCIA_Wholesale Others',
            'SEDES_0',
            'SEDES_1 sede',
            'SEDES_100 o mas sedes',
            'SEDES_De 11 a 25 sedes',
            'SEDES_De 2 a 4 sedes',
            'SEDES_De 26 a 50 sedes',
            'SEDES_De 5 a 10 sedes',
            'SEDES_De 51 a 100 sedes',
            'SEDES_No registra',
            'EMPLEADOS_0',
            'EMPLEADOS_201500',
            'EMPLEADOS_De 11 a 50 empleados',
            'EMPLEADOS_De 2 a 10 empleados',
            'EMPLEADOS_De 201 a 500 empleados',
            'EMPLEADOS_De 51 a 200 empleados',
            'EMPLEADOS_Mayor a 500 empleados',
            'EMPLEADOS_No registra'
        ]

    def prepare_input(self, sector, gerencia, sedes, empleados):
        sector_mapping = {
            'telecomunicaciones': 'Telecomunicaciones',
            'software_internet': 'Desarrollo de software y Servicios de internet',
            'servicios_financieros': 'Servicios Financieros y de Banca',
            'construccion_materiales': 'Construcción, materiales y recursos naturales',
            'energia': 'Energía',
            'manufactura': 'Manufactura',
            'mayoristas_detal': 'Mayoristas y detal',
            'media_entretenimiento': 'Media y entretenimiento',
            'procesamiento_alimentos_bebidas': 'Procesamiento de alimentos y bebidas',
            'productos_consumo': 'Productos de consumo',
            'farmaceuticos_medicos': 'Productos farmaceuticos y médicos',
            'servicios_salud': 'Proveedores de servicios de salud',
            'quimicos': 'Quimicos',
            'seguros': 'Seguros',
            'servicios_profesionales': 'Servicios profesionales',
            'transporte': 'Transporte',
            'educacion': 'Educación'
        }

        gerencia_mapping = {
            'micro_small': 'Micro/Small',
            'medianas_low': 'Medianas Low',
            'large': 'Large',
            'empresas': 'Empresas',
            'gobierno': 'Gobierno',
            'multinacionales': 'Multinacionales',
            'wholesale_international': 'Wholesale International',
            'wholesale_others': 'Wholesale Others'
        }

        sedes_mapping = {
            '1_sede': '1 sede',
            '2_4_sedes': 'De 2 a 4 sedes',
            '5_10_sedes': 'De 5 a 10 sedes',
            '11_25_sedes': 'De 11 a 25 sedes',
            '26_50_sedes': 'De 26 a 50 sedes',
            '51_100_sedes': 'De 51 a 100 sedes',
            '100_mas_sedes': '100 o mas sedes',
            'no_registra': 'No registra'
        }

        empleados_mapping = {
            '2_10_empleados': 'De 2 a 10 empleados',
            '11_50_empleados': 'De 11 a 50 empleados',
            '51_200_empleados': 'De 51 a 200 empleados',
            '201_500_empleados': 'De 201 a 500 empleados',
            'mayor_500_empleados': 'Mayor a 500 empleados',
            'no_registra': 'No registra'
        }

        datos = {feature: [0] for feature in self.feature_names}
        datos['CLIENTE_ID'] = [999999]

        if sector and len(sector) > 0:
            mapped_sector = sector_mapping.get(sector[0])
            if mapped_sector:
                datos[f'SECTOR_{mapped_sector}'] = [1]

        if gerencia and len(gerencia) > 0:
            mapped_gerencia = gerencia_mapping.get(gerencia[0])
            if mapped_gerencia:
                datos[f'GERENCIA_{mapped_gerencia}'] = [1]

        if sedes and len(sedes) > 0:
            mapped_sedes = sedes_mapping.get(sedes[0])
            if mapped_sedes:
                datos[f'SEDES_{mapped_sedes}'] = [1]

        if empleados and len(empleados) > 0:
            mapped_empleados = empleados_mapping.get(empleados[0])
            if mapped_empleados:
                datos[f'EMPLEADOS_{mapped_empleados}'] = [1]

        return pd.DataFrame(datos)[self.feature_names]

    def get_recommendations(self, input_data):
        predictions = {}
        for product_name, model in self.models.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                probability = model.predict_proba(input_data)[0, 1]
                predictions[product_name] = probability
        return dict(sorted(predictions.items(), key=lambda x: x[1], reverse=True))

def main():
    try:
        warnings.filterwarnings('ignore')
        base64_data = sys.argv[1]
        sys.stderr.write("LOG: Recibiendo datos codificados.\n")
        sys.stderr.flush()
        json_data = base64.b64decode(base64_data).decode('utf-8')
        data = json.loads(json_data)
        sys.stderr.write("LOG: Datos decodificados y convertidos a JSON.\n")
        sys.stderr.flush()
        
        # Obtener arreglos directamente del objeto recibido
        sector = data.get("sector", [])
        gerencia = data.get("gerencia", [])
        sedes = data.get("sedes", [])
        empleados = data.get("empleados", [])
        
        sys.stderr.write("LOG: Preparando datos de entrada para la predicción.\n")
        sys.stderr.flush()
        recommender = ProductRecommender()
        input_data = recommender.prepare_input(sector, gerencia, sedes, empleados)
        
        sys.stderr.write("LOG: Ejecutando las predicciones...\n")
        sys.stderr.flush()
        recommendations = recommender.get_recommendations(input_data)
        
        # Convertir los valores a float nativo para poder serializar a JSON
        recommendations = {k: float(v) for k, v in recommendations.items()}
        
        sys.stderr.write("LOG: Predicciones generadas, enviando salida JSON.\n")
        sys.stderr.flush()
        print(json.dumps(recommendations))
        
        sys.exit(0)
        
    except Exception as e:
        sys.stderr.write("LOG: Error durante la ejecución: " + str(e) + "\n")
        sys.stderr.flush()
        sys.exit(1)

if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
