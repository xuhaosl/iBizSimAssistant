from typing import List, Dict, Any
from functools import lru_cache
from src.utils.logger import get_logger


class PerformanceOptimizer:
    """
    性能优化工具类
    """
    
    def __init__(self):
        self.logger = get_logger()
        self.cache_enabled = True
    
    @staticmethod
    @lru_cache(maxsize=128)
    def cached_selector(selector: str) -> str:
        """
        缓存选择器字符串，减少重复字符串的内存占用
        
        Args:
            selector: CSS选择器
            
        Returns:
            缓存的选择器字符串
        """
        return selector
    
    def batch_extract(self, selectors: List[str], 
                    extract_func: callable) -> Dict[str, Any]:
        """
        批量提取数据，减少页面操作次数
        
        Args:
            selectors: 选择器列表
            extract_func: 提取函数
            
        Returns:
            提取结果字典
        """
        results = {}
        
        for selector in selectors:
            try:
                cached_selector = self.cached_selector(selector)
                results[selector] = extract_func(cached_selector)
            except Exception as e:
                self.logger.error(f"Failed to extract {selector}: {e}")
                results[selector] = None
        
        return results
    
    def optimize_wait_time(self, base_timeout: int, 
                         element_count: int = 1) -> int:
        """
        根据元素数量动态调整等待时间
        
        Args:
            base_timeout: 基础超时时间
            element_count: 元素数量
            
        Returns:
            优化后的超时时间
        """
        if element_count <= 1:
            return base_timeout
        
        optimized_timeout = min(base_timeout * (1 + element_count * 0.1), 30000)
        self.logger.debug(f"Optimized timeout: {optimized_timeout}ms for {element_count} elements")
        return int(optimized_timeout)
    
    def parallel_process(self, items: List[Any], 
                      process_func: callable,
                      batch_size: int = 10) -> List[Any]:
        """
        分批处理数据，避免内存溢出
        
        Args:
            items: 要处理的项目列表
            process_func: 处理函数
            batch_size: 批次大小
            
        Returns:
            处理结果列表
        """
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            try:
                batch_results = [process_func(item) for item in batch]
                results.extend(batch_results)
            except Exception as e:
                self.logger.error(f"Failed to process batch {i//batch_size}: {e}")
                results.extend([None] * len(batch))
        
        return results
    
    def deduplicate_data(self, data: List[Any], 
                      key_func: callable = lambda x: x) -> List[Any]:
        """
        去重数据
        
        Args:
            data: 数据列表
            key_func: 键函数
            
        Returns:
            去重后的数据列表
        """
        seen = set()
        unique_data = []
        
        for item in data:
            key = key_func(item)
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        self.logger.debug(f"Deduplicated {len(data)} items to {len(unique_data)} items")
        return unique_data
    
    def compress_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        压缩数据，移除空值和None值
        
        Args:
            data: 数据字典
            
        Returns:
            压缩后的数据字典
        """
        compressed = {}
        
        for key, value in data.items():
            if value is not None and value != '':
                compressed[key] = value
        
        removed_count = len(data) - len(compressed)
        if removed_count > 0:
            self.logger.debug(f"Removed {removed_count} empty values from data")
        
        return compressed
    
    def optimize_memory(self):
        """
        优化内存使用
        """
        self.cached_selector.cache_clear()
        self.logger.debug("Cleared selector cache")
    
    def get_performance_stats(self) -> Dict[str, int]:
        """
        获取性能统计信息
        
        Returns:
            性能统计字典
        """
        cache_info = self.cached_selector.cache_info()
        
        return {
            'cache_hits': cache_info.hits,
            'cache_misses': cache_info.misses,
            'cache_size': cache_info.currsize,
            'cache_maxsize': cache_info.maxsize
        }


class BatchProcessor:
    """
    批量处理器，用于批量操作优化
    """
    
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.logger = get_logger()
    
    def process_in_batches(self, items: List[Any], 
                         process_func: callable) -> List[Any]:
        """
        分批处理项目
        
        Args:
            items: 项目列表
            process_func: 处理函数
            
        Returns:
            处理结果列表
        """
        results = []
        total_batches = (len(items) + self.batch_size - 1) // self.batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(items))
            batch = items[start_idx:end_idx]
            
            self.logger.debug(f"Processing batch {batch_num + 1}/{total_batches}")
            
            try:
                batch_results = [process_func(item) for item in batch]
                results.extend(batch_results)
            except Exception as e:
                self.logger.error(f"Failed to process batch {batch_num + 1}: {e}")
                results.extend([None] * len(batch))
        
        return results
    
    def set_batch_size(self, batch_size: int):
        """
        设置批次大小
        
        Args:
            batch_size: 新的批次大小
        """
        self.batch_size = batch_size
        self.logger.debug(f"Batch size set to {batch_size}")


class LazyLoader:
    """
    懒加载器，延迟加载数据
    """
    
    def __init__(self, load_func: callable):
        self.load_func = load_func
        self._loaded = False
        self._data = None
        self.logger = get_logger()
    
    def load(self) -> Any:
        """
        加载数据
        
        Returns:
            加载的数据
        """
        if not self._loaded:
            self.logger.debug("Lazy loading data...")
            self._data = self.load_func()
            self._loaded = True
        
        return self._data
    
    def is_loaded(self) -> bool:
        """
        检查数据是否已加载
        
        Returns:
            是否已加载
        """
        return self._loaded
    
    def reset(self):
        """
        重置加载状态
        """
        self._loaded = False
        self._data = None
        self.logger.debug("Lazy loader reset")
