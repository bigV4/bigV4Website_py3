# 简介
一个网站
## 功能
* 获得ip和请求头等信息`/ifconfig`
* 
## 结构
* 按照 分区 组织。同一个功能的模板，静态文件，视图都在一个文件夹内。比如api、auth、main三个模块。

```
README.md - 仓库的说明，比如该项目的介绍等
app - 项目的主要功能实现
config.py - 项目的配置
fabfile.py - 使用Fabric3完成项目发布工作的脚本
manage.py - 基于Flask-Script扩展的命令行脚本
requirements - 该项目所依赖的第三方包
unit_tests - 单元测试相关代码
```

# 如何使用
## 依赖
### 主依赖
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install flask # 可以使用豆瓣的源例如：pip3 install flask -i https://pypi.doubanio.com/simple
(venv) $ pip3 install flask-restful
```



### 验证码识别依赖
```
(venv) $ pip3 install torch -i https://pypi.doubanio.com/simple
(venv) $ pip3 install torchvision -i https://pypi.doubanio.com/simple
(venv) $ pip3 install captcha -i https://pypi.doubanio.com/simple
(venv) $ pip3 install matplotlib -i https://pypi.doubanio.com/simple
(venv) $ pip3 install alphabet -i https://pypi.doubanio.com/simple
```
* 安装成功后发现报错：
```
>>> import torch
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    import torch
  File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/torch/__init__.py", line 97, in <module>
    from torch._C import *
ImportError: dlopen(/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/torch/_C.cpython-38-darwin.so, 9): Library not loaded: @rpath/libc++.1.dylib
  Referenced from: /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/torch/_C.cpython-38-darwin.so
  Reason: image not found
```
* 解决:
`libc++.1.dylib`在 `/usr/lib`下，使用 `install_name_tool`

```
install_name_tool -add_rpath /usr/lib /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/torch/_C.cpython-38-darwin.so
```

* brew太慢，brew支持全局socks代理使用前加上这一句：`export ALL_PROXY=socks5://127.0.0.1:1080`


# git管理
## 通过“.gitignore”文件
一般来说每个Git项目中都需要一个“.gitignore”文件，这个文件的作用就是告诉Git哪些文件不需要添加到版本管理中。
实际项目中，很多文件都是不需要版本管理的，比如Python的.pyc文件和一些包含密码的配置文件等等。
这个文件的内容是一些规则，Git会根据这些规则来判断是否将文件添加到版本控制中。
最后需要强调的一点是，如果你不慎在创建.gitignore文件之前就push了项目，那么即使你在.gitignore文件中写入新的过滤规则，这些规则也不会起作用,Git仍然会对所有文件进行版本管理。

在代码目录下建立.gitignore文件：vim .gitignore ,内容如下：
```
#过滤数据库文件、sln解决方案文件、配置文件  
*.mdb
*.ldb
*.sln
*.config

#过滤文件夹Debug,Release,obj,venv
Debug/  
Release/  
obj/  
venv/
```

然后调用`git add . `，执行 `git commit`即可。

## 命令删除github的文件

在github上只能删除仓库,却无法删除文件夹或文件, 所以只能通过命令来解决

首先进入你的master文件夹下, Git Bash Here ,打开命令窗口
```
$ git --help                    # 帮助命令
$ git pull origin master        # 将远程仓库里面的项目拉下来
$ ls                            # 查看有哪些文件夹
$ git rm -r --cached target     # 删除target文件夹
$ git commit -m '删除了target'   # 提交,添加操作说明
$ git push -u origin master     # 将本次更改更新到github项目上去
```
————————————————————————————————————————————————
注:本地项目中的target文件夹不收操作影响,删除的只是远程仓库中的target, 可放心删除，每次增加文件或删除文件，都要commit 然后直接 `git push -u origin master`，就可以同步到github上了
示例：`https://api.github.com/repos/用户名/仓库名`