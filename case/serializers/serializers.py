from django.conf import settings
from rest_framework import serializers
from case.models import Case, Tooth

def allowed_lang_codes():
    return [code for code, _ in getattr(settings, "LANGUAGES", (("en", "English"),))]

class CaseSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    
    # translated payload (write-only)
    translations = serializers.DictField(child=serializers.DictField(), write_only=True, required=True)
    name = serializers.CharField(read_only=True)  # active-language output

    def create(self, validated_data):
        # 1) pull out translations
        translations = validated_data.pop("translations", {})

        # 2) create the shared row with ALL non-translatable fields (no matter how many)
        obj = Case.objects.create(**validated_data)

        # 3) write each language’s translated fields
        for lang, payload in translations.items():
            obj.set_current_language(lang)
            obj.name = payload["name"].strip()
            # set other translated fields here if you add more later...
            obj.save()

        return obj

    def update(self, instance, validated_data):
        # 1) pop translations (may be partial on PATCH)
        translations = validated_data.pop("translations", {})

        # 2) apply all non-translatable updates in one go
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if validated_data:
            instance.save()  # save once for all non-translatable changes

        # 3) apply translated updates (only those provided)
        for lang, payload in translations.items():
            instance.set_current_language(lang)
            if "name" in payload and str(payload["name"]).strip():
                instance.name = payload["name"].strip()
                instance.save()

        return instance

    def to_representation(self, instance):
        req = self.context.get("request")
        lang = getattr(getattr(req, "user", None), "language", None) if req and getattr(req, "user", None) and req.user.is_authenticated else None
        lang = req.GET.get("lang")
        #lang = lang or settings.LANGUAGE_CODE

        name = instance.safe_translation_getter("name", language_code=lang, default=None)
        return {
            "id": str(instance.id),
            "name": name,
        }



class ToothSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    is_adult = serializers.BooleanField(required=True)

    # translated payload (write-only)
    translations = serializers.DictField(child=serializers.DictField(), write_only=True, required=True)
    name = serializers.CharField(read_only=True)  # active-language output

    # ... validate_translations(...) same as before ...

    def create(self, validated_data):
        # 1) pull out translations
        translations = validated_data.pop("translations", {})

        # 2) create the shared row with ALL non-translatable fields (no matter how many)
        obj = Tooth.objects.create(**validated_data)

        # 3) write each language’s translated fields
        for lang, payload in translations.items():
            obj.set_current_language(lang)
            obj.name = payload["name"].strip()
            # set other translated fields here if you add more later...
            obj.save()

        return obj

    def update(self, instance, validated_data):
        # 1) pop translations (may be partial on PATCH)
        translations = validated_data.pop("translations", {})

        # 2) apply all non-translatable updates in one go
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if validated_data:
            instance.save()  # save once for all non-translatable changes

        # 3) apply translated updates (only those provided)
        for lang, payload in translations.items():
            instance.set_current_language(lang)
            if "name" in payload and str(payload["name"]).strip():
                instance.name = payload["name"].strip()
                instance.save()

        return instance

    def to_representation(self, instance):
        req = self.context.get("request")
        lang = getattr(getattr(req, "user", None), "language", None) if req and getattr(req, "user", None) and req.user.is_authenticated else None
        lang = req.GET.get("lang")

        name = instance.safe_translation_getter("name", language_code=lang, default=None)
        return {
            "id": str(instance.id),
            "name": name,
            "is_adult": instance.is_adult
        }



