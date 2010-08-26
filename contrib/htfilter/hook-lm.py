"""
This is a proxy hook for htfilter2

https://launchpad.net/py-htfilter
"""

import re
from urlparse import urlparse
from lm import FaceFinder
from PIL import Image
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

def main():
    class Hook:
        ff = FaceFinder()
        def __init__(self, config, events):
            self.events = events
            self.events['rxhead'] += self.rxHead
            self.events['rxbody'] += self.rxBody
        def rxHead(self, config, request, response):
            if response['headers'].getheader('content-type','') == 'image/jpeg':
                config['buffer'] = 2
        def rxBody(self, config, request, response):
            if response['headers'].getheader('content-type','') == 'image/jpeg':
                try:
                    response['body'].seek(0)
                    img = Image.open(response['body'])
                    if img.size[0] > 100 and img.size[1] > 100:
                        new_img = Image.new('RGBA', img.size)
                        new_img.paste(img, None)
                        del img
                        self.ff.process_image(new_img)
                        response['body'].seek(0)
                        new_img.save(response['body'], 'JPEG')
                        del new_img
                        response['headers']['content-type'] = 'image/jpeg'
                except Exception, e:
                    print e
        def destruct(self):
            pass
    def HookFactory(config, events, request):
        return Hook(config, events)
    return HookFactory
