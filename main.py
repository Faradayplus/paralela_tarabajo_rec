# Importación del framework principal para construir la API
from fastapi import FastAPI

# Importación del manejador de base de datos (pool de conexiones asíncrono)
from database import db

# Importación de los routers que encapsulan los endpoints por temática
from routers.genders import router as genders_router     # Géneros
from routers.species import router as species_router     # Especies
from routers.strata import router as strata_router       # Estratos sociales
from routers.stats import router as stats_router         # Estadísticas

# Se crea una instancia de FastAPI que representa nuestra aplicación principal.
# Aquí se definen metadatos como el título, la descripción y la versión, que se
# mostrarán automáticamente en la documentación Swagger (OpenAPI).
app = FastAPI(
    title="Un API de otro mundo",
    description=(
        "Documentación de la API del trabajo Isekai (simulado) como parte "
        "de la asignatura Computación Paralela y Distribuida de la UTEM "
        "semestre de otoño 2025."
    ),
    version="1.0.0",
)

# Al iniciar la aplicación (startup), se establece la conexión a la base de datos
# utilizando un pool de conexiones asíncrono definido en el módulo `database`.
@app.on_event("startup")
async def on_startup():
    """Inicializa el pool de conexiones al arrancar la aplicación."""
    await db.connect()

# Al cerrar la aplicación (shutdown), se cierra correctamente el pool de conexiones
# para liberar recursos del sistema y evitar conexiones colgantes.
@app.on_event("shutdown")
async def on_shutdown():
    """Cierra el pool de conexiones al detener la aplicación."""
    await db.disconnect()

# Montamos los routers que agrupan las rutas según la lógica de negocio.
# No se define aquí ni el `prefix` ni los `tags`, ya que están contenidos
# directamente en los archivos de cada router.
app.include_router(genders_router)   # Endpoints relacionados con géneros
app.include_router(species_router)   # Endpoints relacionados con especies
app.include_router(strata_router)    # Endpoints relacionados con estratos sociales
app.include_router(stats_router)     # Endpoints relacionados con estadísticas


# Define la ruta principal de la API, que responde a solicitudes GET en "/".
# Sirve como punto de bienvenida y verificación básica del funcionamiento del backend.
@app.get("/", summary="Ruta raíz", tags=["Información base"])
async def root():
    """
    Ruta raíz de la API.
    Devuelve un mensaje de bienvenida para verificar que el servicio está activo.
    """
    return {"message": "Bienvenido a la API Isekai de otro mundo"}
