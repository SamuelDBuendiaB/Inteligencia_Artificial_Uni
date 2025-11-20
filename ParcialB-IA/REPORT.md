# Proyecto B – Clasificación de imágenes

## Resumen ejecutivo
Se desarrolló una solución de clasificación multiclase a partir de imágenes asociadas al dataset `train.csv`. El flujo completo incluye: carga y preprocesamiento de imágenes (redimensionadas a 128×128 y normalizadas), reducción de dimensionalidad mediante PCA y entrenamiento de tres modelos: `RandomForestClassifier`, `GradientBoostingClassifier` y una red neuronal en TensorFlow/Keras. El desempeño final se reporta en el notebook `notebook_clasificacion.ipynb`, donde se registran métricas de accuracy, matrices de confusión y reportes de clasificación sobre los conjuntos de validación y prueba.

## Datos y preprocesamiento
- **Fuente**: `train.csv` contiene las columnas de identificación (`id`/`image_id`) y etiqueta (`species`/`label`), además de descriptores tabulares que se usaron sólo para verificación.
- **Imágenes**: localizadas en `images/`, se cargan con TensorFlow (`tf.io.read_file` + `tf.image.decode_image`), se redimensionan a 128×128 px y se escalan a `[0,1]`.
- **Etiquetas**: codificadas con `LabelEncoder`.
- **División**: 70 % entrenamiento, 15 % validación y 15 % prueba, estratificando por clase para preservar el balance.

## Reducción de dimensionalidad (PCA)
Trabajar directamente con los vectores de pixeles genera 49 152 características por imagen (128×128×3). Para reducir complejidad y ruido se aplicó `sklearn.decomposition.PCA` conservando 95 % de la varianza:

- **Ventajas**:
  - Reduce drásticamente la dimensionalidad, acelerando el entrenamiento de los modelos clásicos.
  - Atenúa ruido y correlaciones redundantes entre pixeles.
  - Facilita la visualización de la varianza explicada e identifica la cantidad mínima de componentes útiles.
- Las componentes principales transformadas (`X_train_pca`, etc.) se usaron como entrada para Random Forest, Gradient Boosting y la red neuronal.

## Modelos entrenados y resultados
| Modelo | Entrenamiento | Detalles clave | Métricas reportadas |
| --- | --- | --- | --- |
| RandomForestClassifier | `sklearn.ensemble` | 100 árboles, profundidad máx. 20, `random_state=42`. | Accuracy en train/val/test, matriz de confusión, reporte de clasificación. |
| GradientBoostingClassifier | `sklearn.ensemble` | 100 estimadores, profundidad 5, `learning_rate=0.1`. | Igual conjunto de métricas. |
| Red neuronal (Keras) | Dense 256-128-64 + Dropout | Optimizer Adam, `categorical_crossentropy`, 50 épocas, batch 32. | Curvas de entrenamiento, accuracy y reporte en test. |

Los resultados detallados (tablas, matrices y clasification reports) se generan al ejecutar las celdas 6–11 del notebook. Además, se guardan en `resultados_clasificacion.csv`.

## Conclusiones y recomendaciones
1. **PCA habilita modelos clásicos eficientes**: sin reducción, el costo computacional sería prohibitivo. Mantener 95 % de varianza conservó el poder predictivo con menos componentes.
2. **Comparación de modelos**: Random Forest ofrece robustez y facilidad de interpretación (importancias), Gradient Boosting suele capturar mejor patrones complejos, y la red neuronal permite explotar relaciones no lineales profundas. Escoger el modelo final depende del mejor balance accuracy/tiempo observado tras ejecutar el notebook.
3. **Pipeline reproducible**: el notebook integra todo el flujo (EDA, preprocesamiento, PCA, entrenamiento, evaluación y guardado de resultados) con semillas fijas.
4. **Próximos pasos**:
   - Ajustar hiperparámetros (Grid/Random Search) para cada modelo.
   - Considerar data augmentation si se detecta sobreajuste o desbalance severo.
   - Exportar el mejor modelo (ej. con `joblib` o `SavedModel`) para despliegue.

Con la ejecución completa del notebook y el análisis consolidado en este reporte, el proyecto queda listo para su entrega y posterior ampliación.

