import urlparse

def get_baseUrl(url):
    urls_tuple = urlparse.urlparse(url)
    return urls_tuple[1]
