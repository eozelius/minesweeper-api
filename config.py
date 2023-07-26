class LocalConfig:
  ENV = "local"

class ProductionConfig:
  ENV = "prod"

config = {
  "local": LocalConfig,
  "production": ProductionConfig,
}
