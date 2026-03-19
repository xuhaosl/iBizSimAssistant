import time
from functools import wraps
from typing import Callable, Any
from src.utils.logger import get_logger


def retry(max_attempts: int = 3, delay: float = 1.0, 
          exceptions: tuple = (Exception,), 
          backoff_factor: float = 2.0):
    """
    重试装饰器
    
    Args:
        max_attempts: 最大重试次数
        delay: 初始延迟时间（秒）
        exceptions: 需要重试的异常类型
        backoff_factor: 退避因子，每次重试延迟时间乘以该因子
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = get_logger()
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (backoff_factor ** attempt)
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. "
                            f"Retrying in {wait_time:.2f} seconds..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                        )
            
            raise last_exception
        return wrapper
    return decorator


class RetryManager:
    """
    重试管理器，提供更灵活的重试控制
    """
    
    def __init__(self, max_attempts: int = 3, delay: float = 1.0,
                 backoff_factor: float = 2.0):
        self.max_attempts = max_attempts
        self.delay = delay
        self.backoff_factor = backoff_factor
        self.logger = get_logger()
    
    def execute(self, func: Callable, *args, 
               exceptions: tuple = (Exception,), **kwargs) -> Any:
        """
        执行函数并处理重试
        
        Args:
            func: 要执行的函数
            *args: 函数参数
            exceptions: 需要重试的异常类型
            **kwargs: 函数关键字参数
            
        Returns:
            函数执行结果
            
        Raises:
            最后一次尝试的异常
        """
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                if attempt < self.max_attempts - 1:
                    wait_time = self.delay * (self.backoff_factor ** attempt)
                    self.logger.warning(
                        f"Attempt {attempt + 1}/{self.max_attempts} failed: {e}. "
                        f"Retrying in {wait_time:.2f} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    self.logger.error(
                        f"All {self.max_attempts} attempts failed: {e}"
                    )
        
        raise last_exception
    
    def execute_with_callback(self, func: Callable, callback: Callable,
                           *args, exceptions: tuple = (Exception,), **kwargs) -> Any:
        """
        执行函数并在每次失败后调用回调函数
        
        Args:
            func: 要执行的函数
            callback: 回调函数，接收当前尝试次数和异常
            *args: 函数参数
            exceptions: 需要重试的异常类型
            **kwargs: 函数关键字参数
            
        Returns:
            函数执行结果
            
        Raises:
            最后一次尝试的异常
        """
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                callback(attempt + 1, e)
                
                if attempt < self.max_attempts - 1:
                    wait_time = self.delay * (self.backoff_factor ** attempt)
                    self.logger.warning(
                        f"Attempt {attempt + 1}/{self.max_attempts} failed: {e}. "
                        f"Retrying in {wait_time:.2f} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    self.logger.error(
                        f"All {self.max_attempts} attempts failed: {e}"
                    )
        
        raise last_exception


class ErrorHandler:
    """
    错误处理器，提供统一的错误处理机制
    """
    
    def __init__(self):
        self.logger = get_logger()
        self.error_handlers = {}
    
    def register_handler(self, exception_type: type, handler: Callable):
        """
        注册特定异常类型的处理器
        
        Args:
            exception_type: 异常类型
            handler: 处理函数
        """
        self.error_handlers[exception_type] = handler
    
    def handle(self, exception: Exception, context: dict = None) -> bool:
        """
        处理异常
        
        Args:
            exception: 异常对象
            context: 上下文信息
            
        Returns:
            是否成功处理异常
        """
        context = context or {}
        
        for exception_type, handler in self.error_handlers.items():
            if isinstance(exception, exception_type):
                try:
                    return handler(exception, context)
                except Exception as e:
                    self.logger.error(f"Error handler failed: {e}")
                    return False
        
        self.logger.exception(f"Unhandled exception: {exception}")
        return False
    
    def handle_with_fallback(self, exception: Exception, 
                           fallback: Callable, context: dict = None) -> Any:
        """
        处理异常，如果处理失败则执行回退函数
        
        Args:
            exception: 异常对象
            fallback: 回退函数
            context: 上下文信息
            
        Returns:
            处理结果或回退函数的返回值
        """
        if not self.handle(exception, context):
            self.logger.info("Executing fallback function")
            return fallback()
        
        return None


def safe_execute(func: Callable, default_value: Any = None,
                exceptions: tuple = (Exception,), 
                log_error: bool = True) -> Any:
    """
    安全执行函数，捕获异常并返回默认值
    
    Args:
        func: 要执行的函数
        default_value: 发生异常时的默认返回值
        exceptions: 要捕获的异常类型
        log_error: 是否记录错误日志
        
    Returns:
        函数执行结果或默认值
    """
    logger = get_logger()
    
    try:
        return func()
    except exceptions as e:
        if log_error:
            logger.error(f"Function {func.__name__} failed: {e}")
        return default_value
