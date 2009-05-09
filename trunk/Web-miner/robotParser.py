import robotparser
from URLInfo import get_baseUrl

def is_crawlable(url):
    robotTxtParser = robotparser.RobotFileParser()
    base_url = get_baseUrl(url)
    robots = "http://"+base_url+"/robots.txt"
    robotTxtParser.set_url(robots)
    robotTxtParser.read()
    return robotTxtParser.can_fetch("web-miner",url)

if __name__ == "__main__":
    print is_crawlable("http://www.google.com/images")