### 安装

cd Tracking

pip install -r requirements.txt

pip install cython

pip install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

pip install cython_bbox

### 目录格式

```
./
   |——————GUI #PythonQT文件
   |
   |
   └——————Output#模型输出文件
   |
   |
   |
   |
   └——————Tracking#算法文件
   |        └——————train
   |        └——————test
   └——————main #主程序文件
```
