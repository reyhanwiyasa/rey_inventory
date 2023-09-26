from django.urls import path
from main.views import show_main, create_product, show_xml, show_json, show_xml_by_id, show_json_by_id, sub_amount, increment_amount, delete_item
from main.views import register
from main.views import login_user
from main.views import logout_user


app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product', create_product, name='create_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),  
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add-amount/<int:id>/',increment_amount, name='increment_amount'),
    path('sub-amount/<int:id>/',sub_amount, name='sub_amount'),
    path('delete_item/<int:id>/',delete_item, name='delete_item'), 
]