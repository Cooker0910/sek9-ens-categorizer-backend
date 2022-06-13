
def Truncate_Text(text, size=20, empty_string='-'):
  return text[:size] + (text[size:] and '..') if (text != None) and (len(text) > 0)  else empty_string

def str2bool(value):
  return True if value == 'true' else False
