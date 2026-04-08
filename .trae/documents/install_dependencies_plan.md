# 安装项目依赖计划

## [ ] 任务 1: 安装核心依赖包
- **优先级**: P0
- **依赖**: 无
- **描述**:
  - 安装项目所需的所有核心依赖包
  - 使用pip install -r requirements.txt命令
- **成功标准**:
  - 所有核心依赖包安装成功
  - 测试脚本能够成功导入所有依赖包
- **测试要求**:
  - `programmatic` TR-1.1: 运行pip install -r requirements.txt命令，无错误输出
  - `programmatic` TR-1.2: 运行test_environment.py脚本，依赖包测试通过
- **注意事项**:
  - 确保在激活的虚拟环境中运行命令
  - 可能需要管理员权限安装某些依赖

## [ ] 任务 2: 安装Spacy中文模型
- **优先级**: P0
- **依赖**: 任务 1
- **描述**:
  - 安装Spacy中文模型zh_core_web_sm
  - 使用python -m spacy download zh_core_web_sm命令
- **成功标准**:
  - Spacy中文模型安装成功
  - 测试脚本能够成功加载Spacy中文模型
- **测试要求**:
  - `programmatic` TR-2.1: 运行python -m spacy download zh_core_web_sm命令，无错误输出
  - `programmatic` TR-2.2: 运行test_environment.py脚本，Spacy模型测试通过
- **注意事项**:
  - 确保在激活的虚拟环境中运行命令
  - 可能需要网络连接下载模型

## [ ] 任务 3: 配置环境变量
- **优先级**: P1
- **依赖**: 任务 1
- **描述**:
  - 从.env.example复制并创建.env文件
  - 配置必要的环境变量，如API密钥等
- **成功标准**:
  - .env文件创建成功
  - 环境变量配置正确
- **测试要求**:
  - `programmatic` TR-3.1: .env文件存在且包含必要的配置项
  - `programmatic` TR-3.2: 运行test_environment.py脚本，环境变量测试通过
- **注意事项**:
  - 需要获取千问API和搜索API的密钥
  - 确保配置项格式正确

## [ ] 任务 4: 验证环境配置
- **优先级**: P1
- **依赖**: 任务 1, 任务 2, 任务 3
- **描述**:
  - 运行test_environment.py脚本验证所有环境配置
  - 确保所有测试通过
- **成功标准**:
  - 所有测试通过
  - 项目环境配置正确
- **测试要求**:
  - `programmatic` TR-4.1: 运行test_environment.py脚本，所有测试通过
  - `human-judgment` TR-4.2: 检查测试输出，确认所有测试项都显示[OK]
- **注意事项**:
  - 确保所有依赖都已正确安装
  - 确保环境变量配置正确

## 执行顺序
1. 任务 1: 安装核心依赖包
2. 任务 2: 安装Spacy中文模型
3. 任务 3: 配置环境变量
4. 任务 4: 验证环境配置

## 命令总结
1. 安装核心依赖: `pip install -r requirements.txt`
2. 安装Spacy中文模型: `python -m spacy download zh_core_web_sm`
3. 配置环境变量: 复制.env.example为.env并编辑
4. 验证环境: `python test_environment.py`