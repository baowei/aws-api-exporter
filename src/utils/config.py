import os
import yaml
import logging

class Config:
    """
    配置管理类，用于加载和管理配置
    """
    def __init__(self, config_file=None):
        """
        初始化配置
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认配置
        """
        self.logger = logging.getLogger('aws-api-exporter')
        self.config = {
            'aws': {
                'region': os.environ.get('AWS_REGION', 'us-east-1'),
                'access_key_id': os.environ.get('AWS_ACCESS_KEY_ID', None),
                'secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY', None),
            },
            'exporter': {
                'port': int(os.environ.get('EXPORTER_PORT', 9090)),
                'address': os.environ.get('EXPORTER_ADDRESS', '0.0.0.0'),
                'metrics_path': os.environ.get('EXPORTER_METRICS_PATH', '/metrics'),
                'collectors': {
                    'ec2': True,
                    'rds': True
                }
            }
        }
        
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file):
        """
        从文件加载配置
        
        Args:
            config_file: 配置文件路径
        """
        try:
            with open(config_file, 'r') as f:
                file_config = yaml.safe_load(f)
                self._merge_config(self.config, file_config)
        except Exception as e:
            self.logger.error(f"Error loading config file: {e}")
    
    def _merge_config(self, base, override):
        """
        合并配置
        
        Args:
            base: 基础配置
            override: 覆盖配置
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key, default=None):
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的路径
            default: 默认值
        
        Returns:
            配置值
        """
        parts = key.split('.')
        config = self.config
        
        for part in parts:
            if part in config:
                config = config[part]
            else:
                return default
        
        return config