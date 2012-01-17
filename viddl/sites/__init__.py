
import re

__all__ = ['register_site', 'get_site']

class SiteRegistry(object):
    
    def __init__(self):
        self.registry = []
        
    def register_site(self, *urls):
        def reg(sitecls):
            for url in urls:
                self.registry.append((re.compile(url), sitecls))
            return sitecls
        return reg

    def get(self, url):
        for siteurl, sitecls in self.registry:
            match = siteurl.match(url)
            if match:
                return sitecls()
        
        return None

site_registry = SiteRegistry()

register_site = site_registry.register_site

get_site = site_registry.get