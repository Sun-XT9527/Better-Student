# Better-Student

一个基于Python的语音转文字与智能分析软件，帮助学生更高效地学习和理解课程内容。

## 项目简介

Better-Student是一个专为学生设计的AI辅助工具，旨在提升听课效率和学习效果。通过集成千问语音转文字和问答模型，它可以实时将课堂内容转化为文字，自动识别专业术语并提供解释，检测教师提出的问题并生成答案，让学习变得更加轻松高效。~~让你装波大的~~

## 功能特点

- **实时语音转文字**：集成千问语音转文字模型，实现低延迟的实时文字输出（支持自定义配置api）
- **文本实时保存**：结构化存储语音转文字结果，包含时间戳等元数据，支持数据持久化
- **专业术语解释**：自动识别文本中的专业名词，提供准确的定义和解释
- **问题检测与处理**：识别教师提出的问题，自动检索上下文信息并生成答案
- **联网搜索增强**：针对检测到的问题，进行联网搜索获取相关信息
- **术语掌握状态管理**：存储专业术语，支持标记掌握状态，根据掌握状态展示不同颜色和解释方式
- **友好的用户界面**：清晰展示语音转文字结果、专业术语解释和问题答案

## 技术栈

- **开发语言**：Python 3.8+
- **音频处理**：PyAudio
- **AI模型**：千问语音转文字API、千问问答API
- **数据存储**：SQLite
- **用户界面**：PyQt5
- **文本分析**：NLTK/Spacy
- **网络请求**：Requests

## 安装和使用

### 前置要求

- Python 3.8+
- pip 20.0+
- 麦克风设备
- 网络连接（用于API调用）

### 安装步骤

1. 克隆项目到本地
   ```bash
   git clone https://github.com/yourusername/Better-Student.git
   cd Better-Student
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量
   ```bash
   # 复制环境变量模板文件
   cp .env.example .env
   # 编辑.env文件，填写千问API密钥等配置
   ```

4. 运行应用
   ```bash
   python src/main.py
   ```

## 项目结构

```
Better-Student/
├── src/
│   ├── core/
│   │   ├── speech_recognition.py  # 语音识别核心模块
│   │   ├── text_analyzer.py      # 文本分析核心模块
│   │   ├── data_storage.py       # 数据存储模块
│   │   ├── ai_integration.py     # AI模型集成模块
│   │   └── term_manager.py       # 专业术语管理模块
│   ├── utils/
│   │   ├── config.py             # 配置管理
│   │   ├── logger.py             # 日志管理
│   │   └── error_handling.py     # 错误处理
│   ├── ui/
│   │   ├── main_window.py        # 主界面
│   │   ├── speech_panel.py       # 语音识别面板
│   │   ├── analysis_panel.py     # 分析结果面板
│   │   ├── term_panel.py         # 术语管理面板
│   │   └── settings_panel.py     # 设置面板
│   ├── api/
│   │   ├── qwen_api.py           # 千问模型API封装
│   │   └── search_api.py         # 搜索API封装
│   └── main.py                   # 应用入口
├── requirements.txt              # 依赖管理
├── setup.py                      # 安装脚本
├── .env.example                  # 环境变量模板
└── README.md                     # 项目说明
```

## 贡献指南

欢迎对Better-Student项目贡献代码和建议！以下是贡献流程：

1. Fork本项目
2. 创建一个新的分支 (`git checkout -b feature/your-feature`)
3. 提交你的更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 打开一个Pull Request

## 许可证


## 联系方式

- 项目维护者：Sun-XT9527
- 邮箱：179635492@qq.com
- GitHub：https://github.com/Sun-XT9527/Better-Student.git

## 鸣谢

感谢所有为Better-Student项目做出贡献的开发者和用户！

---

*让学习变得更简单，让学生变得更优秀* 🚀