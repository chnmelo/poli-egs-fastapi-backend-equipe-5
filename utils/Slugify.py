import re
import unicodedata

class Slugify:
    @staticmethod
    def create_slug(value: str) -> str:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('utf-8')
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return re.sub(r'[-\s]+', '-', value)