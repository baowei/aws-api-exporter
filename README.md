
# AWS API Exporter Create by Claude-3.5-Sonnet module

一个用于收集AWS资源指标的Prometheus Exporter，目前支持以下指标：

- EC2卷大小和IOPS指标
- RDS实例分配存储大小和IOPS指标

## 功能特点

- 模块化设计，易于扩展
- 支持通过配置文件或环境变量进行配置
- 支持多种AWS认证方式（环境变量、配置文件、IAM角色）
- 提供Docker支持，便于部署

## 指标列表

### EC2卷指标

- `aws_ec2_volume_iops`: EC2卷IOPS
- `aws_ec2_volume_throughput_mbps`: EC2卷吞吐量（MBps）

### RDS实例指标

- `aws_rds_allocated_storage_gb`: RDS实例分配存储大小（GB）
- `aws_rds_provisioned_iops`: RDS实例预置IOPS

## 安装

### 从源码安装

```bash
git clone https://github.com/baowei/aws-api-exporter.git
cd aws-api-exporter
pip install -r requirements.txt
```

### 使用Docker

```bash
docker build -t aws-api-exporter .
docker run -p 9099:9099 -v $(pwd)/config:/app/config aws-api-exporter
```

## 配置

可以通过配置文件或环境变量进行配置。

### 配置文件

复制示例配置文件并进行修改：

```bash
cp config/config.yaml.example config/config.yaml
```

### 环境变量

- `AWS_REGION`: AWS区域
- `AWS_ACCESS_KEY_ID`: AWS访问密钥ID
- `AWS_SECRET_ACCESS_KEY`: AWS秘密访问密钥
- `EXPORTER_PORT`: Exporter端口
- `EXPORTER_ADDRESS`: Exporter监听地址
- `EXPORTER_METRICS_PATH`: 指标路径

## 使用方法

### 直接运行

```bash
python src/exporter.py --config config/config.yaml
```

### 使用Docker

```bash
docker run -p 9099:9099 -v $(pwd)/config:/app/config aws-api-exporter
```

## 访问指标

指标可通过以下URL访问：

```
http://localhost:9090/metrics
```

## 在Prometheus中配置

在Prometheus配置文件中添加以下内容：

```yaml
scrape_configs:
  - job_name: 'aws-api-exporter'
    static_configs:
      - targets: ['localhost:9099']
```

## 扩展

如需添加新的收集器，只需在`src/collectors`目录下创建新的收集器类，并在`src/exporter.py`中注册即可。