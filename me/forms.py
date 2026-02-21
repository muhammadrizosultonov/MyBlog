from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    full_name = forms.CharField(
        label=_("Full name"),
        min_length=2,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Muhammadrizo Sultonov"),
                "autocomplete": "name",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("name@gmail.com"),
                "autocomplete": "email",
            }
        ),
    )
    subject = forms.CharField(
        label=_("Subject"),
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": _("Hiring / Project inquiry / Collaboration")}
        ),
    )
    message = forms.CharField(
        label=_("Message"),
        min_length=20,
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "placeholder": _("Tell me about your project, timeline, and requirements..."),
            }
        ),
    )
    website = forms.CharField(
        label=_("Website"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
            }
        ),
    )

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()
        if len(full_name) < 2:
            raise forms.ValidationError(_("Full name must be at least 2 characters."))
        return full_name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError(_("Please use a Gmail address."))
        return email

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 20:
            raise forms.ValidationError(_("Message must be at least 20 characters."))
        return message

    def is_honeypot_triggered(self) -> bool:
        return bool(self.cleaned_data.get("website"))
