import xch
from xch.models.inject.parse_poster import name_and_tripcode

@xch.app.route("/_fn/generate_tripcode", methods=['POST', 'GET'])
def generate_tripcode():
    string = xch.request.form['password']
    
    if string:
        xch.logger.info(str(string) + " was inputted for tripcode generation")
        return string + " trip: " + str(name_and_tripcode(str(string)))

    return ""