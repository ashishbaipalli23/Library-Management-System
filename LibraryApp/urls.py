from django.urls import path
from LibraryApp import views
from django.contrib.auth import views as ad


urlpatterns = [
    path('',views.home,name = 'hm'),
    path('abt/',views.about,name = 'abt'),
    path('cnt/',views.contact,name = 'cnt'),
    path('reg/',views.register,name = 'reg'),
    path('lgin/',ad.LoginView.as_view(template_name='html/login.html'),name="lgin"),
    path('lgot/',ad.LogoutView.as_view(template_name='html/logout.html'),name="lgot"),

    path('stdprof/',views.stdprof,name='stdprof'),
    path('reqbk/',views.showbook,name='reqbk'),
    path('update/',views.update,name='update'),

    path('teachprof/',views.techprof,name='teachprof'),
    path('updatet/',views.updatet,name="updatet"),
    path('addbook/',views.addbook,name='addbook'),
    path('editbook/<int:p>',views.editbook,name='editbook'),
    path('delbook/<int:d>',views.delbook,name='delbook'),

    path('bookview/<int:v>',views.bookview,name="bookview"),
    path('sdashboard/',views.sdashboard,name='sdashboard'),
    path('cancelreq/<int:bk>',views.cancel_req,name='cancelreq'),

    path('tdashboard/',views.tdashboard,name='tdashboard'),
    path('approve_book_request/<int:request_id>/', views.approve_book_request, name='approve_book_request'),
    path('reject_book_request/<int:request_id>/', views.reject_book_request, name='reject_book_request'),
    path('return_book/<int:request_id>', views.return_book, name='return_book'),

    path('payfine/',views.payfine,name='payfine'),
    
]