from src.utils.logger import get_logger

logger = get_logger(__name__)

class BetterStudentError(Exception):
    """Base exception class for Better-Student"""
    pass

class SpeechRecognitionError(BetterStudentError):
    """Exception raised for speech recognition errors"""
    pass

class TextAnalysisError(BetterStudentError):
    """Exception raised for text analysis errors"""
    pass

class DataStorageError(BetterStudentError):
    """Exception raised for data storage errors"""
    pass

class AIIntegrationError(BetterStudentError):
    """Exception raised for AI integration errors"""
    pass

class TermManagerError(BetterStudentError):
    """Exception raised for term manager errors"""
    pass

class UIError(BetterStudentError):
    """Exception raised for UI errors"""
    pass

def handle_error(error, context=None):
    """Handle errors gracefully"""
    error_type = type(error).__name__
    error_message = str(error)
    
    if context:
        logger.error(f"Error in {context}: {error_type} - {error_message}")
    else:
        logger.error(f"Error: {error_type} - {error_message}")
    
    # 可以根据错误类型进行不同的处理
    if isinstance(error, SpeechRecognitionError):
        # 处理语音识别错误
        pass
    elif isinstance(error, TextAnalysisError):
        # 处理文本分析错误
        pass
    elif isinstance(error, DataStorageError):
        # 处理数据存储错误
        pass
    elif isinstance(error, AIIntegrationError):
        # 处理AI集成错误
        pass
    elif isinstance(error, TermManagerError):
        # 处理术语管理错误
        pass
    elif isinstance(error, UIError):
        # 处理UI错误
        pass
    else:
        # 处理其他错误
        pass
    
    return error_message