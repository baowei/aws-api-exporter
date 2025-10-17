from prometheus_client.core import GaugeMetricFamily
from .base_collector import BaseCollector

class RDSInstanceCollector(BaseCollector):
    """
    收集RDS实例的存储大小和IOPS指标
    """
    def _create_client(self):
        """
        创建RDS客户端
        
        Returns:
            boto3 RDS客户端
        """
        return self._create_boto3_client('rds')
    
    def _collect_metrics(self):
        """
        收集RDS实例指标
        
        Returns:
            生成器，产生指标对象
        """
        # 创建RDS存储大小指标
        storage_size = GaugeMetricFamily(
            'aws_rds_allocated_storage_gb',
            'Allocated storage size of RDS instance in GB',
            labels=['dbinstance_identifier', 'db_instance_class', 'engine', 'availability_zone', 'status']
        )
        
        # 创建RDS IOPS指标
        provisioned_iops = GaugeMetricFamily(
            'aws_rds_provisioned_iops',
            'Provisioned IOPS of RDS instance',
            labels=['dbinstance_identifier', 'db_instance_class', 'engine', 'availability_zone', 'status']
        )
        
        paginator = self.client.get_paginator('describe_db_instances')
        for page in paginator.paginate():
            for instance in page.get('DBInstances', []):
                dbinstance_identifier = instance.get('DBInstanceIdentifier')
                db_instance_class = instance.get('DBInstanceClass')
                engine = instance.get('Engine')
                availability_zone = instance.get('AvailabilityZone')
                status = instance.get('DBInstanceStatus')
                
                # 添加存储大小指标
                storage_size.add_metric(
                    [dbinstance_identifier, db_instance_class, engine, availability_zone, status],
                    instance.get('AllocatedStorage', 0)
                )
                
                # 添加IOPS指标
                iops = instance.get('Iops', 0)
                provisioned_iops.add_metric(
                    [dbinstance_identifier, db_instance_class, engine, availability_zone, status],
                    iops
                )
        
        yield storage_size
        yield provisioned_iops
