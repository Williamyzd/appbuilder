# appbuilder
打镜像专用
根据代码仓库打镜像
编辑 gits/gits.txt 文件，添加如下信息（默认数组，支持若干个）：
```
[{
    "name": "llama.cpp", # 镜像名称
    "tag": "cuda-11.8.0", # 镜像 tag
    "file": ".devops/cuda.Dockerfile", # Dockerfile 路径
    "workdir": "llama.cpp", 
    "url": "https://github.com/Williamyzd/llama.cpp.git", # 代码仓库地址
    "need_aliyun": false, # 是否需要推送阿里云镜像仓库，默认为 false
    "need_time_tag":true, # 是否需要打时间戳 tag，默认为 true 在这种情况下，镜像名称为 name:tag + 时间戳
    "cmd": "cd ${workdir} && docker build -t ${tag} -f ${file} .", # 默认的镜像构建命令，不要改动
    "diy_cmd":""  # 如果需要特别定制命令，写在这里，默认为空 不为空时 cmd 命令失效
}]

```
注意前提：
* 如使用 github actions 构建，需要配置好阿里云镜像仓库的账号密码（在仓库的 secrets 中配置 DOCKER_USERNAME 和 DOCKER_PASSWORD 两个环境变量）。同时也需要配置 github 账号的token（在仓库的 secrets 中配置 GITHUB_TOKEN 环境变量）。
* 如果本地该脚本，请提前登录对应的镜像仓库
基本处理逻辑：
* 拉取代码
* 执行 cmd 指定的命令 or diy_cmd 指定的命令
* 默认会打ghcr.io 镜像仓库镜像。镜像前缀在scripts/build_image.sh 中指定为：ghcr.io/github账户名/
* 如果 need_aliyun 为 true，则会额外执行以下操作：
    - 镜像打 tag，镜像名称为 name:tag + 时间戳
    - push 镜像到阿里云镜像仓库
