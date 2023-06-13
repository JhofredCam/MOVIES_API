import pandas as pd
from fastapi import FastAPI
import ast

# http://127.0.0.1:8000/

app = FastAPI()

movies = pd.read_csv("movies.csv")
recommendations = pd.read_csv('recommendations.csv')


@app.get("/cantidad_filmaciones_mes/{month}")
def cantidad_filmaciones_mes(month:str) -> dict:
    """
    Devuelve la cantidad de películas estrenadas en un mes específico.

    Parámetros:
    - month (str): El mes para el cual se desea obtener la cantidad de películas estrenadas.

    Retorna:
    Un diccionario que indica la cantidad de películas estrenadas en el mes especificado.

    """
    
    month = month.capitalize()

    months = {
    'Enero': 1,
    'Febrero': 2,
    'Marzo': 3,
    'Abril': 4,
    'Mayo': 5,
    'Junio': 6,
    'Julio': 7,
    'Agosto': 8,
    'Septiembre': 9,
    'Octubre': 10,
    'Noviembre': 11,
    'Diciembre': 12
    }
    
    # Obtener el recuento de películas estrenadas en el mes proporcionado
    num_movies = movies['release_month'].value_counts().loc[months[month]]

    return {'mes':month,'cantidad':int(num_movies)}


@app.get("/cantidad_filmaciones_dia/{day}")
def cantidad_filmaciones_dia(day:str) -> dict:
    """
    Devuelve la cantidad de películas estrenadas en un día específico.

    Parámetros:
    - day (str): El día para el cual se desea obtener la cantidad de películas estrenadas.

    Retorna:
    Un diccionario que indica la cantidad de películas estrenadas en el día especificado.

    """

    day = day.lower()
    
    days = {
        'uno': 1,
        'dos': 2,
        'tres': 3,
        'cuatro': 4,
        'cinco': 5,
        'seis': 6,
        'siete': 7,
        'ocho': 8,
        'nueve': 9,
        'diez': 10,
        'once': 11,
        'doce': 12,
        'trece': 13,
        'catorce': 14,
        'quince': 15,
        'dieciseis': 16,
        'diecisiete': 17,
        'dieciocho': 18,
        'diecinueve': 19,
        'veinte': 20,
        'veintiuno': 21,
        'veintidos': 22,
        'veintitres': 23,
        'veinticuatro': 24,
        'veinticinco': 25,
        'veintiseis': 26,
        'veintisiete': 27,
        'veintiocho': 28,
        'veintinueve': 29,
        'treinta': 30,
        'treinta y uno': 31
    }
    
    # Obtener el recuento de películas estrenadas en el dia proporcionado
    num_movies = movies['release_day'].value_counts().loc[days[day]]

    return {'dia':day,'cantidad':int(num_movies)}


@app.get("/score_titulo/{title}")
def score_titulo(title: str) -> dict:
    """
    Devuelve la información del título, año de estreno y puntaje de una película específica.

    Parámetros:
    - title (str): El título de la película para la cual se desea obtener la información.

    Retorna:
    Un diccionario que muestra el título de la película, su año de estreno y su puntaje/popularidad.

    """

    title = title.title()

    # Obtener la película con el título proporcionado
    movie = movies[movies['title'] == title].iloc[0, :]

    # Seleccionar las columnas relevantes: título, año de estreno y puntaje
    movie = movie[['title', 'release_year', 'popularity','vote_average']]

    return {'titulo':movie['title'], 'anio':int(movie['release_year']), 'popularidad':round(movie['popularity'],2)}

@app.get("/votos_titulo/{title}")
def votos_titulo(title: str):
    """
    Devuelve información sobre el número de votos y el puntaje promedio de una película específica.

    Parámetros:
    - title (str): El título de la película para la cual se desea obtener la información.

    Retorna:
    Un diccionario que muestra el título de la película, su año de estreno, el número de votos y el puntaje promedio.
    O una cadena de texto indicando que no cumple la condición de 2000 valoraciones o más.

    """

    title = title.title()


    # Obtener la película con el título proporcionado
    movie = movies[movies['title'] == title].iloc[0, :]

    # Verificar si la película tiene 2000 votos o más
    if movie['vote_count'] >= 2000:
        return {'titulo':movie['title'], 'anio':int(movie['release_year']), 'voto_total':int(movie['vote_count']), 'voto_promedio':round(movie['vote_average'],2)}    
    else:
        # Devolver un mensaje indicando que la película no cumple con el criterio de votos mínimos
        return "La película no contiene 2000 valoraciones o más, por lo que no se devuelve ningún valor"
    

@app.get("/get_actor/{actor}")
def get_actor(actor: str) -> dict:
    """
    Devuelve información sobre las filmaciones en las que un actor específico ha participado.

    Parámetros:
    - actor (str): El nombre del actor para el cual se desea obtener la información.

    Retorna:
    Un diccionario que muestra el nombre del actor, el número de filmaciones en las que ha participado,
    el retorno total obtenido y el retorno promedio por filmación.

    """
    def str_eval(x):
        """
        Evalúa una cadena de texto y devuelve el resultado correspondiente.

        Parámetros:
        - x: La cadena de texto que se evaluará.

        Retorna:
        El resultado de la evaluación de la cadena de texto.

        """
        if isinstance(x, str):
            return ast.literal_eval(x)
        else:
            return None
        
    def get_actor_name(cast: str, name: str) -> dict:
        """
        Verifica si el nombre de un actor específico se encuentra en el elenco de una película.

        Parámetros:
        - cast (str): El elenco de la película en forma de cadena de texto.
        - name (str): El nombre del actor para verificar su presencia en el elenco.

        Retorna:
        Un valor booleano que indica si el actor se encuentra en el elenco de la película.

        """
        cast = str_eval(cast)
        if isinstance(cast, list):
            if len(cast) == 0:
                return False
            for person in cast:
                if person == name:
                    return True
            return False
        else:
            return False

    actor = actor.title()

    movies_ = movies.copy()

    # Aplicar la función get_actor_name a la columna 'cast' para obtener una máscara de las películas en las que el actor ha participado
    mask = movies_['cast'].apply(lambda x: get_actor_name(x, actor))
    actor_movies = movies_[mask].loc[:, 'return']

    num_movies = actor_movies.shape[0]
    return_sum = round(actor_movies.sum(),ndigits=2)
    return_mean = round(actor_movies.mean(),ndigits=2)
    return {'actor':actor, 'cantidad_filmaciones':num_movies, 'retorno_total':return_sum, 'retorno_promedio':return_mean}


@app.get("/get_director/{director}")
def get_director(director: str) -> dict:
    """
    Devuelve un diccionario que contiene información sobre las películas dirigidas por un director específico.

    Parámetros:
    - director (str): El nombre del director para el cual se desea obtener la información.

    Retorna:
    Un diccionario que contiene información sobre las películas dirigidas por el director.
    El diccionario contiene los siguientes campos:
    - 'director': El nombre del director.
    - 'retorno_total_director': El retorno financiero total de todas las películas dirigidas por el director.
    - 'peliculas': Una lista de los títulos de las películas dirigidas por el director.
    - 'anio': Una lista de los años de estreno de las películas dirigidas por el director.
    - 'retorno_pelicula': Una lista de los retornos financieros de las películas dirigidas por el director.
    - 'budget_pelicula': Una lista de los presupuestos de las películas dirigidas por el director.
    - 'revenue_pelicula': Una lista de los ingresos generados por las películas dirigidas por el director.

    """

    director = director.title()  # Convertir el nombre del director a título de caso

    director_return = movies[movies['director'] == director].loc[:, ['director', 'title', 'release_year', 'budget', 'revenue', 'return']]

    return {
        'director': director,
        'retorno_total_director': round(director_return['return'].sum(), 2),
        'peliculas': director_return['title'].to_list(),
        'anio': director_return['release_year'].to_list(),
        'retorno_pelicula': director_return['return'].to_list(),
        'budget_pelicula': director_return['budget'].to_list(),
        'revenue_pelicula': director_return['revenue'].to_list()
    }

@app.get("/recomendacion/{title}")
def recomendacion(title: str) -> dict:
    """
    Devuelve una lista de recomendaciones relacionadas con una película específica.

    Parámetros:
    - title (str): El título de la película para la cual se desean obtener las recomendaciones.

    Retorna:
    Un diccionario que contiene las recomendaciones relacionadas con la película especificada.

    """

    title = title.title()

    return {'Lista Recomendada':recommendations[recommendations['title'] == title].iloc[0, 1:].to_list()}