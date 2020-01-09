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


class TaskInput(graphene.InputObjectType):
	id = graphene.ID()
	text = graphene.String()
	list = graphene.Int()


class ListInput(graphene.InputObjectType):
	id = graphene.ID()
	name = graphene.String()
	tasks = graphene.List(TaskInput)


class CreateList(graphene.Mutation):
	class Arguments:
		input = ListInput(required=True)

	ok = graphene.Boolean()
	list = graphene.Field(ListType)

	@staticmethod
	def mutate(root, info, input=None):
		ok = True
		list_instance = List(name=input.name)
		list_instance.save()
		return CreateList(ok=ok, list=list_instance)


class UpdateList(graphene.Mutation):
	class Arguments:
		id = graphene.Int(required=True)
		input = ListInput(required=True)

	ok = graphene.Boolean()
	list = graphene.Field(ListType)

	@staticmethod
	def mutate(root, info, id, input=None):
		ok = False
		list_instance = List.objects.get(pk=id)
		if list_instance:
			ok = True
			list_instance.name = input.name
			list_instance.save()
			return UpdateList(ok=ok, list=list_instance)
		return UpdateList(ok=ok, list=None)


class CreateTask(graphene.Mutation):
	class Arguments:
		input = TaskInput(required=True)

	ok = graphene.Boolean()
	task = graphene.Field(TaskType)

	@staticmethod
	def mutate(root, info, input=None):
		ok = True
		task_instance = Task(text=input.text)
		task_instance.list = List.objects.get(pk=input.list)
		task_instance.save()
		return CreateTask(ok=ok, task=task_instance)


class UpdateTask(graphene.Mutation):
	class Arguments:
		id = graphene.Int()
		input = TaskInput(required=True)

	ok = graphene.Boolean()
	task = graphene.Field(TaskType)

	@staticmethod
	def mutate(root, info, id, input=None):
		ok = False
		task_instance = Task.objects.get(pk=id)
		if task_instance:
			ok = True

			if input.list:
				task_instance.list = input.list

			if input.text:
				task_instance.text = input.text

			task_instance.save()
			return UpdateTask(ok=ok, task=task_instance)
		return UpdateTask(ok=ok, task=None)


class Mutation(graphene.ObjectType):
	create_list = CreateList.Field()
	update_list = UpdateList.Field()
	create_task = CreateTask.Field()
	update_task = UpdateTask.Field()
