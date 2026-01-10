from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
import uuid

class Medication(TranslatableModel):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=50),
    )
    class Meta:
        db_table="Medication"
    
    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or str(self.id)