# -*- coding: utf-8 -*-
import string 

def truncate_text(text, length = 200, suffix = "..."):
  if text == None:
    return None
  if len(text) > 200:
    text = text[0:200] + str(suffix)
  return text