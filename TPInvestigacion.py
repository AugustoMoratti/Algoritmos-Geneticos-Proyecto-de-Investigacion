import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Ruta del archivo descargado
archivo_geojson = "datosElectricosArgentina.geojson"

# Cargar el archivo como GeoDataFrame
gdf = gpd.read_file(archivo_geojson)

# Mostrar los primeros elementos
print(gdf.head())

# Ver las columnas disponibles (por ejemplo: 'power', 'geometry')
print(gdf.columns)

# Filtrar por tipo (opcional)
lineas = gdf[gdf['power'] == 'line']
torres = gdf[gdf['power'] == 'tower']
subestaciones = gdf[gdf['power'] == 'substation']




# Tu ubicación candidata (ejemplo: latitud y longitud)
lat, lon = -32.9468, -60.6393  # Rosario

# Crear punto
mi_ubicacion = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326")

# Asegurar que todo esté en la misma proyección para cálculo de distancia
gdf = gdf.to_crs(epsg=3857)
mi_ubicacion = mi_ubicacion.to_crs(epsg=3857)

# Calcular distancia mínima
distancias = gdf.distance(mi_ubicacion.iloc[0])
min_distancia = distancias.min()

print(f"Distancia mínima a infraestructura eléctrica: {min_distancia:.2f} metros")
ax = gdf[gdf["power"] == "line"].plot(color="red", linewidth=1, figsize=(10, 10))
mi_ubicacion.plot(ax=ax, color="blue", markersize=50)
plt.title("Red eléctrica y ubicación candidata")
plt.show()