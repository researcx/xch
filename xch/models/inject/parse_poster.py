import xch, hashlib, codecs, re, crypt

# tripcode
# blatantly stolen from https://github.com/exclude/monki/blob/1ef9adf1cca9e1593b88d137fe553f84dd1fe8a8/monki/boards/formatting.py#L100
def tripcode(trip):
  trip = bytes(trip, 'sjis', 'xmlcharrefreplace').decode('utf-8', 'ignore')
  salt = (trip + 'H..')[1:3].translate('................................'
                                        '.............../0123456789ABCDEF'
                                        'GABCDEFGHIJKLMNOPQRSTUVWXYZabcde'
                                        'fabcdefghijklmnopqrstuvwxyz.....'
                                        '................................'
                                        '................................'
                                        '................................'
                                        '................................')

  return crypt.crypt(trip, salt)[3:]

def name_and_tripcode(name):
  try:
    name, *trips = name.split('#')
  except AttributeError:
    return None, None
  else:
    trip = '#'.join(trips)

  if not name:
    name = None

  if not trip:
    trip = None
  else:
    trip = tripcode(trip)

  return name, trip
# blatantly stolen from https://github.com/exclude/monki/blob/1ef9adf1cca9e1593b88d137fe553f84dd1fe8a8/monki/boards/formatting.py#L100

def getMD5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()

#@xch.cache.memoize(timeout=86400) # parse_poster
def parse_poster(poster="", length=0, formatting=1):
    poster = poster if poster else ""
    xch.logger.info(str(poster) + ': ' +str(type(poster)))
    if not poster or poster == "":
        return "Anonymous"
    poster_full = name_and_tripcode(poster)
    return poster_full[0] + '#' + poster_full[1]
xch.app.jinja_env.globals.update(parse_poster=parse_poster)
