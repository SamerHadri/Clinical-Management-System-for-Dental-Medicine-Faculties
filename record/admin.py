from django.contrib import admin
from record.models import Record, RecordDisease, RecordMedication, RecordTooth


admin.site.register(Record)
admin.site.register(RecordDisease)
admin.site.register(RecordMedication)
admin.site.register(RecordTooth)