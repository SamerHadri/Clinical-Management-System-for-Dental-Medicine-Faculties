# record/signals.py
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.apps import apps

# IMPORTANT: Use your exact app label and model names here.
# If your model class is Appointment (singular), replace "Appointments" with "Appointment".
Appointments = apps.get_model("record", "Appointments")   # or apps.get_model("records", "Appointments")
RecordTooth  = apps.get_model("record", "RecordTooth")    # or apps.get_model("records", "RecordTooth")

ALIVE_STATUSES = ("P", "A")  # Pending, Approved

def _recalc_next_appointment(record_tooth_id):
    if not record_tooth_id:
        return
    now = timezone.localtime()
    today, now_time = now.date(), now.time()
    
    qs = (Appointments.objects
            .filter(record_tooth_id=record_tooth_id, status__in=ALIVE_STATUSES)
            .filter(models.Q(date__gt=today) | (models.Q(date=today) & models.Q(time__gt=now_time)))
            .order_by("date", "time"))
    
    nxt = qs.first()
    RecordTooth.objects.filter(pk=record_tooth_id).update(
        next_appointment=(nxt.date if nxt else None)
    )

@receiver(pre_save, sender=Appointments, dispatch_uid="record_appointments_pre_save_move_between_teeth")
def _handle_move_between_teeth(sender, instance, **kwargs):
    # If an appointment changes its record_tooth, recompute for the OLD tooth too.
    if not instance.pk:
        return
    try:
        old = Appointments.objects.get(pk=instance.pk)
    except Appointments.DoesNotExist:
        return
    if old.record_tooth_id != instance.record_tooth_id:
        _recalc_next_appointment(old.record_tooth_id)

@receiver(post_save, sender=Appointments, dispatch_uid="record_appointments_post_save_recalc")
def _after_save(sender, instance, **kwargs):
    _recalc_next_appointment(instance.record_tooth_id)

@receiver(post_delete, sender=Appointments, dispatch_uid="record_appointments_post_delete_recalc")
def _after_delete(sender, instance, **kwargs):
    _recalc_next_appointment(instance.record_tooth_id)
