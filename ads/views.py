import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Selection
from ads.permissions import IsOwnerOrStaff
from ads.serializers import AdListSerializer, AdDetailSerializer, SelectionCreateSerializer, SelectionListSerializer, \
    SelectionDetailSerializer, CategorySerializer, AdUpdateSerializer, AdDeleteSerializer, AdCreateSerializer
from avito import settings
from users.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def root(request):
    return JsonResponse({'status': 'ok'})


# @method_decorator(csrf_exempt, name='dispatch')
# class CategoryView(View):
#     def get(self, request):
#         categories = Category.objects.all()
#         result = []
#         for cat in categories:
#             result.append({"id": cat.id, "name": cat.name})
#         return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})
#
#     def post(self, request):
#         data = json.loads(request.body)
#         new_category = Category.objects.create(name=data['name'])
#         return JsonResponse({'id': new_category.id, 'name': new_category.name}, safe=False,
#                             json_dumps_params={'ensure_ascii': False})
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class CategoryCreateView(CreateView):
#     model = Category
#     fields = ['name']
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         category = Category.objects.create(name=data['name'])
#         return JsonResponse({'id': category.id, 'name': category.name}, safe=False,
#                             json_dumps_params={'ensure_ascii': False})
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class CategoryUpdateView(UpdateView):
#     model = Category
#     fields = ['name']
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#         data = json.loads(request.body)
#         self.object.name = data['name']
#         self.object.save()
#         return JsonResponse({'id': self.object.id, 'name': self.object.name}, safe=False,
#                             json_dumps_params={'ensure_ascii': False})
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class CategoryDeleteView(DeleteView):
#     model = Category
#     success_url = '/'
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#         return JsonResponse({}, status=204)
#
#
# class CategoryDetailView(DetailView):
#     model = Category
#
#     def get(self, request, *args, **kwargs):
#         cat = self.get_object()
#         return JsonResponse({'id': cat.id, 'name': cat.name}, safe=False,
#                             json_dumps_params={'ensure_ascii': False})


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class AdViewSet(ModelViewSet):
#     queryset = Ad.objects.order_by("-price").all()
#     serializer_class = AdListSerializer
#
#     def list(self, request, *args, **kwargs):
#         categories = request.GET.getlist('cat', [])
#         if categories:
#             self.queryset = self.queryset.filter(category_id__in=categories)
#         text = request.GET.get('text')
#         if text:
#             self.queryset = self.queryset.filter(name__icontains=text)
#         location = request.GET.get('location')
#         if location:
#             self.queryset = self.queryset.filter(author__location__name__icontains=location)
#         price_from = request.GET.get('price_from')
#         price_to = request.GET.get('price_to')
#         if price_from:
#             self.queryset = self.queryset.filter(price__gte=price_from)
#         if price_to:
#             self.queryset = self.queryset.filter(price__lte=price_to)
#
#         return super().list(self, request, *args, **kwargs)


class AdListView(ListAPIView):
    queryset = Ad.objects.order_by("-price").all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat', [])
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)
        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)
        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().get(self, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request):
        all_ads = Ad.objects.all()
        result = []
        for ad in all_ads:
            result.append(
                {"id": ad.id,
                 "name": ad.name,
                 "author": ad.author,
                 "price": ad.price,
                 "description": ad.description,
                 "is_published": ad.is_published})
        return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        data = json.loads(request.body)
        new_ad = Ad.objects.create(
            name=data['name'],
            author=data['author'],
            price=data['price'],
            description=data['description'],
            is_published=data['is_published']
        )
        return JsonResponse({
            "id": new_ad.id,
            "name": new_ad.name,
            "author": new_ad.author,
            "price": new_ad.price,
            "description": new_ad.description,
            "is_published": new_ad.is_published
        }, safe=False, json_dumps_params={'ensure_ascii': False})

#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdCreateView(CreateView):
#     model = Ad
#     fields = ['name', 'author', 'price', 'description', 'is_published', 'category']
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#
#         author = get_object_or_404(User, id=data['author_id'])
#         category = get_object_or_404(Category, id=data['category_id'])
#
#         new_ad = Ad.objects.create(
#             name=data['name'],
#             author=author,
#             category=category,
#             price=data['price'],
#             description=data['description'],
#             is_published=data['is_published'] if 'is_published' in data else False
#         )
#
#         return JsonResponse({
#             "id": new_ad.id,
#             "name": new_ad.name,
#             "author": new_ad.author.username,
#             "category": new_ad.category.name,
#             "price": new_ad.price,
#             "description": new_ad.description,
#             "is_published": new_ad.is_published
#         }, safe=False, json_dumps_params={'ensure_ascii': False})
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdUpdateView(UpdateView):
#     model = Ad
#     fields = ['name']
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#         data = json.loads(request.body)
#         self.object.name = data['name']
#         self.object.save()
#         return JsonResponse({
#             "id": self.object.id,
#             "name": self.object.name,
#             "author": self.object.author.username,
#             "category": self.object.category.name,
#             "price": self.object.price,
#             "description": self.object.description,
#             "is_published": self.object.is_published
#         }, safe=False, json_dumps_params={'ensure_ascii': False})
#
#
@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "category": self.object.category.name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url
        }, safe=False, json_dumps_params={'ensure_ascii': False})


# class AdDetailView(DetailView):
#     model = Ad
#
#     def get(self, request, *args, **kwargs):
#         ad = self.get_object()
#         return JsonResponse({"id": ad.id,
#                              "name": ad.name,
#                              "author": ad.author,
#                              "price": ad.price,
#                              "description": ad.description,
#                              "is_published": ad.is_published}, safe=False,
#                             json_dumps_params={'ensure_ascii': False})


class AdCreateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]


class AdDeleteView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]
