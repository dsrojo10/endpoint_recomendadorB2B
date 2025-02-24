const { spawn } = require('child_process');
const fs = require('fs');

let modelos = {};

function cargarModelos(callback) {
  const scriptPath = './modelos/cargar_modelos.py';
  const errorFile = './error.log';

  const pythonProcess = spawn('python', [scriptPath]);

  pythonProcess.stdout.on('data', (data) => {
    try {
      const modelosCargados = JSON.parse(data.toString());
      modelos = modelosCargados;
      callback(null);
    } catch (error) {
      callback(error);
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    fs.appendFile(errorFile, data, (err) => {
      if (err) {
        console.error('Error al escribir en el archivo de error:', err);
      }
    });
    console.error(`Error al cargar modelos (stderr - ver error.log): ${data.toString()}`);
    callback(new Error(data));
  });
}

function realizarPrediccion(datos) {
  return new Promise((resolve, reject) => {
    const scriptPath = './modelos/predecir.py';
    // Codificar el JSON a base64 antes de enviarlo
    const base64Data = Buffer.from(JSON.stringify(datos)).toString('base64');
    const pythonProcess = spawn('python', [scriptPath, base64Data]);

    let stdoutData = "";
    pythonProcess.stdout.on('data', (data) => {
      stdoutData += data.toString();
    });

    pythonProcess.stdout.on('end', () => {
      try {
        const predicciones = JSON.parse(stdoutData);
        resolve(predicciones);
      } catch (error) {
        reject(error);
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      const str = data.toString();
      // Si el mensaje es solo un log, lo mostramos y no rechazamos la promesa
      if (str.startsWith("LOG:")) {
         console.log("Python Log:", str);
      } else {
         reject(new Error(str));
      }
    });

    pythonProcess.on('close', (code) => {
      console.log(`Proceso Python cerrado con código ${code}`);
    });
  });
}

module.exports = { cargarModelos, realizarPrediccion };
