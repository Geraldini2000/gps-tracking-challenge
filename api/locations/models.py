from django.db import models
from django.contrib.auth.models import User


class UserDevice(models.Model):
    """
    Relaciona usuários aos seus dispositivos GPS.
    Garante que apenas o proprietário possa acessar os dados do dispositivo.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=100, unique=True, db_index=True)
    device_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_devices'
        unique_together = ('user', 'device_id')

    def __str__(self):
        return f"{self.user.username} - {self.device_id}"
