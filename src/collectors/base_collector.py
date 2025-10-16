import abc
import boto3
import logging
from prometheus_client.core import GaugeMetricFamily

class BaseCollector(abc.ABC):
    """
    收集器抽象基类：定义所有 Collector 的统一接口
    所有具体收集器必须继承此类并实现抽象方法
    """
    def __init__(self, region="us-east-1", aws_access_key_id=None, aws_secret_access_key=None):
        """
        初始化基础收集器
        
        Args:
            region: AWS区域
            aws_access_key_id: AWS访问密钥ID
            aws_secret_access_key: AWS秘密访问密钥
        """
        self.region = region
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.logger = logging.getLogger('aws-api-exporter')
        self.client = self._create_client()
    
    def _create_boto3_client(self, service_name):
        """
        创建boto3客户端
        
        Args:
            service_name: AWS服务名称
            
        Returns:
            boto3客户端
        """
        return boto3.client(
            service_name,
            region_name=self.region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
    
    @abc.abstractmethod
    def _create_client(self):
        """
        创建AWS服务客户端
        
        Returns:
            boto3客户端对象
        """
        pass
    
    @abc.abstractmethod
    def _collect_metrics(self):
        """
        收集指标的具体实现
        
        Returns:
            生成器，产生指标对象
        """
        pass
    
    def collect(self):
        """
        Prometheus收集器接口方法
        
        Returns:
            生成器，产生指标对象
        """
        try:
            yield from self._collect_metrics()
        except Exception as e:
            self.logger.error(f"Error collecting metrics in {self.__class__.__name__}: {e}")
            # 在出错时返回一个错误指标
            error_metric = GaugeMetricFamily(
                f'aws_collector_error',
                f'Error occurred during metrics collection',
                labels=['collector_type', 'error']
            )
            error_metric.add_metric([self.__class__.__name__, str(e)], 1)
            yield error_metric