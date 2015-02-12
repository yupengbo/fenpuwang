# -*- coding: utf-8 -*-
import codecs
import md5
import string 
import re
from django.core.urlresolvers import reverse
def truncate_text(text, length = 200, suffix = "..."):
  if text == None:
    return None
  if len(text) > 200:
    text = text[0:200] + str(suffix)
  return text

def truncate(text,suffix="..."):             #kim
   if text == None:
       return None
   if len(text)>60:
       text = text[0:60] + str(suffix)
   return text

def replace_text_newline(text):
  if text:
    return text.replace(u'\n', u'<br/>')
  else:
    return ""

def clear_link(text):
  if text:
    return text.replace(u'<(.*?)>', u"")  

def replace_newkeyword(text):               #kim
  if text:
      if "keyword" in text:
          return text.replace('keyword','newkeyword')
      else:
          return text
def replace_link(text):                     #kim
    if text:
        if "&lt;/em&gt;" in text:
            text=text.replace("&lt;","<")
            text=text.replace("&gt;",">")
            text=text.replace("<em","<a")
            text=text.replace("em>","a>")
            keyword_pattern = '<a keyword="([^<]+)">'
            product_pattern = '<a product_id=([^<]+)>'
            search_pattern  = '<a newkeyword="([^<]+)">'
            for letter in text.split("</a>"):
                if re.search(keyword_pattern,letter):
                    letter_group=re.search(keyword_pattern,letter).group(1)
                    search_url = reverse('search:search',kwargs={'keyword':letter_group})
                    #text=text.replace('"'+letter_group+'"','/search/'+letter_group+'/'+' class='+'"'+'keyword_link'+'"')
                    text = text.replace('"'+letter_group+'"',search_url+' class='+'"'+'keyword_link'+'"')
                    text=text.replace("keyword","href")
                elif re.search(product_pattern,letter):
                    letter_group=re.search(product_pattern,letter).group(1)
                    product_url = reverse('product:product_detail',kwargs={'product_id':letter_group})
                    text = text.replace(letter_group,"\"" +product_url+'\" class='+'"'+'keyword_link'+'"')
                    text=text.replace("product_id","href")
                elif re.search(search_pattern,letter):
                    letter_group=re.search(search_pattern,letter).group(1)
                    text=text.replace("<a","<span")
                    text=text.replace("a>","span>")
                    text = text.replace('"'+letter_group+'"','"'+"color:red;"+'"')
                    text=text.replace("newkeyword","style")
            return text
        else:
            return text
    else:
        return ""
def get_md5(to_md5_str):
    m = md5.new()
    m.update(to_md5_str)
    return m.hexdigest()
