map reduce

环境配置
cd yaml
# 部署Redis
kubectl apply -f redis.yaml
# 部署MinIO
kubectl apply -f minio.yaml
注意事项：
namespace：默认为default，建议改为自己的ns以免冲突
nodeName：请改成自己集群的节点，或者删除不绑定
minio的挂载路径：默认为/mnt/minio，请修改或者自行创建相关目录
minio的用户名和密码：有需要请修改MINIO_ROOT_USER和MINIO_ROOT_PASSWORD，并相应修改下文3中的函数中的配置

数据生成
cd gen_data
# 编译
cd .
# 生成数据，参数依次代表模型名，文件数量，文件行数，每行词数，输出目录，可根据需要更改
./gen_text_data.sh lda_wiki1w 5 8000 2000 wc-100M-5/
# 上传数据至存储系统，注意修改对应参数。请自行调用make_bucket API创建数据桶。
python3 upload.py

实验运行
cd functions
# 编译镜像
faashwh-cli build -f wc-mapper.yml
faashwh-cli build -f wc-reducer.yml
# 部署
faashwh-cli deploy -f wc-mapper.yml
faashwh-cli deploy -f wc-reducer.yml
# 运行
python3 client.py
# 清理中间数据
python3 clean.py
注意事项：
数据存储：目前Redis和Minio的配置使用默认值，有更改请更新代码并重新编译部署。当前使用MinIO作为输入和输出的存储系统，Redis作为中间数据的存储。
函数配置：目前锁定5个实例和部署位置。节点限制可自行更改或直接删除。因没有实现输入文件自动分区，所以锁定5个函数实例，暂不支持自定义实例数量。如需修改，需要相应以下参数
1：gen_text_data中生成文件数量的参数
2：upload.py脚本中的分区数量
3：yml文件中实例的数量
4：client脚本中mapper_num和reducer_num变量
客户端调用：目前使用默认的输入目录。有需要请自行更改。
中间数据清理：请自行更新为本地Redis服务的IP。