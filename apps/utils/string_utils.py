# -*- coding: utf-8 -*-
import string 
import re
from django.core.urlresolvers import reverse
def truncate_text(text, length = 200, suffix = "..."):
  if text == None:
    return None
  if len(text) > 200:
    text = text[0:200] + str(suffix)
  return text

def replace_text_newline(text):
  if text:
    return text.replace(u'\n', u'<br/>')
  else:
    return ""
     
def replace_link(text):
    if text:
        if "&lt;/em&gt;" in text:
            text=text.replace("&lt;","<")
            text=text.replace("&gt;",">")
            text=text.replace("keyword","href")
            text=text.replace("<em","<a")
            text=text.replace("em>","a>")
            pattern = '<a href="([^<]+)">'
            for letter in text.split("</a>"):
                if re.search(pattern,letter):
                    letter_group=re.search(pattern,letter).group(1)
                    search_url = reverse('search:search',kwargs={'keyword':letter_group})
                    #text=text.replace('"'+letter_group+'"','/search/'+letter_group+'/'+' class='+'"'+'keyword_link'+'"')
                    text = text.replace('"'+letter_group+'"',search_url+' class='+'"'+'keyword_link'+'"')
            return text
        else:
            return text
    else:
        return ""
        						  
