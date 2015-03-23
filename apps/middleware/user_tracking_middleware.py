from django.http import HttpResponseRedirect
from django.contrib.auth import SESSION_KEY

class UserTrackingMiddleware(object):
  def process_request(self, request):
    user_from = request.REQUEST.get('from')
    if user_from != None and user_from != "":
      request.session['user_from'] = user_from
    pass
