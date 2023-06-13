# Sistema Recomendador de Peliculas

***

## Descripción

El repositorio presente usa el dataset presente en el [presente link](https://drive.google.com/drive/folders/1cNdrsWSsz-TVTrSJg3hZmnhnhymcbJ6U?usp=sharing) para crear una API desarrollada con FASTAPI que entrega 7 endpoints distintos, siendo el último basado en un modelo de ML encargado de recomendar peliculas teniendo en cuenta la similitud del coseno.

## Distribución del Proyecto

El proyecto usa dos entornos virtuales para su desarrollo, siendo el primero para el archivo main.py, el cual es el encargado de desplegar la API, y el segundo para los jupyter notebooks en los que ocurren procesos de ETL, EDA y ML.

A continuación se presenta una breve descripción de cada archivo .py o .ipynb:

- **transform_data.ipynb:** Es el archivo encargado de hacer ETL, usa el dataset presentado anteriormente y retorna una tabla principal movies.csv y otras tablas producto de columnas anidadas en el dataset original.

- **EDA.ipynb:** Aquí se realiza un breve analisís exploratorio de los datos y se ven algunas gráficas al respecto.

- **recommender_system.ipynb:** Archivo encargado de preprocesar los datos para la creación de un modelo basado en la similitud del coseno.

- **main.py:** Archivo donde se despliega la API. Aquí se encuentran todos los endpoints y un objeto FastApi.

*Para ejecutar correctamente los archivos puede seguir instalar las librerias descritas en "requirements.txt" o "ipynb_requirements.txt."*

## Tecnologías Utilizadas

El proyecto hace uso de las siguientes tecnologías:

- **Python:** Se utiliza como lenguaje principal de programación. Se emplean diversas librerías, descritas en "requirements.txt".

- **Jupyter Notebook:** Se utiliza para desarrollar y presentar el proyecto. Los análisis, visualizaciones y conclusiones se presentan en forma de cuadernos interactivos. Se emplean diversas librerías, descritas en "ipynb_requirements.txt".

- **FastAPI:** Se utiliza como framework de desarrollo web para construir una API que permita el acceso y la interacción con los datos analizados. 

- **Render:** Se utiliza para desplegar la interfaz web y la API de forma sencilla y escalable.

