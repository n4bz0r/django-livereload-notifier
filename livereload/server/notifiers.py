from urllib.request import urlopen
import logging


class LivereloadServerNotifier:

    logger = logging.getLogger(__name__)


    def __init__(self, host, port):
        self.host = host
        self.port = port


    def force_page_reload(self):
        livereload_address = f'http://{self.host}:{self.port}'
        force_reload_url   = f'{livereload_address}/changed?files=.'
    
        try:
            urlopen(force_reload_url)
            
            self.logger.info(f'Page reload request emitted: {livereload_address}')
        except IOError as exception:
            self.logger.error(f'Livereload server {livereload_address} is not (yet) available')