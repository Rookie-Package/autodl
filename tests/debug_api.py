"""
AutoDL API调试脚本
用于查看API的实际响应格式
"""

import json
from autodl import AutoDLElasticDeployment

def debug_api_responses():
    """调试API响应格式"""
    
    # 从文件读取token
    try:
        with open(".autodl_token", "r") as f:
            token = f.read().strip()
    except FileNotFoundError:
        print("请创建.autodl_token文件并填入您的API token")
        return
    
    # 创建客户端
    client = AutoDLElasticDeployment(token)
    
    print("=== AutoDL API响应调试 ===\n")
    
    # 1. 调试获取镜像列表
    print("1. 调试获取镜像列表:")
    try:
        response = client._make_request("POST", "/api/v1/dev/image/private/list", 
                                      data={"page_index": 1, "page_size": 5})
        print(f"响应状态: {response.get('code')}")
        print(f"响应消息: {response.get('msg')}")
        print(f"响应数据结构: {json.dumps(response, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. 调试获取部署列表
    print("2. 调试获取部署列表:")
    try:
        response = client._make_request("GET", "/api/v1/dev/deployment/list")
        print(f"响应状态: {response.get('code')}")
        print(f"响应消息: {response.get('msg')}")
        print(f"响应数据结构: {json.dumps(response, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. 调试获取GPU库存
    print("3. 调试获取GPU库存:")
    try:
        response = client._make_request("POST", "/api/v1/dev/machine/region/gpu_stock", 
                                      data={"region_sign": "westDC2", "cuda_v": 118})
        print(f"响应状态: {response.get('code')}")
        print(f"响应消息: {response.get('msg')}")
        print(f"响应数据结构: {json.dumps(response, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. 调试获取账户余额
    print("4. 调试获取账户余额:")
    try:
        response = client._make_request("POST", "/api/v1/dev/wallet/balance")
        print(f"响应状态: {response.get('code')}")
        print(f"响应消息: {response.get('msg')}")
        print(f"响应数据结构: {json.dumps(response, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    debug_api_responses() 