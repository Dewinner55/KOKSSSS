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
        # abstract = False

    def __str__(self):
        return f"{self.id} {self.username} {self.email}"
    
    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        print("CREATE ACT CODE=>", code)
        self.activation_code = code

    # class Meta(AbstractUser.Meta):
    #     swappable = "AUTH_USER_MODEL"


# class EmailConfirmation(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

# class RevokedToken(models.Model):
#     user = models.ForeignKey(CustomUser, verbose_name='Токен пользователя',on_delete=models.CASCADE, null=True)
#     token = models.TextField(verbose_name='Токен', unique=True)
#     timestamp = models.DateTimeField(verbose_name='Время создания Токена', auto_now_add=True, null=True)
#
#     def __str__(self):
#         return f"{self.user}: {self.token}"


