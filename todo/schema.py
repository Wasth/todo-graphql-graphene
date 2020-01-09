import graphene

from graphene_django.types import DjangoObjectType

from todo.models import List, Task


class ListType(DjangoObjectType):
	class Meta:
		model = List


class TaskType(DjangoObjectType):
	class Meta:
		model = Task


class Query(object):
	list = graphene.Field(ListType, id=graphene.Int())
	task = graphene.Field(TaskType, id=graphene.Int())
	lists = graphene.List(ListType)
	tasks = graphene.List(TaskType)

	def resolve_task(self, info, **kwargs):
		id = kwargs.get('id')

		if id is not None:
			return Task.objects.get(pk=id)

		return None

	def resolve_list(self, info, **kwargs):
		id = kwargs.get('id')

		if id is not None:
			return List.objects.get(pk=id)

		return None

	def resolve_lists(self, info, **kwargs):
		return List.objects.all()

	def resolve_tasks(self, info, **kwargs):
		return Task.objects.select_related('list').all()
