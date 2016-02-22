#encoding=utf8
#Author : manza
#Created : 22.02.2016
#Last Modified : 22.02.2016

import requests
import json
import os
import webbrowser
from languagecodes import languages
from wox import Wox,WoxAPI
from os.path import join

class YoutubeWox(Wox):
    usage = {"Title": "Usage" , "SubTitle": "yt [query [order by {date|rating|relevance|title|videoCount|viewCount}]] | --config]" , "IcoPath":"icon.png"}
    #loadConfig
    with open(os.path.join(os.path.dirname(__file__),"config.json"), "r") as jsonfile:
        configfile = json.load(jsonfile)
        jsonfile.close()

    def query(self,key):
    
      anfrage = key.split('--config ')
      results = []
  
      if len(anfrage)<2 :
        #regular query, get results from youtube
        self.fetchResults(key, results)

      else:
        #user wants to do some configuration
        config_item = anfrage[1].split(' ', 1)
        if len(config_item) < 2:
          self.showConfigOptions(results)
        elif config_item[0] =='maxResults':
          value = 5
          try:
            valueRead = int(config_item[1])
            if (valueRead > 0 and valueRead  < 21):
              value = valueRead    
          except ValueError:
            value = 5
          finally:
            results.append({"Title" : "Change maximum Results to "+ str(value), "SubTitle": "maxResults can be between [1,20], default is 5", "IcoPath":"icon.png", "JsonRPCAction":{"method": "saveConfig","parameters":['maxResults', value],"dontHideAfterAction":False}})
        elif config_item[0] =='language':
          value = 'en'
          try:
            valueRead = config_item[1]
            if valueRead in languages:
              value = valueRead    
          except ValueError:
            value = 'en'
          finally:
            results.append({"Title" : "Change language to "+ value, "SubTitle": "language must be a two letter ISO 639-1 Code, default is en", "IcoPath":"icon.png", "JsonRPCAction":{"method": "saveConfig","parameters":['relevanceLanguage',value],"dontHideAfterAction":False}})   
        elif config_item[0] =='api':
          value = ''
          try:
            valueRead = config_item[1]  
            value = valueRead
          except ValueError:
            value = ''
          finally:
            results.append({"Title" : "Change apikey to "+ value, "SubTitle": "Use your own Youtube API key, you can get it on http://console.developers.google.com", "IcoPath":"icon.png", "JsonRPCAction":{"method": "saveConfig","parameters":['apikey', value],"dontHideAfterAction":False}})   
        else:
          results.append(self.usage)      

      return results
  
  
    def fetchResults(self, key, results):
      proxies = {}
      if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
        proxies = {
            "http": "http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
            "http": "https://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
        }
      
      reqUrl  = 'https://www.googleapis.com/youtube/v3/search?&part=snippet'
      reqUrl += '&key=' + self.configfile['apikey']
      reqUrl += '&q=' + key.split(' order by ')[0]
      reqUrl += '&maxResults='+str(self.configfile['maxResults'])
      reqUrl += '&relevanceLanguage='+ self.configfile['relevanceLanguage'] 
      
      orderSpecified = self.substringAfter(key, 'order by ')  
      if (orderSpecified in ('date','rating','relevance', 'title', 'videoCount', 'viewCount')):
        #use specified order for searching
        reqUrl += '&order=' + orderSpecified

      res = requests.get(reqUrl ,proxies = proxies)
      items = res.json()['items']
      for i in items:
          title = i['snippet']['title']
          channel = i['snippet']['channelTitle']
          video = i['id']
          typ = json.dumps(i['id']['kind'])
          if "channel" in typ:
              url = 'https://www.youtube.com/user/' + channel
              results.append({"Title": channel , "SubTitle": "Channel", "IcoPath":"icon.png","JsonRPCAction":{"method": "openUrl","parameters":[url],"dontHideAfterAction":False}})
          elif "video" in typ:
              vid = video['videoId']
              url = 'https://www.youtube.com/watch?v=' + vid
              results.append({"Title": title , "SubTitle": "Video by " + channel, "IcoPath":"icon.png","JsonRPCAction":{"method": "openUrl","parameters":[url],"dontHideAfterAction":False}})
          else:
              continue


    def showConfigOptions(self, results):
      results.append({"Title": "maximum Results" , "SubTitle": "change the number of maximum results displayed" , "IcoPath":"icon.png","JsonRPCAction":{"method": "config","parameters":['maxResults '],"dontHideAfterAction":True}}) 
      results.append({"Title": "language" , "SubTitle": "change preferred language" , "IcoPath":"icon.png","JsonRPCAction":{"method": "config","parameters":['language '],"dontHideAfterAction":True}})
      results.append({"Title": "API key" , "SubTitle": "set your own Youtube API key" , "IcoPath":"icon.png","JsonRPCAction":{"method": "config","parameters":['api '],"dontHideAfterAction":True}})   

  
    def substringAfter( self, s, delim):
        substring = s.partition(delim)[2]
        if (substring != ''):
          return substring.split(' ', 1)[0]


    def openUrl(self,url):
        webbrowser.open(url)
        #remove input from Wox line
        WoxAPI.change_query('')


    def config(self, text):
        WoxAPI.change_query('yt --config ' + text)


    def saveConfig(self, jkey, value):
        WoxAPI.change_query('')
        self.configfile[jkey] = value
        with open(os.path.join(os.path.dirname(__file__),"config.json"), "w+") as jsonFile:   
            jsonFile.write(json.dumps(self.configfile)) 
            jsonFile.close()


if __name__ == "__main__":
    YoutubeWox()