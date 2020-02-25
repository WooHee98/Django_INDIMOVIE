from rest_framework import serializers
from movie.models import Movie
from user.models import Userdatado
from funding.models import Fundingdatado



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userdatado
        fields = '__all__'

        def create(self, data):
            user = Userdatado.objects.create(
                uidtext=data['u_idtext'],
                upassword=data['u_password'],
                uname=data['u_name'],
                ubirth=data['u_birth'],
                ubirth1=data['u_birth1'],
                ubirth2=data['u_birth2'],
                uphone=data['u_phone']

            )
            return user


class JoinSerializer(serializers.ModelSerializer):
    def create(self, data):
        user = Userdatado.objects.create(
            u_idtext=data['u_idtext'],
            u_password=data['u_password'],
            u_name=data['u_name'],
            u_birth=data['u_birth'],
            u_birth1=data['u_birth1'],
            u_birth2=data['u_birth2'],
            u_phone=data['u_phone'],
            )
        user.set_password(data['u_password'])
        #user.set_password(password)
        #user.u_password(user.password)
        user.save()
        return user
    
    class Meta:
        model = Userdatado
        fields = ('u_idtext', 'u_password', 'u_name', 'u_birth', 'u_birth1', 'u_birth2', 'u_phone')

class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fundingdatado
        fields = ('f_amount', 'f_cardnum', 'f_vaildity', 'f_cardpass', 's_id', 'u_id','address')

        def create(self, data):
            funding = Fundingdatado.objects.create(
                famount=data['f_amount'],
                fcardnum=data['f_cardnum'],
                fvaild=data['f_vaildity'],
                fcardpass=data['f_cardpass'],
                sid=data['s_id'],
                uid=data['u_id'],
                address=data['address']

            )
            funding.save()
            return funding


class FundingAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fundingdatado
        fields = ('f_id', 'f_amount', 'f_created_at', 'f_cardnum', 'f_vaildity', 'f_cardpass', 's_id', 'u_id')






