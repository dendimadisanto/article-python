from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bs4 import BeautifulSoup
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import json
import PyPDF2


import requests

@api_view(['GET', 'POST'])
def cariArtikelScholar(request):
    
    if request.method == 'GET':
      keyword = request.GET.get('keyword', '')
      start = request.GET.get('start','')
      r = requests.get('https://scholar.google.com/scholar?start='+start+'&hl=id&as_sdt=0%2C5&q=' + keyword + '&btnG=')
      soup = BeautifulSoup(r.content, 'html.parser')
      print(soup)
      data=[]
      for i in soup.find_all('div', {'class':'gs_r gs_or gs_scl'}):
        value =  {}
        if i.find("div", {"class": "gs_or_ggsm"}):
          value['title'] = i.find('h3').find('a').get_text()
          value['link_pdf'] = i.find('a')['href']
          value['author'] = i.find('div', {"class":"gs_a"}).get_text()
          value['desc'] = i.find('div', {"class":"gs_rs"}).get_text()
          data.append(value)

      return Response(data,status=200)

@api_view(['GET', 'POST'])
def cariArtikel(request):
    
    if request.method == 'GET':
      keyword = request.GET.get('keyword', '')
      start = request.GET.get('start','')
      r = requests.get('https://scholar.google.co.id/scholar?q='+keyword+'&hl=id&as_sdt=0,5')
      soup = BeautifulSoup(r.content, 'html.parser')
      data=[]
      for i in soup.find_all('div', {'class':'gs_r gs_or gs_scl'}):
        value =  {}
        if i.find("div", {"class": "gs_or_ggsm"}):
          value['title'] = i.find('h3').find('a').get_text()
          value['link_pdf'] = i.find('a')['href']
          value['author'] = i.find('div', {"class":"gs_a"}).get_text()
          value['desc'] = i.find('div', {"class":"gs_rs"}).get_text()
          data.append(value)

      return Response(data,status=200)

@api_view(['POST'])
def ekstrak(request):
  if request.method == 'POST':
    data = request.POST.get('data')
    data = json.loads(data)
    dokumen = data['dokumen']
    directory = data['directory']
    search = data['search']
    result = []
    for k in range(0, len(dokumen)):
      object = PyPDF2.PdfFileReader(directory + '/' + dokumen[k]['file_name_generated'])
      # get number of pages
      NumPages = object.getNumPages()
      # define keyterms
      search_keywords=search
      # extract text and do the search
      for i in range(0, NumPages):
        PageObj = object.getPage(i)
        sentences=PageObj.extractText()
        sentences=sentences.split(",")
        for sentence in sentences:
          lst = []
          obj = {}
          for word in search_keywords:
            if word in sentence.lower():
              lst.append(word)
              obj['sentence'] = sentence
              obj['pages'] = i
              obj['file'] = dokumen[k]['file_name_original']
              obj['ket'] = '{0} key word(s) in sentence: {1}'.format(len(lst), ', '.join(lst))
              result.append(obj)

    return Response(result,status=200)


@api_view(['GET', 'POST'])
def scrape_google(request):
    if request.method == 'GET':
      keyword = request.GET.get('keyword', '')
      start = request.GET.get('start','')
      response = get_results(keyword, start)
      data = parse_results(response)
      return Response(data,status=200)
    

def get_results(query, start):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?start="+start+"&q=" + query)
    
    return response

def parse_results(response):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link_pdf': result.find(css_identifier_link, first=True).attrs['href'],
            'desc': result.find(css_identifier_text, first=True).text
        }
        
        output.append(item)
        
    return output

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)