from django.urls import reverse

AUTH_SETTINGS = {
    'login_url': reverse('auth:login'),
    'home_url': reverse('shop:index'),
    'register_url': reverse('auth:register')
}
