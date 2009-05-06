import robotparser
from URLInfo import get_baseUrl

def is_crawlable(url):
    ioebot = robotparser.RobotFileParser()
    base_url = get_baseUrl(url)
    robots = "http://"+base_url+"/robots.txt"
    ioebot.set_url(robots)
    ioebot.read()
    return ioebot.can_fetch("IOEBOT",url)

if __name__ == "__main__":
    print is_crawlable("http://www.google.com/images")