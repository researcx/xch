import xch, hashlib
from geolite2 import geolite2

#@xch.cache.memoize(timeout=86400) # parse_ip
def parse_ip(ip):
    if xch.config['server']['anonymize_ip'] == True:
        return hashlib.sha256(ip.encode()).hexdigest()[-8:]
    else:
        return ip

#@xch.cache.memoize(timeout=86400) # country_from_ip
@xch.app.template_filter('country_from_ip')
def country_from_ip(ip):
    country_iso_code = "UN"
    continent_code = "UN"
    country_name = "Unknown"
    city_name = "Unknown"
    region = "Unknown"
    if ip:
        reader = geolite2.reader()
        geo_data = reader.get(ip)
        geolite2.close()
        if geo_data:
            if 'country' in geo_data and 'iso_code' in geo_data['country']:
                country_iso_code = geo_data['country']['iso_code']
                if 'names' in geo_data['country']:
                    country_name = geo_data['country']['names']['en']
            if 'continent' in geo_data and 'code' in geo_data['continent']:
                continent_code = geo_data['continent']['code']
            if 'city' in geo_data and 'names' in geo_data['city']:
                city_name = geo_data['city']['names']['en']
            if 'subdivisions' in geo_data and 'iso_code' in geo_data['subdivisions']:
                region = geo_data['subdivisions']['iso_code']

        return {'ip': ip, 'iso_code': country_iso_code, 'continent_code': continent_code, 'country_name': country_name, 'city_name': city_name, 'region': region}
xch.app.jinja_env.globals.update(country_from_ip=country_from_ip)
