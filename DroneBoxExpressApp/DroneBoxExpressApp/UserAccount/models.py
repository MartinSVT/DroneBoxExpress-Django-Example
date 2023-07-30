from enum import Enum
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from DroneBoxExpressApp.Core.validators import custom_word_content_validator, validate_file_size
from DroneBoxExpressApp.Core.mixins import EnumMixin


class ProfileTypes(EnumMixin, Enum):
    Admin = "Admin"
    Customer = "Customer"
    Editor = "Editor"
    Pilot = "Pilot"


class DroneBoxUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        help_text=_(
            "Maximum 50 characters. Letters, digits and @.+-_"
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("Username already exists"),
        },
    )
    email = models.EmailField(_("email address"), blank=False, null=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class DroneBoxProfile(models.Model):
    profile_type = models.CharField(
        choices=ProfileTypes.list_choices(),
        max_length=ProfileTypes.max_len(),
        default="Customer",
        null=False,
        blank=False,
    )
    first_name = models.CharField(max_length=30, validators=(
        MinLengthValidator(2),
        custom_word_content_validator,
    ), blank=True, null=True)
    last_name = models.CharField(max_length=30, validators=(
        MinLengthValidator(2),
        custom_word_content_validator,
    ), blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="images", validators=(validate_file_size,), blank=True, null=True)
    user = models.OneToOneField(DroneBoxUser, on_delete=models.CASCADE, primary_key=True)
    total_revenue = models.FloatField(blank=True, null=False, default=0.0, validators=[MinValueValidator(0.0)])

    def get_custom_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        else:
            return self.user.username

    def __str__(self):
        return self.get_custom_name()
