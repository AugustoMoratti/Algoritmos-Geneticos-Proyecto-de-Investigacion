# Algoritmos-Geneticos-Proyecto-de-Investigacion

INDIVIDUO

individuo = {
    "lat": float,  # Latitud
    "long": float   # Longitud
}

Todos los demás valores necesarios para calcular el fitness se obtendrán a partir de esta ubicación, consultando fuentes externas como archivos GeoJSON, APIs o bases de datos preprocesadas.

___________________________________________________________________

FITNESS
FUNCIÓN DE FITNESS
La función de fitness está definida así:

Donde:

1. Potencial Eólico (normalizado)

ρ=1.225 kg/m3 (densidad del aire)


A = área de barrido del rotor (ej A = πr^2


v(x) = velocidad media del viento en la ubicación


n(x) = número estimado de aerogeneradores según el terreno



2. Costo de Instalación (normalizado)
Depende de:
Tipo de suelo (ej: rocoso, arenoso)


Pendiente del terreno


Accesibilidad y distancia a caminos


Precio del terreno (puede estimarse por zona)



3. Costo de Transporte (normalizado)
Depende de:
Distancia a la línea eléctrica más cercana


Relieve/topografía


Costo estimado por km de tendido


Necesidad de subestaciones



4. Penalización
if está_en_zona_prohibida:
    Penalización(x) = 1_000_000  # castiga fuertemente
else:
    Penalización(x) = 0
