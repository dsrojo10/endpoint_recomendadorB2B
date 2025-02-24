# Proyecto ML NodeJS 🚀

Este proyecto implementa un endpoint en Node.js que invoca scripts en Python para cargar modelos y realizar predicciones basadas en datos de entrada. El servidor se inicia con `npm start` y está preparado para recibir peticiones POST en el endpoint `/prediccion`.

---

## Autor 🧑‍💻

Desarrollado por **dsrojo**.

---

## Requisitos 🔧

### Node.js 💻
- Instalar [Node.js](https://nodejs.org/) (versión 12 o superior recomendada).

### Python 🐍
- Tener instalado Python (preferiblemente Python 3).
- Instalar las siguientes librerías de Python:
  - `joblib`
  - `pandas`
  - `scikit-learn` (u otra dependencia necesaria para la generación y carga de modelos)
- Puedes instalarlas mediante:
  ```bash
  pip install joblib pandas scikit-learn
  ```

---

## Instalación 🛠️

1. **Clona o descarga el repositorio:**  
   Clona el repositorio o descarga el código fuente en tu máquina.

2. **Abre una terminal en la carpeta raíz del proyecto:**  
   Navega hasta la carpeta donde se encuentra el proyecto.

3. **Instala las dependencias de Node.js:**  
   ```bash
   npm install
   ```

4. **Verifica la estructura de archivos:**  
   Asegúrate de que en la carpeta `modelos` se encuentren los siguientes archivos:
   - `cargar_modelos.py`
   - `predecir.py`
   - `modelos.js`
   - Los archivos de modelos entrenados, por ejemplo:
     - `modelo_PRODUCTO_SD_WAN.joblib`
     - `modelo_PRODUCTO_Comunicaciones_Unificadas.joblib`
     - `modelo_PRODUCTO_Cloud.joblib`
     - `modelo_PRODUCTO_Ciberseguridad.joblib`
     - `modelo_PRODUCTO_Data_Center.joblib`

---

## Estructura del Proyecto 📁

```
ML_nodejs/
├── error.log
├── package.json
├── package-lock.json
├── peticion.txt
├── servidor.js
└── modelos/
    ├── cargar_modelos.py
    ├── modelos.js
    ├── predecir.py
    ├── modelo_PRODUCTO_SD_WAN.joblib
    ├── modelo_PRODUCTO_Comunicaciones_Unificadas.joblib
    ├── modelo_PRODUCTO_Cloud.joblib
    ├── modelo_PRODUCTO_Ciberseguridad.joblib
    └── modelo_PRODUCTO_Data_Center.joblib
```

- **servidor.js:** Archivo principal del servidor Node.js.  
- **modelos/modelos.js:** Contiene la lógica para cargar los modelos y realizar las predicciones invocando scripts Python.  
- **modelos/cargar_modelos.py:** Script Python que carga los modelos y devuelve una representación serializada.  
- **modelos/predecir.py:** Script Python que recibe datos codificados en base64, prepara la entrada, realiza la predicción y retorna el resultado en JSON.  
- **Archivos .joblib:** Archivos con los modelos previamente entrenados.

---

## Ejecución ⚡

Para iniciar el servidor, desde la raíz del proyecto ejecuta:
```bash
npm start
```

El servidor se iniciará en el puerto 3000 y cargará los modelos. La salida en consola mostrará mensajes de log tanto del lado Node.js como Python.

---

## Uso 🔍

Para realizar una predicción, envía una petición POST a:
```
http://localhost:3000/prediccion
```

### Ejemplo de petición usando PowerShell

```powershell
$body = @{
    sector = @("telecomunicaciones")
    gerencia = @("micro_small")
    sedes = @("1_sede")
    empleados = @("2_10_empleados")
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Headers @{ "Content-Type" = "application/json" } -Body $body -Uri http://localhost:3000/prediccion
```

La respuesta será un objeto JSON con las probabilidades de recomendación para cada producto.

---

## Notas Adicionales 📝

- **Logs:** Se han añadido mensajes de log en ambos lados (Node.js y Python) para facilitar la depuración. Estos se muestran en la consola.
- **Base64:** El JSON enviado al script Python se codifica en base64 desde Node.js para que el script pueda decodificarlo y procesarlo correctamente.
- **Serialización:** Se convierten a tipo `float` nativo los valores de predicción para garantizar la correcta serialización a JSON.
- **PowerShell:** Se recomienda utilizar `Invoke-RestMethod` para evitar errores al convertir objetos con claves duplicadas.

---
