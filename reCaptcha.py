import json
import urllib2, urllib

API_SERVER = "https://www.google.com/recaptcha/api/siteverify"


class  RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

    def __unicode__(self):
        print "%s, %s" % (self.is_valid, self.error_code)

    def __str__(self):
        return self.__unicode__()

    def get_error(self):
        if self.error_code and len(self.error_code):
            print 'recaptcha error: ', self.error_code[0]
            return self.error_code[0]


def submit(recaptcha_secret, recaptcha_response, remoteip=''):

    if not (recaptcha_secret and recaptcha_response and len(recaptcha_secret) and len(recaptcha_response) ):
        return RecaptchaResponse(is_valid=False, error_code='incorrect-captcha-sol')

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode({
        'secret': encode_if_necessary(recaptcha_secret),
        'response': encode_if_necessary(recaptcha_response),
        'remoteip': encode_if_necessary(remoteip)
    })

    request = urllib2.Request(
        url=API_SERVER,
        data=params,
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
        }
    )

    httpresp = urllib2.urlopen(request)
    return_values = json.loads(httpresp.read())
    print return_values

    if return_values.get('success', False):
        return RecaptchaResponse(is_valid=True)
    else:
        print 'RecaptchaResponse return_values: ', return_values
        return RecaptchaResponse(is_valid=False, error_code=return_values.get('error-codes', ''))
