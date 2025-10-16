from prometheus_client.core import GaugeMetricFamily
from .base_collector import BaseCollector

class EC2VolumeCollector(BaseCollector):
    """
    收集EC2卷的大小和IOPS指标
    """
    def _create_client(self):
        """
        创建EC2客户端
        
        Returns:
            boto3 EC2客户端
        """
        return self._create_boto3_client('ec2')
    
    def _collect_metrics(self):
        """
        收集EC2卷指标
        
        Returns:
            生成器，产生指标对象
        """
        # 创建基础标签列表
        base_labels = ['volume_id', 'volume_type', 'availability_zone', 'state', 'name']
        
        # 创建卷IOPS指标
        volume_iops = GaugeMetricFamily(
            'aws_ec2_volume_iops',
            'IOPS of EC2 volume',
            labels=base_labels
        )
        
        # 创建卷吞吐量指标
        volume_throughput = GaugeMetricFamily(
            'aws_ec2_volume_throughput_mbps',
            'Throughput of EC2 volume in MBps',
            labels=base_labels
        )
        
        # 获取所有卷信息
        paginator = self.client.get_paginator('describe_volumes')
        for page in paginator.paginate():
            for volume in page.get('Volumes', []):
                volume_id = volume.get('VolumeId')
                volume_type = volume.get('VolumeType')
                availability_zone = volume.get('AvailabilityZone')
                state = volume.get('State')
                
                # 获取卷的标签
                tags = volume.get('Tags', [])
                name = next((tag['Value'] for tag in tags if tag['Key'].lower() == 'name'), 'unknown')
                
                # 准备标签值列表
                label_values = [
                    volume_id,
                    volume_type,
                    availability_zone,
                    state,
                    name
                ]
                
                # 添加卷IOPS指标
                volume_iops.add_metric(
                    label_values,
                    volume.get('Iops', 0)
                )
                
                # 添加卷吞吐量指标 (仅适用于某些卷类型)
                throughput = volume.get('Throughput', 0)
                volume_throughput.add_metric(
                    label_values,
                    throughput
                )
        
        yield volume_iops
        yield volume_throughput