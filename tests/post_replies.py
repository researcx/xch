import re

def get_replies_from_post(content):
    m = re.findall('>>(\d+)', content, re.IGNORECASE|re.MULTILINE)
    if m:
        print(m)
        return m
    return []
message = '''
yeah, fuck off faggots
>lol
'''

print(message)
print(get_replies_from_post(message))

for reply in get_replies_from_post(message):
    print(reply)