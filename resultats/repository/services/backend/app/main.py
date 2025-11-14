from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from app.routers import api_v1, partner_api
from app.database import init_db, close_db, check_db_connection
from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire du cycle de vie de l'application FastAPI."""
    
    # Startup: Initialisation de la base de données
    print("🚀 Démarrage de l'application PredictMob...")
    
    # Vérification de la connexion DB
    if await check_db_connection():
        print("✅ Connexion à la base de données établie")
        # Note: En production, utilisez Alembic au lieu de init_db()
        await init_db()
        print("✅ Base de données initialisée")
    else:
        print("❌ Impossible de se connecter à la base de données")
        print("⚠️  L'application démarrera mais les endpoints DB ne fonctionneront pas")
    
    yield
    
    # Shutdown: Nettoyage des ressources
    print("🔄 Arrêt de l'application...")
    await close_db()
    print("✅ Connexions fermées")

tags_metadata = [
    {
        "name": "Public - Core API",
    },
    {
        "name": "Publique - API Partenaire",
    },
    {
        "name": "Privé - Core API",
    },
]

app = FastAPI(
    title=settings.api.title,
    version=settings.api.version,
    description="API pour la prédiction des aléas de transport et alternatives de mobilité",
    lifespan=lifespan,
    contact={
        "name": "Équipe PredictMob",
        "email": "contact@predictmob.fr"
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=tags_metadata
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="PredictMob API",
        version="1.0.0",
        description="""
## API PredictMob - Système de prédiction et alternatives de mobilité

### Vue d'ensemble
PredictMob est un système intelligent qui prédit les aléas de transport et propose des alternatives de mobilité durable.

### Fonctionnalités principales

#### 🚨 Système de prédiction (Levier A)
- **Hotspots**: Zones de risque de retard identifiées par IA
- **Alternatives**: Solutions de mobilité alternatives proposées automatiquement

#### 📱 Suivi de mobilité (Levier B) 
- **Logs de trajets**: Enregistrement des choix de mobilité des employés
- **Consentement**: Gestion du partage de données avec l'entreprise
- **RSE**: Indicateurs environnementaux et sociaux
- **Gamification**: Classements et points pour encourager la mobilité durable

#### 🤝 API Partenaires
- Intégration de solutions externes (BlaBlaCar, Vélib', RATP...)
- Proposition automatique d'alternatives par les partenaires

### Authentification
L'authentification sera implémentée dans une version future. Pour l'instant, l'API fonctionne avec des données de démonstration.

### Environnement de test
Cette version utilise des données mock pour démonstration. La logique métier et la base de données seront intégrées dans les versions suivantes.
        """,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get(
    "/",
    tags=["Système"],
    summary="Point d'entrée de l'API",
    description="Informations générales sur l'API PredictMob"
)
async def root():
    """Point d'entrée principal de l'API PredictMob"""
    return {
        "message": "Bienvenue sur l'API PredictMob",
        "version": "1.0.0",
        "description": "Système de prédiction des aléas de transport et alternatives de mobilité",
        "documentation": "/docs",
        "status": "active"
    }

@app.get(
    "/health",
    tags=["Système"],
    summary="Vérification de l'état de l'API",
    description="Endpoint de vérification de l'état de santé de l'API"
)
async def health_check():
    """Vérification de l'état de santé du service"""
    db_status = await check_db_connection()
    return {
        "status": "healthy" if db_status else "degraded",
        "database": "connected" if db_status else "disconnected",
        "timestamp": "2025-11-14T12:00:00Z",
        "version": settings.api.version
    }

# Routes principales
app.include_router(api_v1.router)
app.include_router(partner_api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
