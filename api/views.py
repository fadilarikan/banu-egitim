from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1, required=False)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserAddSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, required=True)

class UserView(APIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def get(self, request):
        user_id = request.query_params.get('id')
        try:
            if user_id is not None and user_id != '':
                serializer = IdSerializer(data=request.query_params)
                if not serializer.is_valid():
                    return Response({
                        'success': False,
                        'message': serializer.errors

                    }, status=400)
                data = serializer.data
                user = User.objects.filter(id=data['id']).first()
                if user is None:
                    return Response({
                        'success': False,
                        'message': 'User not found'
                    }, status=400)
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    # ... diğer özellikler
                }
                return Response({
                    'success': True,
                    'data': user_data
                }, status=200)
            else:
                return Response({
                    'success': True,
                    'data': list(User.objects.all().values())
                }, status=200)
        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Getting user is failed'
            }, status=400)

    def post(self, request):
        try:
            serializer = UserAddSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': serializer.errors
                }, status=400)
            data = serializer.validated_data
            user = User.objects.filter(username=data['username'],
                                       email=data['email']).first()
            if user:
                return Response({
                    'success': False,
                    'message': 'User already exists'
                }, status=400)
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # ... diğer özellikler
            }
            return Response({
                'success': True,
                'message': 'User added',
                'data': user_data
            }, status=200)

        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Adding user is failed'
            }, status=400)

    def delete(self, request):
        try:
            serializer = IdSerializer(data=request.query_params)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'User not found'
                }, status=400)
            data = serializer.validated_data
            user = User.objects.filter(id=data['id']).first()
            if user is None:
                return Response({
                    'success': False,
                    'message': 'User not found'
                }, status=400)
            user.delete()
            return Response({
                'success': True,
                'message': 'User deleted',
                'data': data['id']
            }, status=200)
        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Deleting user is failed'
            }, status=400)
