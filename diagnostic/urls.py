from django.urls import path
from .views import index, RecordListView, RecordDetailView, RecordCreate, diagnose_record, DiagnoseCreate, DiagnoseListView

urlpatterns = [
    path("", index, name="index"),
    path("records/", RecordListView.as_view(), name="records"),
    path("records/new/", RecordCreate.as_view(), name="new-record"),
    path("records/<int:pk>", RecordDetailView.as_view(), name="record-detail"),
    path("records/<int:pk>/diagnose/", diagnose_record, name="record-diagnose"),
    path("diagnoses/", DiagnoseListView.as_view(), name="diagnoses"),
    path("diagnoses/new/", DiagnoseCreate.as_view(), name="new-diagnose"),
]
