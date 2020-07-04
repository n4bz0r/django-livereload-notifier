from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import smart_str
from django.conf import settings

from bs4 import BeautifulSoup
import logging


class LiveReloadScriptInjector(MiddlewareMixin):

    script_host = getattr(settings, 'LIVERELOAD_HOST', 'localhost')
    script_port = getattr(settings, 'LIVERELOAD_PORT', 35729)

    logger = logging.getLogger(__name__)


    def process_response(self, request, response):
        invalid_response = self.is_response_invalid(response)

        if invalid_response:
            return response
        
        parsed_page     = self.parse_page_content(response.content)
        invalid_content = self.is_head_tag_not_present(parsed_page)
        
        if invalid_content:
            return response
        
        script_tag      = self.make_script_tag(parsed_page, self.script_host, self.script_port)
        altered_page    = self.append_script_tag(parsed_page, script_tag)
        serialized_page = self.serialize_page(altered_page)
        
        return self.alter_response_content(response, serialized_page)


    def is_response_invalid(self, response):
        streaming            = self.is_response_streaming(response)
        invalid_status       = self.is_status_code_invalid(response)
        invalid_content_type = self.is_content_type_invalid(response)
        
        return streaming or invalid_status or invalid_content_type


    def is_response_streaming(self, response):
        streaming = getattr(response, 'streaming', None)
        
        if not streaming:
            return False
        
        self.logger.debug('Response is streaming, returning unaltered response')
        
        return True


    def is_status_code_invalid(self, response):
        status = getattr(response, 'status_code', 0)
        
        if status == 200:
            return False

        self.logger.debug(f'Response status code {status} is invalid, returning unaltered response')

        return True


    def is_content_type_invalid(self, response):
        content_type = response.get('Content-Type', '')
        content_type = content_type.split(';')[0].strip().lower()
        
        if content_type in ['text/html', 'application/xhtml+xml']:
            return False
            
        self.logger.debug(f'Response content type {content_type} is invalid, returning unaltered response')
        
        return True


    def parse_page_content(self, content):
        content = smart_str(content)
        parser  = 'html.parser'
   
        return BeautifulSoup(content, features=parser)


    def is_head_tag_not_present(self, parsed_page):
        head_tag_present = getattr(parsed_page, 'head', None)
   
        if head_tag_present:
            return False
        
        self.logger.debug('No <head> tag found, returning unaltered response')
        
        return True


    def make_script_tag(self, parsed_page, host, port):
        script_tag  = 'script'
        script_src  = f'http://{host}:{port}/livereload.js'
        script_type = 'text/javascript'
        
        self.logger.debug(f'Creating script tag with src: {script_src}')

        return parsed_page.new_tag(script_tag, src=script_src, type=script_type )


    def append_script_tag(self, parsed_page, script_tag):
        parsed_page.head.append(script_tag)
        
        return parsed_page


    def serialize_page(self, parsed_page):
        return str(parsed_page)
   
   
    def alter_response_content(self, response, new_content):
        response.content = new_content

        self.logger.debug('Livereload script tag successfully injected, returning altered response')

        return response