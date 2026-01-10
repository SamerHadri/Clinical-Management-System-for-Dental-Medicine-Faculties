from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
import uuid



class Department(TranslatableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=50),
    )
    
    class Meta:
        db_table = "Department"
    
    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or str(self.id)

class Subject(TranslatableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=50),
    )
    academic_year = models.IntegerField(default = 1)
    academic_term = models.IntegerField(default = 1)
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        related_name="Subjects",
        related_query_name="Subject"
    )
    required_cases = models.IntegerField()
    
    class Meta:
        db_table = "Subject"
    
    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or str(self.id)
