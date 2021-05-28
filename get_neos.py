import ast
import urllib.request
from decouple import config

API_KEY = config("API_KEY")


class GetNeos(object):
    """
    Class which pulls the neo data from neo url every day
    """
    def __init__(self):
        self.url = 'https://api.nasa.gov/planetary/apod?api_key={}'.format(API_KEY)

    def getneo(self):
        webUrl = urllib.request.urlopen(self.url)
        data = webUrl.read()
        dict_str = data.decode("UTF-8")
        mydata = ast.literal_eval(dict_str)
        return mydata