LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'style': '{',
    'formatters': {
        'to_logs_general_security': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'to_console_0': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'to_console_1_to_mail': {
            'format': '%(levelname)s %(asctime)s %(message)s %(pathname)s'
        },
        'to_console_2_error_log': {
            'format': '%(levelname)s %(asctime)s %(message)s %(pathname)s %(exc_info)s'
        }
    },
    'filters': {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'filter_debug_info_levels': {
           '()': 'logging_formatter.log_custom_filters.FilterLevels',
           'filter_levels': ['DEBUG,''INFO']
        },
        'filter_warning_level': {
           '()': 'logging_formatter.log_custom_filters.FilterLevels',
           'filter_levels': ['WARNING']
        },
    },
    'handlers': {
        'console_0': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'to_console_0',
            'filters': ['require_debug_true', 'filter_debug_info_levels']
        },
        'console_1': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'to_console_1_to_mail',
            'filters': ['require_debug_true', 'filter_warning_level']
        },
        'console_2': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'to_console_2_error_log',
            'filters': ['require_debug_true']
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'to_console_1_to_mail',
            'filters': ['require_debug_false']
        },
        'logfile_general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/general.log',
            'formatter': 'to_logs_general_security',
            'filters': ['require_debug_false']
        },
        'logfile_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'to_console_2_error_log'
        },
        'logfile_security': {
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'to_logs_general_security'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console_0', 'console_1', 'console_2', 'logfile_general'],
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins', 'logfile_errors'],
            'propagate': False
        },
        'django.server': {
            'handlers': ['mail_admins', 'logfile_errors'],
            'propagate': False
        },
        'django.template': {
            'handlers': ['logfile_errors'],
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['logfile_errors'],
            'propagate': False
        },
        'django.security': {
            'handlers': ['logfile_security'],
            'propagate': False
        }
    }
}