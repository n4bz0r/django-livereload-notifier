from watchdog.observers import Observer

import django.template.utils as template_utilities

import logging


class DjangoTemplateDirectoriesObserver:

    logger = logging.getLogger(__name__)


    def __init__(self):
        self.observer = Observer()


    def start(self):
        self.logger.debug(f'Starting template directories observer')
    
        self.observer.start()


    def schedule(self, event_handler, template_directory, recursive = True):
        self.logger.info(f'Watching template directory for changes: {template_directory}')
    
        self.observer.schedule(event_handler, template_directory, recursive = recursive)


    def schedule_template_directories(self, settings, event_handler):
        template_engines = getattr(settings, 'TEMPLATES', [])
        
        if not template_engines:
            self.logger.info(f'No template engines defined in TEMPLATES settings variable.')

        for template_engine in template_engines:
            app_dirs_enabled = template_engine.get('APP_DIRS', False)
            
            if app_dirs_enabled:
                template_directories = template_utilities.get_app_template_dirs('templates')
            else:
                template_directories = template_engine.get('DIRS', [])

            for template_directory in template_directories:
                self.schedule(event_handler, template_directory)