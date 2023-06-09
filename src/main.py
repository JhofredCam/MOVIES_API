import pandas as pd
from fastapi import FastAPI
import ast

# http://127.0.0.1:8000/

app = FastAPI()

movies = pd.read_csv("Tables\movies.csv")

@app.get("/cantidad_filmaciones_mes/{month}")
def cantidad_filmaciones_mes(month:str) -> str:
    """
    Devuelve la cantidad de películas estrenadas en un mes específico.

    Parámetros:
    - month (str): El mes para el cual se desea obtener la cantidad de películas estrenadas.

    Retorna:
    Una cadena de texto que indica la cantidad de películas estrenadas en el mes especificado.

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

    return f"{num_movies} cantidad de películas fueron estrenadas en el mes de {month}"



@app.get("/cantidad_filmaciones_dia/{day}")
def cantidad_filmaciones_dia(day:str) -> str:
    """
    Devuelve la cantidad de películas estrenadas en un día específico.

    Parámetros:
    - day (str): El día para el cual se desea obtener la cantidad de películas estrenadas.

    Retorna:
    Una cadena de texto que indica la cantidad de películas estrenadas en el día especificado.

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

    return f"{num_movies} cantidad de películas fueron estrenadas en el día {days[day]} ({day})"



@app.get("/score_titulo/{title}")
def score_titulo(title: str) -> str:
    """
    Devuelve la información del título, año de estreno y puntaje de una película específica.

    Parámetros:
    - title (str): El título de la película para la cual se desea obtener la información.

    Retorna:
    Una cadena de texto que muestra el título de la película, su año de estreno y su puntaje/popularidad.

    """
    # Obtener la película con el título proporcionado
    movie = movies[movies['title'] == title].iloc[0, :]

    # Seleccionar las columnas relevantes: título, año de estreno y puntaje
    movie = movie[['title', 'release_year', 'vote_average']]

    return f"La película {movie['title']} fue estrenada en el año {movie['release_year']} con un score/popularidad de {movie['vote_average']}"



@app.get("/votos_titulo/{title}")
def votos_titulo(title: str) -> str:
    """
    Devuelve información sobre el número de votos y el puntaje promedio de una película específica.

    Parámetros:
    - title (str): El título de la película para la cual se desea obtener la información.

    Retorna:
    Una cadena de texto que muestra el título de la película, su año de estreno, el número de votos y el puntaje promedio.

    """
    # Obtener la película con el título proporcionado
    movie = movies[movies['title'] == title].iloc[0, :]

    # Verificar si la película tiene 2000 votos o más
    if movie['vote_count'] >= 2000:
        return f"La película {movie['title']} fue estrenada en el año {movie['release_year']}. La misma cuenta con un total de {int(movie['vote_count'])} valoraciones, con un score promedio de {movie['vote_average']}"
    
    else:
        # Devolver un mensaje indicando que la película no cumple con el criterio de votos mínimos
        return "La película no contiene 2000 valoraciones o más, por lo que no se devuelve ningún valor"
    
@app.get("/get_actor/{actor}")
def get_actor(actor: str) -> str:
    """
    Devuelve información sobre las filmaciones en las que un actor específico ha participado.

    Parámetros:
    - actor (str): El nombre del actor para el cual se desea obtener la información.

    Retorna:
    Una cadena de texto que muestra el nombre del actor, el número de filmaciones en las que ha participado,
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
        
    def get_actor_name(cast: str, name: str) -> bool:
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

    movies_ = movies.copy()

    # Aplicar la función get_actor_name a la columna 'cast' para obtener una máscara de las películas en las que el actor ha participado
    mask = movies_['cast'].apply(lambda x: get_actor_name(x, actor))
    actor_movies = movies_[mask].loc[:, 'return']

    num_movies = actor_movies.shape[0]
    return_sum = round(actor_movies.sum(),ndigits=2)
    return_mean = round(actor_movies.mean(),ndigits=2)

    return f"El actor {actor} ha participado en {num_movies} filmaciones, el mismo ha conseguido un retorno de {return_sum} con un promedio de {return_mean} por filmación"

@app.get("/get_director/{director}")
def get_director(director: str) -> list:
    """
    Devuelve una lista de diccionarios que contiene información sobre las películas dirigidas por un director específico.

    Parámetros:
    - director (str): El nombre del director para el cual se desea obtener la información.

    Retorna:
    Una lista de diccionarios que contiene información sobre las películas dirigidas por el director.
    Cada diccionario representa una película y contiene los siguientes campos:
    - 'title': El título de la película.
    - 'release_year': El año de estreno de la película.
    - 'budget': El presupuesto de la película.
    - 'revenue': Los ingresos generados por la película.
    - 'return': El retorno financiero de la película.

    """
    director_return = movies[movies['director'] == director].loc[:, ['title', 'release_year', 'budget', 'revenue', 'return']]
    director_return['return'] = director_return['return'].apply(lambda x: round(x,ndigits=2))
    return director_return.to_dict('records')