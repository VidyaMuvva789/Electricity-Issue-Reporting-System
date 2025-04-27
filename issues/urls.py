from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import register, user_login, user_logout, report_issue, issue_list, admin_issue_list, update_issue_status_admin, submit_feedback, view_feedback

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('report/', report_issue, name='report_issue'),
    path('issues/', issue_list, name='issue_list'),
    path('manage/issues/', admin_issue_list, name='admin_issue_list'),
    path('manage/update/<int:issue_id>/', update_issue_status_admin, name='update_issue_admin'),
    path('feedback/<int:issue_id>/', submit_feedback, name='submit_feedback'),
    path('manage/feedback/', view_feedback, name='view_feedback'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
