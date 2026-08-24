"""Configuration management for NetConnect."""

import os
import yaml
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path
import platformdirs


@dataclass
class NetConnectConfig:
    """NetConnect configuration."""
    defaults: dict = field(default_factory=lambda: {
        "duration": 300,
        "timeout": 5,
        "output": "table",
        "protocol": "both",
    })
    logging: dict = field(default_factory=lambda: {
        "level": "INFO",
        "file": "",
    })


class ConfigManager:
    """Manages NetConnect configuration."""
    
    def __init__(self):
        self.app_name = "netconnect"
        self.app_author = "NetConnect"
        self.config_dir = Path(platformdirs.user_config_dir(self.app_name, self.app_author))
        self.config_file = self.config_dir / "config.yaml"
        self._config: Optional[NetConnectConfig] = None
    
    def load(self) -> NetConnectConfig:
        """Load configuration from file."""
        if self._config is not None:
            return self._config
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = yaml.safe_load(f) or {}
                self._config = NetConnectConfig(
                    defaults=data.get('defaults', {}),
                    logging=data.get('logging', {})
                )
            except Exception:
                self._config = NetConnectConfig()
        else:
            self._config = NetConnectConfig()
        
        return self._config
    
    def save(self, config: NetConnectConfig) -> None:
        """Save configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        data = {
            'defaults': config.defaults,
            'logging': config.logging,
        }
        with open(self.config_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        self._config = config
    
    def get_default(self, key: str, default=None):
        """Get a default value from config."""
        return self.load().defaults.get(key, default)
    
    def set_default(self, key: str, value) -> None:
        """Set a default value in config."""
        config = self.load()
        config.defaults[key] = value
        self.save(config)
    
    def get_config_path(self) -> Path:
        """Get path to config file."""
        return self.config_file


# Global instance
config_manager = ConfigManager()