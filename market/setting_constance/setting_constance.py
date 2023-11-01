CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_ADDITIONAL_FIELDS = {
    "yes_no_null_select": [
        "django.forms.fields.ChoiceField",
        {"widget": "django.forms.Select", "choices": ((None, "-----"), ("yes", "Yes"), ("no", "No"))},
    ],
}

CONSTANCE_CONFIG = {
    "SITE_NAME": ("Megano", "Title text", str),
    "MAIL_SUPPORT": ("Support@ninzio.com", "Title text"),
}

CONSTANCE_CONFIG_FIELDSETS = {"General Options": {"SITE_NAME", "MAIL_SUPPORT"}}
