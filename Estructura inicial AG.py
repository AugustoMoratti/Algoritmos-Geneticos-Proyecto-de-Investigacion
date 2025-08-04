import math
import random

# -------- Constantes físicas --------
RHO = 1.225  # kg/m3, densidad del aire
ROTOR_RADIUS = 40  # metros (ejemplo)
A = math.pi * ROTOR_RADIUS ** 2  # área barrido rotor

# -------- Funciones simuladas para obtener datos basados en lat,long --------
#Obviamente faltaria obtener todos estos datos realmente desde un JSON o una API
def obtener_velocidad_viento(lat, long):
    return random.uniform(5, 12)

def obtener_numero_aerogeneradores(lat, long):
    return random.randint(1, 10)

def obtener_tipo_suelo(lat, long):
    return random.choice(['rocoso', 'arenoso', 'arcilloso'])

def obtener_pendiente(lat, long):
    return random.uniform(0, 30)

def obtener_accesibilidad(lat, long):
    return random.uniform(0, 1)

def obtener_precio_terreno(lat, long):
    return random.uniform(10, 100)

def obtener_distancia_linea_electrica(lat, long):
    return random.uniform(0, 20)

def obtener_relieve(lat, long):
    return random.uniform(0, 1)

def obtener_costo_tendido_km():
    return 50000 #Debemos cambiar por un valor real

def necesita_subestacion(lat, long):
    return random.choice([True, False])

def esta_en_zona_prohibida(lat, long):
    return random.random() < 0.05

# -------- Normalización simple --------
def normalizar(valor, minimo, maximo):
    if maximo - minimo == 0:
        return 0
    return (valor - minimo) / (maximo - minimo)

# -------- Función de fitness --------
def calcular_fitness(individuo):
    lat = individuo['lat']
    long = individuo['long']

    v = obtener_velocidad_viento(lat, long)
    n = obtener_numero_aerogeneradores(lat, long)
    pot_eol = 0.5 * RHO * A * v**3 * n

    v_norm = normalizar(v, 5, 12)
    n_norm = normalizar(n, 1, 10)
    pot_eol_norm = v_norm * n_norm

    suelo = obtener_tipo_suelo(lat, long)
    pendiente = obtener_pendiente(lat, long)
    accesibilidad = obtener_accesibilidad(lat, long)
    precio_terreno = obtener_precio_terreno(lat, long)

    costos_suelo = {'rocoso': 100000, 'arenoso': 70000, 'arcilloso': 50000}
    costo_suelo = costos_suelo.get(suelo, 70000)

    pendiente_norm = normalizar(pendiente, 0, 30)
    accesibilidad_norm = accesibilidad
    precio_terreno_norm = normalizar(precio_terreno, 10, 100)
    costo_suelo_norm = normalizar(costo_suelo, 50000, 100000)

    costo_instalacion_norm = (
        0.4 * costo_suelo_norm +
        0.3 * pendiente_norm +
        0.2 * (1 - accesibilidad_norm) +
        0.1 * precio_terreno_norm
    )

    distancia = obtener_distancia_linea_electrica(lat, long)
    relieve = obtener_relieve(lat, long)
    subestacion = necesita_subestacion(lat, long)

    distancia_norm = normalizar(distancia, 0, 20)
    relieve_norm = relieve
    subestacion_cost = 1 if subestacion else 0

    costo_transporte_norm = (
        0.5 * distancia_norm +
        0.3 * relieve_norm +
        0.2 * subestacion_cost
    )

    penalizacion = 1_000_000 if esta_en_zona_prohibida(lat, long) else 0

    fitness = pot_eol_norm - costo_instalacion_norm - costo_transporte_norm - penalizacion

    return fitness

# -------- Clase Individuo --------
class Individuo:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.fitness = None

    def calcular_fitness(self, funcion_fitness):
        self.fitness = funcion_fitness({'lat': self.lat, 'long': self.long})

# -------- Inicialización de población --------
def inicializar_poblacion(tam_poblacion, lat_range, long_range):
    poblacion = []
    for _ in range(tam_poblacion):
        lat = random.uniform(*lat_range)
        long = random.uniform(*long_range)
        poblacion.append(Individuo(lat, long))
    return poblacion

# -------- Selección --------
def seleccion_ruleta(poblacion):
    total_fitness = sum(ind.fitness for ind in poblacion if ind.fitness and ind.fitness > 0)
    if total_fitness == 0:
        return random.choice(poblacion)
    pick = random.uniform(0, total_fitness)
    current = 0
    for ind in poblacion:
        if ind.fitness and ind.fitness > 0:
            current += ind.fitness
            if current > pick:
                return ind
    return random.choice(poblacion)

def seleccion_torneo(poblacion, k=3):
    participantes = random.sample(poblacion, k)
    participantes.sort(key=lambda x: x.fitness if x.fitness is not None else -math.inf, reverse=True)
    return participantes[0]

# -------- Crossover --------
def crossover_padres(padre1, padre2):
    hijo1_lat = (padre1.lat + padre2.lat) / 2
    hijo1_long = (padre1.long + padre2.long) / 2
    hijo2_lat = padre1.lat
    hijo2_long = padre2.long
    return Individuo(hijo1_lat, hijo1_long), Individuo(hijo2_lat, hijo2_long)

# -------- Mutación --------
def mutacion(individuo, prob_mutacion, lat_range, long_range, magnitud=0.1):
    if random.random() < prob_mutacion:
        individuo.lat += random.uniform(-magnitud, magnitud)
        individuo.long += random.uniform(-magnitud, magnitud)
        individuo.lat = max(min(individuo.lat, lat_range[1]), lat_range[0])
        individuo.long = max(min(individuo.long, long_range[1]), long_range[0])

# -------- Algoritmo Genético --------
def algoritmo_genetico(
    funcion_fitness,
    tam_poblacion,
    generaciones,
    lat_range,
    long_range,
    prob_crossover,
    prob_mutacion,
    metodo_seleccion='ruleta'
):
    poblacion = inicializar_poblacion(tam_poblacion, lat_range, long_range)

    # Evaluar fitness inicial
    for ind in poblacion:
        ind.calcular_fitness(funcion_fitness)

    for gen in range(generaciones):
        nueva_poblacion = []

        while len(nueva_poblacion) < tam_poblacion:
            if metodo_seleccion == 'ruleta':
                padre1 = seleccion_ruleta(poblacion)
                padre2 = seleccion_ruleta(poblacion)
            elif metodo_seleccion == 'torneo':
                padre1 = seleccion_torneo(poblacion)
                padre2 = seleccion_torneo(poblacion)
            else:
                raise ValueError("Método de selección no válido")

            if random.random() < prob_crossover:
                hijo1, hijo2 = crossover_padres(padre1, padre2)
            else:
                hijo1, hijo2 = Individuo(padre1.lat, padre1.long), Individuo(padre2.lat, padre2.long)

            mutacion(hijo1, prob_mutacion, lat_range, long_range)
            mutacion(hijo2, prob_mutacion, lat_range, long_range)

            hijo1.calcular_fitness(funcion_fitness)
            hijo2.calcular_fitness(funcion_fitness)

            nueva_poblacion.extend([hijo1, hijo2])

        poblacion = nueva_poblacion[:tam_poblacion]

        mejor = max(poblacion, key=lambda x: x.fitness)
        print(f"Generación {gen+1} - Mejor fitness: {mejor.fitness:.4f} en ({mejor.lat:.4f}, {mejor.long:.4f})")

    return max(poblacion, key=lambda x: x.fitness)

# -------- Ejecución --------
if __name__ == "__main__":
    lat_range = (-35.0, -34.0)
    long_range = (-59.0, -58.0)

    mejor_individuo = algoritmo_genetico(
        funcion_fitness=calcular_fitness,
        tam_poblacion=30,
        generaciones=20,
        lat_range=lat_range,
        long_range=long_range,
        prob_crossover=0.7,
        prob_mutacion=0.1,
        metodo_seleccion='torneo'  # o 'ruleta'
    )

    print("\nMejor individuo encontrado:")
    print(f"Latitud: {mejor_individuo.lat}")
    print(f"Longitud: {mejor_individuo.long}")
    print(f"Fitness: {mejor_individuo.fitness}")
