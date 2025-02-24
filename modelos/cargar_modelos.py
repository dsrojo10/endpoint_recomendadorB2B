import joblib
import json
import warnings
import os
import sys

warnings.filterwarnings("ignore")

try:
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    modelos = {}
    productos = [
        'PRODUCTO_SD_WAN',
        'PRODUCTO_Comunicaciones_Unificadas',
        'PRODUCTO_Cloud',
        'PRODUCTO_Ciberseguridad',
        'PRODUCTO_Data_Center'
    ]

    for producto in productos:
        modelo_path = os.path.join(current_dir, f"modelo_{producto}.joblib")
        modelos[producto] = joblib.load(modelo_path)

    # Convertir los modelos a una representación serializable
    modelos_serializables = {k: "loaded" for k in modelos.keys()}
    print(json.dumps(modelos_serializables))

except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    sys.exit(1)