from django.db import models


class List(models.Model):
	name = models.CharField(max_length=250)

	def __str__(self):
		return 'List: ' + self.name


class Task(models.Model):
	text = models.CharField(max_length=500)
	list = models.ForeignKey(
		List, related_name='tasks', on_delete=models.CASCADE
	)

	def __str__(self):
		return 'Task: ' + self.text
