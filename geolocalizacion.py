import requests

RUTA_URL = "https://graphhopper.com/api/1/route"
GEOCODE_URL = "https://graphhopper.com/api/1/geocode"
KEY = "467b6449-e596-4209-84c0-d25d154fd72c"

def geocodificar(lugar):
    params = {"q": lugar, "limit": 1, "locale": "es", "key": KEY}
    r = requests.get(GEOCODE_URL, params=params)
    datos = r.json()
    if r.status_code == 200 and len(datos["hits"]) != 0:
        hit = datos["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        nombre = hit["name"]
        if "country" in hit:
            nombre += ", " + hit["country"]
        print(f"URL de geocodificación para {nombre}")
        return 200, lat, lng, nombre
    print("Error de geocodificación. Estado:", r.status_code)
    return r.status_code, None, None, lugar

def es_salida(texto):
    return texto.strip().lower() in ("s", "salir")

while True:
    print("\n=========================================")
    print("Perfiles de vehículo disponibles: auto, bicicleta, a pie")
    print("=========================================")
    perfil = input("Ingrese un perfil de vehículo (o 's'/'salir' para terminar): ")
    if es_salida(perfil):
        print("Saliendo del programa. ¡Hasta pronto!")
        break
    mapa = {"auto": "car", "bicicleta": "bike", "a pie": "foot"}
    vehiculo = mapa.get(perfil.strip().lower(), "car")
    if perfil.strip().lower() not in mapa:
        print("Perfil no válido. Se usará 'auto'.")

    origen = input("Ubicación de origen (o 's'/'salir'): ")
    if es_salida(origen):
        print("Saliendo del programa. ¡Hasta pronto!")
        break
    est1, lat1, lng1, nombre1 = geocodificar(origen)

    destino = input("Ubicación de destino (o 's'/'salir'): ")
    if es_salida(destino):
        print("Saliendo del programa. ¡Hasta pronto!")
        break
    est2, lat2, lng2, nombre2 = geocodificar(destino)

    if est1 == 200 and est2 == 200:
        params = [
            ("point", f"{lat1},{lng1}"),
            ("point", f"{lat2},{lng2}"),
            ("vehicle", vehiculo),
            ("locale", "es"),
            ("key", KEY),
        ]
        r = requests.get(RUTA_URL, params=params)
        datos = r.json()
        print("Estado de la API de rutas:", r.status_code)
        if r.status_code == 200:
            ruta = datos["paths"][0]
            km = ruta["distance"] / 1000
            millas = km / 1.61
            seg = int(ruta["time"] / 1000)
            horas = seg // 3600
            minutos = (seg % 3600) // 60
            segundos = seg % 60

            print("=================================================")
            print(f"Dirección desde {nombre1} hasta {nombre2} en {perfil}")
            print("=================================================")
            print(f"Distancia recorrida: {millas:.2f} millas / {km:.2f} km")
            print(f"Duración del viaje: {horas:02d}:{minutos:02d}:{segundos:02d}")
            print("=================================================")
            print("Narrativa del viaje:")
            for paso in ruta["instructions"]:
                dist_km = paso["distance"] / 1000
                print(f"{paso['text']} ( {dist_km:.2f} km )")
            print("=================================================")
        else:
            print("Mensaje de error:", datos.get("message", "sin detalle"))