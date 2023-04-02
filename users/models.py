from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _



class CustomUser(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    activation_code = models.CharField(max_length=255, blank=True)

    email = models.EmailField(_("email address"), unique=False)

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )



    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")


    def __str__(self):
        return f"{self.id} {self.username} {self.email}"
    
    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        print("CREATE ACT CODE=>", code)
        self.activation_code = code


