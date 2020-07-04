from livereload.django.template.observers import DjangoTemplateDirectoriesObserver
from livereload.server.notifiers import LivereloadServerNotifier
from livereload.event.handlers import LivereloadFileEventHandler

from django.conf import settings

if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
    from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand
else:
    from django.core.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):

    help = 'Runs development server, and notifies external livereload server on server reload or template changes'

    livereload_host = getattr(settings, 'LIVERELOAD_HOST', 'localhost')
    livereload_port = getattr(settings, 'LIVERELOAD_PORT', 35729)
    

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            '--livereload-host',
            default = self.livereload_host,
            action  = 'store',
            dest    = 'livereload_host',
            help    = 'Livereload server host',
        )
        
        parser.add_argument(
            '--livereload-port',
            default = self.livereload_port,
            action  = 'store',
            dest    = 'livereload_port',
            help    = 'Livereload server port',
        )


    def get_handler(self, *args, **options):
        handler = super().get_handler(*args, **options)

        self.apply_command_line_options(**options)
        self.start_livereload_notifier(self.livereload_host, self.livereload_port)

        return handler


    def apply_command_line_options(self, **options):
        self.livereload_host = options.get('livereload_host', self.livereload_host)
        self.livereload_port = options.get('livereload_port', self.livereload_port)
        
        setattr(settings, 'LIVERELOAD_HOST', self.livereload_host)
        setattr(settings, 'LIVERELOAD_PORT', self.livereload_port)
        

    def start_livereload_notifier(self, livereload_host, livereload_port):
        server_notifier = LivereloadServerNotifier(livereload_host, livereload_port)
        event_handler   = LivereloadFileEventHandler(server_notifier)
        
        observer = DjangoTemplateDirectoriesObserver()
        observer.schedule_template_directories(settings, event_handler)
        observer.start()
        
        server_notifier.force_page_reload()