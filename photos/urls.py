"""mydjangosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import include, path
from .views import photos_list, photo_detail, PhotoAPIView, import_photo, import_json, render_view

urlpatterns = [

    path('', render_view),
    path('photo/', PhotoAPIView.as_view()),
    path('photo_detail/<int:pk>/', photo_detail),
    path('import_photo/<int:id>/', import_photo),
    path('import_json/<str:path>/', import_json),
]


