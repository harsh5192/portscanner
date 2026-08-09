import os
from typing import Dict, Any, Optional
from pathlib import Path
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class ProfileConfig(BaseModel):
    name: str
    description: str
    nmap_arguments: str
    requires_authorization: bool = False

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SCANNER_", env_file=".env", extra="ignore")

    app_name: str = "Modular Network Security Assessment Platform"
    app_version: str = "0.1.0"
    env: str = "development"
    debug: bool = False
    database_url: str = "sqlite:///./data/scanner.db"
    nmap_path: str = "nmap"
    default_timeout: int = 300
    output_dir: str = "./reports"
    log_level: str = "INFO"
    log_file_path: str = "./logs/scanner.log"
    profiles: Dict[str, ProfileConfig] = Field(default_factory=dict)

def load_settings(config_path: Optional[str] = None) -> Settings:
    """Load settings from config.yaml and environment variables."""
    settings_dict: Dict[str, Any] = {}
    
    # Locate config.yaml
    path = Path(config_path) if config_path else Path("config.yaml")
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f) or {}
            
            if "app" in yaml_data:
                settings_dict["app_name"] = yaml_data["app"].get("name", settings_dict.get("app_name"))
                settings_dict["app_version"] = yaml_data["app"].get("version", settings_dict.get("app_version"))
                settings_dict["env"] = yaml_data["app"].get("env", settings_dict.get("env"))

            if "database" in yaml_data:
                settings_dict["database_url"] = yaml_data["database"].get("url", "sqlite:///./data/scanner.db")

            if "scanner" in yaml_data:
                sc = yaml_data["scanner"]
                settings_dict["nmap_path"] = sc.get("nmap_path", "nmap")
                settings_dict["default_timeout"] = sc.get("default_timeout", 300)
                settings_dict["output_dir"] = sc.get("output_dir", "./reports")

            if "logging" in yaml_data:
                lg = yaml_data["logging"]
                settings_dict["log_level"] = lg.get("level", "INFO")
                settings_dict["log_file_path"] = lg.get("file_path", "./logs/scanner.log")

            if "profiles" in yaml_data:
                settings_dict["profiles"] = {
                    k: ProfileConfig(**v) for k, v in yaml_data["profiles"].items()
                }

    return Settings(**settings_dict)

settings = load_settings()
