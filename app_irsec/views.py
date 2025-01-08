from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Category, Topic
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, TopicSerializer
from rest_framework.viewsets import ModelViewSet


def index(request):
    root_categories = Category.objects.filter(parent__isnull=True).prefetch_related(
        'subcategories', 'topics').order_by('name')
    return render(request, 'app_irsec/categories.html', {'categories': root_categories})


def get_topic_content(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return JsonResponse({'content': topic.content})


class CategoryGetOrCreateView(APIView):
    def post(self, request):
        name = request.data.get('name')
        parent_id = request.data.get('parent_id')
        tree = request.data.get('tree')

        try:
            parent_category = None
            if parent_id:
                parent_category = Category.objects.get(id=parent_id)
            category, created = Category.objects.get_or_create(name=name, parent=parent_category, tree=tree)
            serializer = CategorySerializer(category)
        except Exception as e:
            print(f"---ERROR--- {e}")

        if created:
            print(f"Added category: {category.name}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(f"Syncronized category: {category.name}")
            return Response(serializer.data, status=status.HTTP_200_OK)


class TopicGetOrCreateView(APIView):
    def post(self, request):
        name = request.data.get('topic_name')
        category_id = request.data.get('category_id')
        file_name = request.data.get('file_name')
        category = Category.objects.get(id=category_id)
        content = request.data.get('content')
        tree = request.data.get('tree')

        try:
            topic, created = Topic.objects.get_or_create(
                name=name, category=category, file_name=file_name, tree=tree)
            serializer = TopicSerializer(topic)

            if not created:
                if topic.content == content:
                    print(f"Syncronized topic: {topic.name}")
                else:
                    topic.content = content
                    topic.save()
                    print(f"Updated topic: {topic.name}")
                serializer = TopicSerializer(topic)
                return Response(serializer.data, status=status.HTTP_200_OK)

            topic.content = content
            topic.save()
            print(f"Added topic: {topic.name}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"---ERROR--- {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topic.objects.all()
