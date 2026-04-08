# Better-Student - 文本处理流程优化计划

## 项目背景
当前项目采用"Spacy文本分析预处理+大模型内容处理"的两步操作流程。为了简化系统架构，提高处理效率，需要将其优化为"大模型端到端处理"的单步流程。

## 优化目标
1. 移除Spacy预处理环节，减少系统依赖
2. 调整大模型输入格式，直接处理原始文本
3. 确保处理速度、资源占用和分析准确性不低于原流程
4. 保留核心分析能力，同时简化操作步骤

## 任务分解与优先级

### [ ] 任务1: 分析现有文本处理流程
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 详细分析现有文本处理流程的各个组件
  - 识别Spacy在流程中的具体作用
  - 确定需要保留的核心功能
- **Success Criteria**:
  - 完整理解现有流程的工作原理
  - 明确Spacy的使用场景和功能
- **Test Requirements**:
  - `programmatic` TR-1.1: 列出所有使用Spacy的代码位置
  - `human-judgement` TR-1.2: 确认核心功能需求

### [ ] 任务2: 调整AI集成模块，支持直接处理原始文本
- **Priority**: P0
- **Depends On**: 任务1
- **Description**:
  - 修改 `src/core/ai_integration.py`，增强其直接处理原始文本的能力
  - 实现术语识别和问题识别的大模型版本
  - 优化大模型输入提示，确保准确识别术语和问题
- **Success Criteria**:
  - AI集成模块能够直接处理原始文本
  - 能够识别文本中的术语和问题
  - 处理结果质量不低于原Spacy处理结果
- **Test Requirements**:
  - `programmatic` TR-2.1: 测试术语识别准确率
  - `programmatic` TR-2.2: 测试问题识别准确率
  - `programmatic` TR-2.3: 测试处理速度和资源占用

### [ ] 任务3: 修改术语管理模块，移除Spacy依赖
- **Priority**: P1
- **Depends On**: 任务2
- **Description**:
  - 修改 `src/core/term_manager.py`，使用新的AI集成模块处理术语
  - 移除对 `TextAnalyzer` 的依赖
  - 调整术语处理流程，直接调用大模型识别术语
- **Success Criteria**:
  - 术语管理模块能够正常工作
  - 术语识别结果准确
  - 不再依赖Spacy
- **Test Requirements**:
  - `programmatic` TR-3.1: 测试术语处理功能
  - `programmatic` TR-3.2: 验证Spacy依赖已移除

### [ ] 任务4: 更新分析面板，使用新的文本处理流程
- **Priority**: P1
- **Depends On**: 任务2
- **Description**:
  - 修改 `src/ui/analysis_panel.py`，使用新的AI集成模块进行文本分析
  - 移除对 `TextAnalyzer` 的依赖
  - 更新UI逻辑，适应新的处理流程
- **Success Criteria**:
  - 分析面板能够正常工作
  - 文本分析结果准确
  - UI响应流畅
- **Test Requirements**:
  - `programmatic` TR-4.1: 测试分析面板功能
  - `human-judgement` TR-4.2: 验证UI响应速度和用户体验

### [ ] 任务5: 更新语音面板，使用新的术语处理流程
- **Priority**: P1
- **Depends On**: 任务3
- **Description**:
  - 修改 `src/ui/speech_panel.py`，使用新的术语管理模块
  - 调整语音识别后的文本处理流程
  - 确保术语标记功能正常工作
- **Success Criteria**:
  - 语音面板能够正常工作
  - 术语标记功能准确
  - 处理速度不低于原流程
- **Test Requirements**:
  - `programmatic` TR-5.1: 测试语音识别后的术语处理
  - `human-judgement` TR-5.2: 验证语音处理流畅度

### [ ] 任务6: 移除TextAnalyzer模块和Spacy依赖
- **Priority**: P2
- **Depends On**: 任务3, 任务4, 任务5
- **Description**:
  - 移除 `src/core/text_analyzer.py` 中对Spacy的依赖
  - 简化TextAnalyzer模块，或完全移除
  - 更新 `requirements.txt`，移除Spacy相关依赖
- **Success Criteria**:
  - 项目不再依赖Spacy
  - 所有功能正常工作
  - 依赖项列表已更新
- **Test Requirements**:
  - `programmatic` TR-6.1: 验证Spacy已从依赖中移除
  - `programmatic` TR-6.2: 测试所有功能正常运行

### [ ] 任务7: 更新测试环境脚本
- **Priority**: P2
- **Depends On**: 任务6
- **Description**:
  - 修改 `test_environment.py`，移除Spacy模型测试
  - 更新依赖测试列表
  - 确保测试脚本能够正确验证新的环境配置
- **Success Criteria**:
  - 测试脚本能够正常运行
  - 不再测试Spacy模型
  - 能够正确验证新的环境配置
- **Test Requirements**:
  - `programmatic` TR-7.1: 测试脚本能够正常运行
  - `programmatic` TR-7.2: 验证依赖项测试结果正确

### [ ] 任务8: 性能测试和优化
- **Priority**: P2
- **Depends On**: 任务2, 任务3, 任务4, 任务5
- **Description**:
  - 测试新的端到端处理流程的性能
  - 与原流程进行对比，确保性能不下降
  - 优化大模型提示，提高处理效率
- **Success Criteria**:
  - 处理速度不低于原流程
  - 资源占用不高于原流程
  - 分析准确性不低于原流程
- **Test Requirements**:
  - `programmatic` TR-8.1: 测试处理速度
  - `programmatic` TR-8.2: 测试资源占用
  - `programmatic` TR-8.3: 测试分析准确性

## 实施步骤
1. 首先完成任务1，全面了解现有流程
2. 然后实施任务2，调整AI集成模块
3. 依次实施任务3、4、5，更新相关模块
4. 实施任务6，移除Spacy依赖
5. 实施任务7，更新测试环境脚本
6. 最后实施任务8，进行性能测试和优化

## 风险评估
1. **大模型处理延迟**：可能会比本地Spacy处理慢，需要优化提示和处理逻辑
2. **分析准确性**：需要确保大模型在术语和问题识别上的准确性
3. **API调用成本**：增加大模型调用可能会增加API使用成本
4. **网络依赖**：相比本地Spacy，更依赖网络连接

## 应对策略
1. **优化提示工程**：设计高效的提示，减少大模型处理时间
2. **缓存机制**：对常见术语和问题建立缓存，减少重复调用
3. **批量处理**：合并多个分析请求，减少API调用次数
4. **错误处理**：增加网络错误处理和重试机制

## 预期成果
1. 简化的系统架构，减少依赖项
2. 统一的文本处理流程，提高可维护性
3. 保持或提高分析准确性
4. 优化处理速度和资源占用