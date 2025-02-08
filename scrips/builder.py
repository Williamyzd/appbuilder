# -*- coding: utf-8 -*-
import subprocess,os,json
code_path = 'gits/code.json'
base_registry = 'registry.cn-hangzhou.aliyuncs.com/reg_pub/'
## 修改为自己的账户名称
ghcr_registry = 'ghcr.io/williamyzd/'
import datetime
def get_safe_value(dic:dict,key):
    value = None
    if key in dic.keys():
        value = dic[key]
        if len(value) <= 0:
            value = None
            print('{} 值为空'.format(key))
    else:
        print('{} 不存在'.format(key))  
    return value
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
        url = code['url']
        if os.path.exists(app_name):
            os.system('cd ~ && rm -rf {}'.format(app_name))
        num,rs = subprocess.getstatusoutput('git clone {} {} '.format(url,app_name))
        print('git clone {}'.format(url))
        if num != 0:
            print('{} 下载失败,原因：{}'.format(url,rs))
            return
        else:
            print('{} 下载成功'.format(url))
        diy_cmd = get_safe_value(code,'diy_cmd')
        build_cmd = diy_cmd if diy_cmd else get_safe_value(code,'cmd')
        print("开始构建 {}".format(app_name))
        tag = ghcr_registry +app_name+":" + code['tag']
        if get_safe_value(code,'need_time_tag'):
            ct = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            tag = tag + '-' + ct
        maps ={
            "${workdir}":code["workdir"],
            "${file}":code["file"],
            "${tag}":tag
        }
        for k,v in maps.items():
            build_cmd = build_cmd.replace(k,v)
        build_cmd = build_cmd + "  && docker push {} ".format(tag) 
        num,rs = subprocess.getstatusoutput(build_cmd)
        if num !=0 :
            print('{} 构建失败,原因：{}'.format(build_cmd,rs))
            return
        else:
            print('{} 构建成功'.format(build_cmd))
        if code['need_aliyun'] == True:
            new_tag = base_registry + tag
            num,rs = subprocess.getstatusoutput('docker tag {} {} && docker push {}'.format(tag,new_tag,new_tag))
            if num !=0 :
                print('{} 推送阿里云失败,原因：{}'.format(tag,rs))
                return
            else:
                print('{} 推送阿里云成功'.format(new_tag))
        
    
clone_push(read_codes(code_path))
        










    
