"""
AutoDL弹性部署API使用示例
展示如何使用AutoDLElasticDeployment类进行各种操作
"""

import sys
import time
from autodl import AutoDLElasticDeployment, AutoDLConstants


def main():
    """主函数 - 演示各种API功能"""
    
    # 从文件读取token
    try:
        with open(".autodl_token", "r") as f:
            token = f.read().strip()
    except FileNotFoundError:
        print("请创建.autodl_token文件并填入您的API token")
        return
    
    # 创建客户端
    client = AutoDLElasticDeployment(token)
    
    print("=== AutoDL弹性部署API演示 ===\n")
    
    # 1. 获取镜像列表
    print("1. 获取私有镜像列表:")
    try:
        images = client.get_images(page_index=1, page_size=5)
        if images:
            for img in images:
                print(f"   - {img['image_name']} (UUID: {img['image_uuid']})")
        else:
            print("   没有找到私有镜像")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 2. 获取部署列表
    print("2. 获取当前部署列表:")
    deployments = []
    try:
        deployments = client.get_deployments()
        if deployments:
            for dep in deployments:
                print(f"   - {dep['name']} (UUID: {dep['uuid']}) - 状态: {dep['status']}")
        else:
            print("   没有找到部署")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 3. 获取GPU库存
    print("3. 获取西北企业区GPU库存 (CUDA 11.8):")
    try:
        region_sign = AutoDLConstants.REGIONS["西北企业区(推荐)"]
        stock = client.get_gpu_stock(region_sign, 118)
        if stock:
            for gpu in stock:
                print(f"   - {gpu['gpu_type']}: 可用 {gpu['idle_gpu_num']}/{gpu['total_gpu_num']}")
        else:
            print("   没有找到GPU库存信息")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 4. 演示创建部署功能
    print("4. 创建部署功能:")
    print("   ✅ 支持三种部署类型：")
    print("   - ReplicaSet: 副本集部署")
    print("   - Job: 任务部署")
    print("   - Container: 容器部署")
    print("   ")
    print("   示例：创建ReplicaSet部署")
    print("   # deployment_uuid = client.create_replicaset_deployment(")
    print("   #     name='API测试部署',")
    print("   #     image_uuid='base-image-l2t43iu6uk',")
    print("   #     replica_num=1,")
    print("   #     gpu_name_set=['RTX 4090'],")
    print("   #     gpu_num=1,")
    print("   #     cmd='jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root'")
    print("   # )")
    print("   ")
    print("   示例：停止和删除部署")
    print("   # client.stop_deployment(deployment_uuid)  # 停止部署")
    print("   # client.delete_deployment(deployment_uuid)  # 删除部署")
    
    print()
    
    # 5. 如果有部署，演示其他操作
    if deployments:
        deployment = deployments[0]  # 使用第一个部署进行演示
        print(f"5. 对部署 '{deployment['name']}' 进行演示操作:")
        
        # 获取容器列表
        try:
            containers = client.query_containers(deployment['uuid'])
            print(f"   - 容器数量: {len(containers)}")
            for container in containers:
                if isinstance(container, dict):
                    print(f"     * {container.get('container_uuid', 'N/A')} - 状态: {container.get('status', 'N/A')}")
                else:
                    print(f"     * {container} - 状态: N/A")
        except Exception as e:
            print(f"   获取容器失败: {e}")
        
        # 获取容器事件
        try:
            events = client.query_container_events(deployment['uuid'])
            print(f"   - 容器事件数量: {len(events)}")
        except Exception as e:
            print(f"   获取容器事件失败: {e}")
        
        # 获取调度黑名单
        try:
            blacklist = client.get_scheduling_blacklist(deployment['uuid'])
            print(f"   - 调度黑名单: {blacklist}")
        except Exception as e:
            print(f"   获取调度黑名单失败: {e}")
        
        # 获取时长包信息
        try:
            ddp_info = client.get_ddp_overview(deployment['uuid'])
            if ddp_info:
                for ddp in ddp_info:
                    print(f"   - GPU类型: {ddp.get('gpu_type', 'N/A')}")
                    print(f"     总时长: {ddp.get('total', 0)}秒")
                    print(f"     剩余时长: {ddp.get('balance', 0)}秒")
                    print(f"     地区: {ddp.get('dc_list', 'N/A')}")
        except Exception as e:
            print(f"   获取时长包信息失败: {e}")
    
    print()
    
    # 6. 显示常量信息
    print("6. 可用的地区标识:")
    for name, sign in AutoDLConstants.REGIONS.items():
        print(f"   - {name}: {sign}")
    
    print("\n可用的基础镜像:")
    for name, uuid in AutoDLConstants.BASE_IMAGES.items():
        print(f"   - {name}: {uuid}")
    
    print("\nCUDA版本映射:")
    for version, code in AutoDLConstants.CUDA_VERSIONS.items():
        print(f"   - CUDA {version}: {code}")


def create_sample_deployment(client):
    """创建示例部署的函数"""
    print("创建示例部署...")
    
    try:
        # 使用PyTorch 2.0.0基础镜像创建部署
        deployment_uuid = client.create_replicaset_deployment(
            name='API测试部署',
            image_uuid=AutoDLConstants.BASE_IMAGES['PyTorch 2.0.0 (CUDA 11.8)'],
            replica_num=1,
            gpu_name_set=['RTX 4090'],
            gpu_num=1,
            cpu_num_from=1,
            cpu_num_to=100,
            memory_size_from=1,
            memory_size_to=256,
            dc_list=['westDC2'],
            cuda_v_from=118,
            cmd='jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root',
            env_vars={'JUPYTER_TOKEN': 'test123'},
            price_from=10,
            price_to=9000,
            reuse_container=True
        )
        
        print(f"部署创建成功，UUID: {deployment_uuid}")
        return deployment_uuid
        
    except Exception as e:
        print(f"创建部署失败: {e}")
        return None


def manage_deployment(client, deployment_uuid):
    """管理部署的示例函数"""
    if not deployment_uuid:
        return
    
    print(f"\n管理部署 {deployment_uuid}:")
    
    # 等待部署启动
    print("等待部署启动...")
    time.sleep(10)
    
    # 获取容器信息
    try:
        containers = client.query_containers(deployment_uuid)
        print(f"容器数量: {len(containers)}")
        
        if containers:
            # 停止第一个容器
            container = containers[0]
            container_uuid = container.get('deployment_container_uuid', '')
            if container_uuid:
                print(f"停止容器 {container_uuid}...")
                client.stop_container(container_uuid)
            
            # 修改副本数量
            print("设置副本数量为2...")
            client.set_replicas(deployment_uuid, 2)
            
            # 设置调度黑名单
            print("设置调度黑名单...")
            client.set_scheduling_blacklist(deployment_uuid, 10, "测试黑名单")
            
            # 停止部署
            print("停止部署...")
            client.stop_deployment(deployment_uuid)
            
            # 删除部署
            print("删除部署...")
            client.delete_deployment(deployment_uuid)
            
    except Exception as e:
        print(f"管理部署时出错: {e}")


if __name__ == "__main__":
    main()
    
    # 如果要实际创建和管理部署，取消注释以下代码
    # client = AutoDLElasticDeployment(token)
    # deployment_uuid = create_sample_deployment(client)
    # manage_deployment(client, deployment_uuid) 