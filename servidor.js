const express = require('express');
const app = express();
const port = 3000;
const { cargarModelos, realizarPrediccion } = require('./modelos/modelos');

app.use(express.json());

cargarModelos((err) => {
  if (err) {
    console.error('Error al cargar modelos:', err);
    process.exit(1);
  } else {
    console.log('Modelos cargados correctamente.');
  }
});

app.post('/prediccion', (req, res) => {
  const datos = req.body;

  realizarPrediccion(datos)
    .then(predicciones => {
      console.log("==========================");
      console.log("📊 Datos de la empresa recibidos:");
      console.log(datos);
      console.log("==========================");
      console.log("🔮 Recomendación generada:");
      console.log(predicciones);
      console.log("==========================");
      res.json(predicciones);
    })
    .catch(error => {
      console.error('❌ Error en la predicción:', error);
      res.status(500).json({ error: 'Error en la predicción' });
    });
});

app.listen(port, () => {
  console.log(`Servidor escuchando en el puerto ${port}`);
});
