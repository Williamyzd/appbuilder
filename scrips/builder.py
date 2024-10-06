# -*- coding: utf-8 -*-
import subprocess,os,json
code_path = 'gits/code.json'
base_registry = 'registry.cn-hangzhou.aliyuncs.com/reg_pub/'
def read_codes(code_path):
    """
    读取代码仓库，返回仓库列表
    
    Args:
        code_path (str): 代码文件路径
    
    Returns:
        list: 代码列表
    
    """
    with open(code_path, 'r') as f:
        codes = json.load(f)
    return codes
print(read_codes(code_path))

def clone_push(codes):
    """
    克隆并推送镜像到指定的仓库
    
    Args:
        codes (list): 包含需要克隆和推送的镜像信息的列表
    
    Returns:
        None
    
    """
    for code in codes:
        if len(code) <=0:
            return
        app_name = code['name']
        if os.path.exists(app_name):
            os.system('cd ~ && rm -rf {}'.format(app_name))
        num,rs = subprocess.getstatusoutput('git clone {} {} '.format(code,app_name))
        print('git clone {}'.format(code))
        if num != 0:
            print('{} 下载失败,原因：{}'.format(code,rs))
            return
        else:
            print('{} 下载成功'.format(code))
        build_cmd = code['cmd']
        new_tag = base_registry + code['tag']
        num,rs = subprocess.getstatusoutput(build_cmd + " && docker tag {} {}".format(code['tag'],new_tag))
        if num !=0 :
            print('{} 构建失败,原因：{}'.format(build_cmd),rs)
            return
        else:
            print('{} 构建成功'.format(build_cmd))
        num,rs = subprocess.getstatusoutput('docker push {}'.format(new_tag))
        if num !=0 :
            print('{} 推送失败,原因：{}'.format(base_registry+app_name,rs))
            return
        else:
            print('{} 推送成功'.format(base_registry+app_name))

clone_push(read_codes(code_path))
        










    