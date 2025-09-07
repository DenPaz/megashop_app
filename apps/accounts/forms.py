from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from apps.core.formmixins import MultiModelFormMixin
from apps.users.models import Profile

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "birth_date",
            "gender",
            "phone_number",
        ]


class PersonalInfoForm(MultiModelFormMixin, forms.Form):
    form_classes = {
        "user": UserForm,
        "profile": ProfileForm,
    }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        if instance is not None and not isinstance(instance, dict):
            kwargs["instance"] = {
                "user": instance,
                "profile": instance.profile,
            }
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, *, commit=True):
        objects = super().save(commit=commit)
        user = objects["user"]
        profile = objects["profile"]
        if commit:
            user.save()
            profile.user = user
            profile.save()
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "cep",
            "state",
            "city",
            "neighborhood",
            "street",
            "number",
            "complement",
        ]
