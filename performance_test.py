#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
性能测试脚本
用于比较新旧文本处理流程的性能
"""

import time
from src.core.ai_integration import AIIntegration

# 测试文本
test_texts = [
    "人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。什么是机器学习？",
    "Python是一种广泛使用的解释型、高级和通用的编程语言。它支持多种编程范式，包括结构化、面向对象和函数式编程。",
    "数据结构是计算机中存储、组织数据的方式。常见的数据结构包括数组、链表、栈、队列、树和图等。",
    "算法是解决问题的步骤集合。常见的算法包括排序算法、搜索算法、图算法等。什么是时间复杂度？",
    "计算机网络是指将分散的计算机通过通信设备和传输介质连接起来，实现信息交换和资源共享的系统。"
]

def test_ai_integration_performance():
    """测试AI集成模块的性能"""
    ai = AIIntegration()
    total_time = 0
    total_terms = 0
    total_questions = 0
    
    print("=== 测试AI集成模块性能 ===")
    
    for i, text in enumerate(test_texts):
        start_time = time.time()
        
        # 分析文本
        result = ai.analyze_text(text)
        
        end_time = time.time()
        
        execution_time = end_time - start_time
        total_time += execution_time
        total_terms += len(result['terms'])
        total_questions += len(result['questions'])
        
        print(f"测试文本 {i+1}:")
        print(f"  处理时间: {execution_time:.4f} 秒")
        print(f"  识别术语: {len(result['terms'])} 个")
        print(f"  识别问题: {len(result['questions'])} 个")
        print(f"  术语列表: {result['terms']}")
        print(f"  问题列表: {result['questions']}")
        print()
    
    average_time = total_time / len(test_texts)
    print("=== 性能测试结果 ===")
    print(f"平均处理时间: {average_time:.4f} 秒/文本")
    print(f"总处理时间: {total_time:.4f} 秒")
    print(f"平均识别术语数: {total_terms / len(test_texts):.1f} 个/文本")
    print(f"平均识别问题数: {total_questions / len(test_texts):.1f} 个/文本")
    
    return {
        'average_time': average_time,
        'total_time': total_time,
        'average_terms': total_terms / len(test_texts),
        'average_questions': total_questions / len(test_texts)
    }

if __name__ == "__main__":
    test_ai_integration_performance()
