# appbuilder
打镜像专用
1. 根据代码仓库打镜像
编辑 gits/gits.txt 文件，添加如下信息（默认数组，支持若干个）：
```
[{
    "name": "vllm", # 会根据此名字创建临时文件夹
    "tag": "vllm-cpu-env:v20241006", # build出的镜像名称
    "url": "https://github.com/vllm-project/vllm.git", # 代码仓库地址
    "cmd": "cd vllm && docker build -f Dockerfile.cpu -t vllm-cpu-env:v20241006 --shm-size=4g ." # 构建命令，需要跳转到dockerfile所在目录,可以在此指定build时需要添加的参数，-t 指定的tag 需要和前边的tag参数保持一致，否则会报错
}]
基本处理逻辑：
* 拉取代码到 name 指定的文件夹
* 执行 cmd 指定的命令
* 镜像打 tag，镜像名称为 阿里云镜像仓库地址 + tag 指定的值
* push 镜像到阿里云的镜像仓库