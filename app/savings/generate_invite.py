import jwt
from django.conf import settings
from datetime import datetime, timedelta
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json




class InviteCode:
    ALGORITHM ='HS256'
    def __init__(self,request=None):
        self.request = request
    def _generate_invite_token(self,group_name):
        """
        Generates an invite token that stores this user's invite,stored
        in request session and deleted after registeration through the invite
        token
        """
        token_time =datetime.utcnow() 
        
        self.request.session['dt'] = json.dumps(token_time,cls=DjangoJSONEncoder)
        token = jwt.encode({
            'dt':self.request.session.get('dt'),
            'group_name': group_name,
        }, settings.SECRET_KEY, algorithm=self.ALGORITHM)
        del self.request.session['dt']
        return token.decode('utf-8')

    def jwt_extract_handler(self,token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[self.ALGORITHM])

        except ValueError:
                return(f"Validation error {v}")   
        return {
        'expiry_date':payload.get('dt'),
        'group_name': payload.get('group_name')
            }

    def invite_code(self, group_name):

        return self._generate_invite_token(group_name)