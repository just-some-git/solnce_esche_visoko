from pathlib import Path


# Can not import this from Django settings because of circular import
# so need to create BASE_DIR here again
LOG_BASE_DIR = Path(__file__).resolve().parent.parent


CUSTOM_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },

    "formatters": {
        "default_formatter": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] / {levelname} \n"
                      "{message} \n",
            "style": "{",
        }
    },

    "handlers": {
        # DEBUG = True
        "debug_console_debug_true": {
            "level": "DEBUG",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "warning_console_debug_true": {
            "level": "WARNING",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "warning_file_debug_true": {
            "level": "WARNING",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/warning.log",
        },
        "error_console_debug_true": {
            "level": "ERROR",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "error_file_debug_true": {
            "level": "ERROR",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/error.log",
        },
        "critical_console_debug_true": {
            "level": "CRITICAL",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "critical_file_debug_true": {
            "level": "CRITICAL",
            "filters": [
                "require_debug_true",
            ],
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/critical.log",
        },

        # DEBUG = False
        "info_file_debug_false": {
            "level": "INFO",
            "filters": [
                "require_debug_false",
            ],
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/info_prod.log",
        },
        "warning_file_debug_false": {
            "level": "WARNING",
            "filters": [
                "require_debug_false",
            ],
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/warning_prod.log",
        },
        "error_file_debug_false": {
            "level": "ERROR",
            "filters": [
                "require_debug_false",
            ],
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/error_prod.log",
        },
        "critical_file_debug_false": {
            "level": "CRITICAL",
            "filters": [
                "require_debug_false",
            ],
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": f"{LOG_BASE_DIR}/logs/critical_prod.log",
        },
    },

    "loggers": {
        "django.request": {
            "handlers": [
                "debug_console_debug_true",
                "warning_console_debug_true",
                "warning_file_debug_true",
                "error_console_debug_true",
                "error_file_debug_true",
                "critical_console_debug_true",
                "critical_file_debug_true",
                "info_file_debug_false",
                "warning_file_debug_false",
                "error_file_debug_false",
                "critical_file_debug_false",
            ],
            "level": "INFO",
        },
        "django.server": {
            "handlers": [
                "debug_console_debug_true",
                "warning_console_debug_true",
                "warning_file_debug_true",
                "error_console_debug_true",
                "error_file_debug_true",
                "critical_console_debug_true",
                "critical_file_debug_true",
                "info_file_debug_false",
                "warning_file_debug_false",
                "error_file_debug_false",
                "critical_file_debug_false",
            ],
            "level": "INFO",
        },
        "django.db.backends": {
            "handlers": [
                "debug_console_debug_true",
                "warning_console_debug_true",
                "warning_file_debug_true",
                "error_console_debug_true",
                "error_file_debug_true",
                "critical_console_debug_true",
                "critical_file_debug_true",
                "info_file_debug_false",
                "warning_file_debug_false",
                "error_file_debug_false",
                "critical_file_debug_false",
            ],
            "level": "INFO",
        },
    },
}
