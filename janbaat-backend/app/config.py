from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_name: str = "JanBaat"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    allowed_origins: str = "http://localhost:3000,http://localhost:8081"

    # Supabase
    supabase_url: str
    supabase_service_key: str
    supabase_jwt_secret: str

    # Database
    database_url: str

    # Redis
    redis_url: str

    # AI
    openai_api_key: str

    # Cloudinary
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    # Firebase
    firebase_credentials_path: str = "./firebase-credentials.json"

    # Rate limiting
    rate_limit_per_minute: int = 100

    # Monitoring
    sentry_dsn: str = ""

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


settings = Settings()
