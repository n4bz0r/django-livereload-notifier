from livereload.server.notifiers import LivereloadServerNotifier

from watchdog.events import FileSystemEventHandler

import threading
import logging
import time


class ThrottledLivereloadFileEventHandler(FileSystemEventHandler):

    logger = logging.getLogger(__name__)


    def __init__(self, delay_milliseconds = 20):
        self.pending_events     = {}
        self.delay_seconds      = delay_milliseconds / 1000
        self.delay_milliseconds = delay_milliseconds


    def dispatch(self, event):
        if self.is_pending(event):
            self.logger.debug(f'Event is already pending, throttling: {event}')
            
            return
            
        self.store_pending_event(event)
        self.start_delayed_dispatch_thread(event)


    def start_delayed_dispatch_thread(self, event):
        thread = threading.Thread(
            target = self.dispatch_with_delay,
            daemon = True,
            args   = (event, self.delay_seconds,)
        )
        
        self.logger.debug(f'Starting delayed ({self.delay_milliseconds}ms) dispatch thread for event: {event}')
        
        thread.start()


    def dispatch_with_delay(self, event, delay):
        time.sleep(delay)

        self.logger.debug(f'{self.delay_milliseconds}ms passed, dispatching event: {event}')
        
        super().dispatch(event)
        
        self.clear_pending_event(event)


    def is_pending(self, event):
        return event.src_path in self.pending_events


    def store_pending_event(self, event):
        self.pending_events[event.src_path] = event


    def clear_pending_event(self, event):
        self.pending_events.pop(event.src_path, None)


class LivereloadFileEventHandler(ThrottledLivereloadFileEventHandler):

    logger = logging.getLogger(__name__)
    

    def __init__(self, server_notifier, delay_milliseconds = 20):
        super().__init__(delay_milliseconds)
        
        if not isinstance(server_notifier, LivereloadServerNotifier):
            raise ValueError('{server_notifier} is not an instance of LivereloadServerNotifier')
    
        self.server_notifier = server_notifier


    def on_any_event(self, event):
        self.server_notifier.force_page_reload()


    def on_moved(self, event):
        self.logger.info(f'Moved: from {event.src_path} to {event.dest_path}')


    def on_created(self, event):
        self.logger.info(f'Created: {event.src_path}')


    def on_deleted(self, event):
        self.logger.info(f'Deleted: {event.src_path}')


    def on_modified(self, event):
        self.logger.info(f'Modified: {event.src_path}')