"""
Centralized logging configuration for the MCP Prospect Research Server.
Provides structured logging with context tracking for all operations.
"""

import json
import logging
import time
import uuid
from contextvars import ContextVar
from typing import Dict, Any, Optional

# Context variables for tracking across async operations
current_operation: ContextVar[Optional[str]] = ContextVar('current_operation', default=None)
current_prospect_id: ContextVar[Optional[str]] = ContextVar('current_prospect_id', default=None)
current_tool_name: ContextVar[Optional[str]] = ContextVar('current_tool_name', default=None)
request_id: ContextVar[Optional[str]] = ContextVar('request_id', default=None)


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs with context."""
    
    def format(self, record: logging.LogRecord) -> str:
        # Base log entry structure
        log_entry = {
            'timestamp': time.time(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add context information if available
        if current_operation.get():
            log_entry['operation'] = current_operation.get()
        
        if current_prospect_id.get():
            log_entry['prospect_id'] = current_prospect_id.get()
            
        if current_tool_name.get():
            log_entry['tool_name'] = current_tool_name.get()
            
        if request_id.get():
            log_entry['request_id'] = request_id.get()
        
        # Add exception information if present
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__ if record.exc_info[0] else None,
                'message': str(record.exc_info[1]) if record.exc_info[1] else None,
                'traceback': self.formatException(record.exc_info) if record.exc_info else None
            }
        
        # Add extra fields from the record
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
                          'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName',
                          'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
                          'processName', 'process', 'message']:
                log_entry[key] = value
        
        return json.dumps(log_entry, default=str, ensure_ascii=False)


class ContextLogger:
    """Enhanced logger with automatic context tracking."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def _log_with_context(self, level: int, message: str, **kwargs) -> None:
        """Log with automatic context inclusion."""
        extra_context = {}
        
        # Add timing information for operations
        if current_operation.get():
            extra_context['operation_context'] = {
                'operation': current_operation.get(),
                'prospect_id': current_prospect_id.get(),
                'tool_name': current_tool_name.get(),
                'request_id': request_id.get()
            }
        
        # Handle exc_info separately to avoid conflicts
        exc_info = kwargs.pop('exc_info', None)
        
        # Merge with any additional context provided
        extra_context.update(kwargs)
        
        # Log with or without exception info
        if exc_info:
            self.logger.log(level, message, exc_info=exc_info, extra=extra_context)
        else:
            self.logger.log(level, message, extra=extra_context)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with context."""
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message with context."""
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with context."""
        self._log_with_context(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message with context."""
        self._log_with_context(logging.ERROR, message, **kwargs)
    
    def exception(self, message: str, **kwargs) -> None:
        """Log exception with full context and stack trace."""
        self._log_with_context(logging.ERROR, message, exc_info=True, **kwargs)


def setup_logging(level: str = "INFO", structured: bool = True) -> None:
    """
    Configure application-wide logging.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        structured: Whether to use structured JSON logging
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    
    if structured:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> ContextLogger:
    """Get a context-aware logger for the given name."""
    return ContextLogger(name)


class OperationContext:
    """Context manager for tracking operations with automatic logging."""
    
    def __init__(self, operation: str, prospect_id: Optional[str] = None, 
                 tool_name: Optional[str] = None):
        self.operation = operation
        self.prospect_id = prospect_id
        self.tool_name = tool_name
        self.request_id = str(uuid.uuid4())
        self.start_time = None
        self.logger = get_logger(f"operation.{operation}")
    
    def __enter__(self):
        # Set context variables
        current_operation.set(self.operation)
        current_prospect_id.set(self.prospect_id)
        current_tool_name.set(self.tool_name)
        request_id.set(self.request_id)
        
        self.start_time = time.time()
        
        # Log operation start
        self.logger.info(
            f"Operation started: {self.operation}",
            operation_start=True,
            start_time=self.start_time
        )
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time if self.start_time else 0
        
        if exc_type is None:
            # Successful completion
            self.logger.info(
                f"Operation completed successfully: {self.operation}",
                operation_end=True,
                duration_seconds=duration,
                success=True
            )
        else:
            # Failed operation
            self.logger.error(
                f"Operation failed: {self.operation}",
                operation_end=True,
                duration_seconds=duration,
                success=False,
                error_type=exc_type.__name__ if exc_type else None,
                error_message=str(exc_val) if exc_val else None
            )
        
        # Clear context variables
        current_operation.set(None)
        current_prospect_id.set(None)
        current_tool_name.set(None)
        request_id.set(None)


# Initialize logging on module import
setup_logging()
