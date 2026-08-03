from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig
from typing import Any as any

config_by_name: dict[str, any] = {
    'development': DevelopmentConfig,
    'dev': DevelopmentConfig,
    'production': ProductionConfig,
    'prod': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}