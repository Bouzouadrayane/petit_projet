from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine.errors import DoesNotExist, ValidationError
from .models import Task


class TaskListView(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        return Response([t.to_dict() for t in tasks], status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        if not title:
            return Response({'error': 'title is required'}, status=status.HTTP_400_BAD_REQUEST)

        task = Task(title=title)
        task.save()
        return Response(task.to_dict(), status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):

    def get_object(self, pk):
        try:
            return Task.objects.get(id=pk)
        except (DoesNotExist, ValidationError):
            return None

    def get(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(task.to_dict(), status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get('title')
        done = request.data.get('done')

        if title is not None:
            task.title = title
        if done is not None:
            task.done = done

        task.save()
        return Response(task.to_dict(), status=status.HTTP_200_OK)

    def delete(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
