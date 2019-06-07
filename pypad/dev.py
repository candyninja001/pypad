import inspect
import time

# This module provide functions for debugging parsing and
# other library behavior without disrupting programs importing
# this library

class Dev:
    _dev_mode_enabled = False
    _dev_log_entries = []

    _dev_timer_start = time.time()
    _dev_timer_end = None

    # Enable automatic printing of log into console
    @classmethod
    def enable(cls):
        return True

    @classmethod
    def disable(cls):
        return False

    # Recording log messages
    @classmethod
    def log(cls, message):
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        caller_module_name = caller_module.__name__
        dev_log_message = f'[{caller_module_name}] {message}'
        
        cls._dev_log_entries.append(dev_log_message)
        if cls._dev_mode_enabled:
            print(dev_log_message)

    @classmethod
    def clear_log(cls):
        cls._dev_log_entries = []

    @classmethod
    def get_log(cls):
        return cls._dev_log_entries

    # Functions allowing for timing speeds
    @classmethod
    def timer_start(cls):
        cls._dev_timer_start = time.time()
        cls._dev_timer_end = None

    @classmethod
    def timer_end(cls):
        cls._dev_timer_end = time.time()

    @classmethod
    def timer_read(cls):
        if cls._dev_timer_end == None:
            return time.time() - cls._dev_timer_start
        return cls._dev_timer_end - cls._dev_timer_start