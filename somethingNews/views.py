from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import Post
import requests
import time, random
#from bs4 import BeautifulSoup

# Create your views here.

def newsCrawl(request):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }
    baseUrl = "https://udn.com/api/more"
    pageNum = 4
    newsList = []
    ranNum = random.randint(0, 2)

    for page in range(pageNum):
        query = f"page={page+1}&channelId=1&cate_id=6&type=breaknews"
        newsListUrl = baseUrl + '?' + query
        
        r = requests.get(newsListUrl, headers=HEADERS)
        newsList.extend(r.json()['lists'])
        
        time.sleep(random.uniform(1, 2))
        now = datetime.now()
    
    newsNum = len(newsList)
    
    return render(request, 'index.html', locals())
