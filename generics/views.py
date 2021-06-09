import datetime

from django.core.exceptions import ImproperlyConfigured

from rest_framework.views import APIView
from rest_framework.response import Response


class CommandGenericView(APIView):
	"""Base generic view to get entries using command"""

	get_command = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.get_command:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have `get_command` attribute"
			)

	def get(self, request):
		command = self.get_command(request.user)
		data = command.execute()
		return Response(data)


class GetCreateGenericView(CommandGenericView):
	"""Base generic view to get and create entry"""

	create_service = None
	serializer_class = None
	model_name = 'object'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.create_service:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`create_service` attribute"
			)
		if not self.serializer_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`serializer_class` attribute"
			)

	def post(self, request):
		entry_data = request.data | {'owner': request.user}
		serializer = self.serializer_class(data=entry_data)
		if serializer.is_valid():
			entry = self.create_service.execute(entry_data)
			return Response({self.model_name: entry.pk}, status=201)

		return Response(serializer.errors, status=400)


class GetUpdateDeleteGenericView(APIView):
	"""Base generic view to get/update/delete a concrete entry"""

	get_service_class = None
	delete_service_class = None
	update_service_class = None
	serializer_class = None
	model_name = 'object'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.get_service_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`get_service_class` attribute"
			)
		if not self.delete_service_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`delete_service_class` attribute"
			)
		if not self.update_service_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`update_service_class` attribute"
			)
		if not self.serializer_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`serializer_class` attribute"
			)

	def dispatch(self, request, pk):
		self.get_service = self.get_service_class(request.user)
		self.entry = self.get_service.get_concrete(pk)
		return super().dispatch(request, pk)

	def get(self, request, pk):
		serializer = self.serializer_class(self.entry)
		return Response(serializer.data)

	def delete(self, request, pk):
		self.delete_service_class.execute({
			self.model_name: self.entry, 'owner': request.user
		})
		return Response(status=204)

	def put(self, request, pk):
		serializer = self.serializer_class(self.entry, data=request.data)
		if serializer.is_valid():
			service_data = serializer.validated_data | {
				self.model_name: self.entry, 'owner': request.user
			}
			self.update_service_class.execute(service_data)
			return Response(status=204)

		return Response(serializer.errors, status=400)


class GetForTheDateGenericView(APIView):
	"""Base generic view to get entries for the date"""

	command = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.command:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have `command` attribute"
			)

	def get(self, request, **kwargs):
		if 'day' not in kwargs:
			kwargs |= {'day': 1}
			
		date = datetime.date(**kwargs)
		command = self.command(request.user, date)
		entries = command.execute()
		return Response(entries)
