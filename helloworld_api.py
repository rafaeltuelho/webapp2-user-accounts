"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.

Ref:
    https://cloud.google.com/appengine/docs/python/endpoints/getstarted/backend/write_api
    https://cloud.google.com/appengine/docs/python/endpoints/getstarted/backend/write_api_post
    https://cloud.google.com/appengine/docs/python/endpoints/getstarted/backend/auth
"""


import endpoints

from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.ext import ndb
from google.appengine.api import mail

import webapp2
import json

import main
from main import BaseHandler

from models import User
from helloworld_api_messages import UserRequestMessage
from helloworld_api_messages import UserResponseMessage

package = 'Hello'

class Greeting(messages.Message):
  """Greeting that stores a message."""
  message = messages.StringField(1)


class GreetingCollection(messages.Message):
  """Collection of Greetings."""
  items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])

@endpoints.api(name='helloworld', version='v1')
class HelloWorldApi(remote.Service):
  """Helloworld API v1."""

  @endpoints.method(message_types.VoidMessage, GreetingCollection,
                    path='hellogreeting', http_method='GET',
                    name='greetings.listGreeting')
  def greetings_list(self, unused_request):
    return STORED_GREETINGS

  ID_RESOURCE = endpoints.ResourceContainer(
      message_types.VoidMessage,
      id=messages.IntegerField(1, variant=messages.Variant.INT32))

  @endpoints.method(ID_RESOURCE, Greeting,
                    path='hellogreeting/{id}', http_method='GET',
                    name='greetings.getGreeting')
  def greeting_get(self, request):
    try:
      return STORED_GREETINGS.items[request.id]
    except (IndexError, TypeError):
      raise endpoints.NotFoundException('Greeting %s not found.' %
                                        (request.id,))

  @endpoints.method(UserRequestMessage, UserResponseMessage,
                    path='users', http_method='POST',
                    name='users.createUser')
  def create_user(self, request):
    print 'create_user REST endpoint!!!'
    print '\t payload: ', request

    if (not request) or (not request.email): #user_data is a tuple
      error_msg = 'invalid payload!'
      raise endpoints.BadRequestException(error_msg)

    unique_properties = ['email_address']
    new_user = User
    user_data = new_user.create_user(request.user_name,
                                              unique_properties,
                                              email_address=request.email,
                                              name=request.name,
                                              password_raw=request.password,
                                              last_name=request.last_name,
                                              verified=False)

    print 'user_data: ', user_data

    if not user_data[0]: #user_data is a tuple
      error_msg = 'Unable to create user for email %s because of \
        duplicate keys %s' % (request.user_name, user_data[1])
      raise endpoints.NotFoundException(error_msg)

    base_handler = BaseHandler()
    user = user_data[1]
    user_id = user.get_id()

    token = new_user.create_signup_token(user_id)
    #'http://localhost:8080/v/4993981813358592-zFI2HbDWjLUAmTNCQK4JNm'
    # create a dummy request just to use webapp2 API in context of endpoints
    dummy_req = webapp2.Request.blank('/')
    dummy_req.app = main.app
    main.app.set_globals(app=main.app, request=dummy_req)

    verification_url = webapp2.uri_for('verification', type='v', user_id=user_id,
      signup_token=token, _full=True)

    print 'verification_url: ', verification_url

    msg = 'User created! \
          Please confirm your registration visiting <a href="{url}">{url}</a>'

    base_handler.send_mail('GAE Python Cloud Endpoint: Confirm your Subscription',
        msg.format(url=verification_url),
        user.email_address)

    return UserResponseMessage(user_name=user.email_address,
        confirmation_link=verification_url,
        created=True)

APPLICATION = endpoints.api_server([HelloWorldApi])
