from app.crawler.crawler import start
# from controller.models import testing
import os

current_path = os.getcwd() # os.path.dirname(__file__)
chromedriver = os.path.join(current_path, 'chromedriver.exe')

if __name__ == '__main__':
    # print(current_path)
    print(chromedriver)
    start(chromedriver=chromedriver)
    # testing()
