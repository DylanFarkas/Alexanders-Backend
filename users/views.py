from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .serializers import RegisterSerializer, LoginSerializer, PasswordResetSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Usar authenticate para verificar las credenciales
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'telefono': user.telefono,
                'rol': user.rol,
            }
        })

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Email no registrado'}, status=status.HTTP_404_NOT_FOUND)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://localhost:4200/reset-password/{uid}/{token}/"  # Asegúrate de que esta URL sea correcta
        send_mail(
            'Restablecer contraseña',
            f'Usa este enlace para restablecer tu contraseña: {reset_link}',
            'noreply@tusistema.com',
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Correo enviado con el enlace de recuperación'})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Necesita configuración extra para habilitar el blacklisting
            return Response({"message": "Sesión cerrada correctamente"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Token de refresh no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Token inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)
