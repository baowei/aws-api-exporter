import time
import argparse
from prometheus_client import start_http_server, REGISTRY

from utils.config import Config
from utils.logger import setup_logger
from collectors.ec2_collector import EC2VolumeCollector
from collectors.rds_collector import RDSInstanceCollector
from collectors.base_collector import BaseCollector

class AWSExporter:
    """
    AWS Exporter主类，用于注册收集器并启动HTTP服务器
    """
    def __init__(self, config_file=None):
        """
        初始化AWS Exporter
        
        Args:
            config_file: 配置文件路径
        """
        self.config = Config(config_file)
        self.logger = setup_logger()
        self.collectors = []
        
        # 注册收集器
        self._register_collectors()
    
    def _register_collectors(self):
        """
        注册所有启用的收集器
        """
        aws_config = {
            'region': self.config.get('aws.region'),
            'aws_access_key_id': self.config.get('aws.access_key_id'),
            'aws_secret_access_key': self.config.get('aws.secret_access_key')
        }
        
        # 注册EC2卷收集器
        if self.config.get('exporter.collectors.ec2', True):
            self.logger.info("Registering EC2 volume collector")
            REGISTRY.register(EC2VolumeCollector(**aws_config))
        
        # 注册RDS实例收集器
        if self.config.get('exporter.collectors.rds', True):
            self.logger.info("Registering RDS instance collector")
            REGISTRY.register(RDSInstanceCollector(**aws_config))
    
    def start(self):
        """
        启动HTTP服务器
        """
        port = self.config.get('exporter.port', 9099)
        address = self.config.get('exporter.address', '0.0.0.0')
        
        self.logger.info(f"Starting AWS API Exporter on {address}:{port}")
        start_http_server(port, address)
        
        # 保持进程运行
        try:
            while True:
                time.sleep(1800)
        except KeyboardInterrupt:
            self.logger.info("Exporter stopped")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='AWS API Exporter')
    parser.add_argument('--config', help='Path to configuration file')
    args = parser.parse_args()
    
    exporter = AWSExporter(args.config)
    exporter.start()


if __name__ == '__main__':
    main()