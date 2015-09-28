import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from goose import Goose


class GooseAPI:
    def __init__(self, url=None, raw_html=None):
        self.url = url
        self.raw_html = raw_html
        self.goose = Goose()
        self.extracted_content = None

    def extract(self):
        if self.url != None:
            self.extracted_content = self.goose.extract(url=self.url)
        elif self.raw_html != None:
            self.extracted_content = self.goose.extract(raw_html=self.raw_html)
        else:
            return {
                'title': '',
                'summary': '',
                'content': '',
                'published_at': '',
                'assets': []
            }

        return {
            'title': self.extracted_content.title,
            'summary': self.extracted_content.meta_description,
            'content': self.extracted_content.content_html,
            'published_at': self.extracted_content.publish_date,
            'assets': self.images()
        }

    def images(self):
        images = []
        for image in self.extracted_content.images:
            images.append({
                'url': image.src,
                'width': image.width,
                'height': image.height,
                'type': 'image'
            })
        return images
