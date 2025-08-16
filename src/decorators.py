import functools
import sys
from datetime import datetime
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: Имя файла для записи логов. Если None - вывод в консоль.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__
            log_message = ""

            try:
                result = func(*args, **kwargs)
                log_message = f"{func_name} ok\n"
                return result
            except Exception as e:
                log_message = f"{func_name} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}\n"
                raise
            finally:
                if filename:
                    with open(filename, "a") as f:
                        f.write(f"[{datetime.now()}] {log_message}")
                else:
                    sys.stdout.write(f"[{datetime.now()}] {log_message}")

        return wrapper

    return decorator
