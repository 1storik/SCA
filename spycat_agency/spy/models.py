from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Cat name: {self.name} - id: {self.pk}"


class Mission(models.Model):
    cat = models.ForeignKey(Cat, null=True, blank=True, on_delete=models.SET_NULL, related_name='missions')
    is_complete = models.BooleanField(default=False)

    def check_if_complete(self):
        if self.cat is not None and all(target.is_complete for target in self.targets.all()):
            self.is_complete = True
            self.save()

    def __str__(self):
        return f'Mission {self.id}'


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='targets')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'Target: {self.name} ({self.country})'
