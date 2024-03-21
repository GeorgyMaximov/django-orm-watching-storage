from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def is_long(self, minutes=60):
        if self.leaved_at:
            return (self.leaved_at - self.entered_at).total_seconds() > minutes * 60
        else:
            return (localtime() - self.entered_at).total_seconds() > minutes * 60
        
    def get_duration(self):
        if self.leaved_at:
            duration = int((self.leaved_at - self.entered_at).total_seconds())
        else:
            duration = int((localtime() - self.entered_at).total_seconds())
        return f'{duration//3600}:{duration%3600//60}:{duration%3600%60}'
    
    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
