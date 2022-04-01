from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.core.paginator import Paginator

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешны зарегистрированы .')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистации.')
    else:
        form = UserRegisterForm()

    return render(request, 'news/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'news/login.html', {'form':form})


def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7', 'ringo8']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_obj})


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'# using name in template(object_list)
    queryset = News.objects.select_related('category')
    paginate_by = 2
    #extra_context = {'title': 'Список новостей'}#only static data (str,dict)

    def get_context_data(self, *, object_list=None, **kwargs):# for list or dinamic data
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список новостей'
        return context

    #def get_queryset(self):
        #return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False# zapret na pokaz pustih category
    queryset = News.objects.select_related('category')

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):# for list or dinamic data
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'

    #pk_url_kwarg = 'news_id' <int:pk> -> <int:news_id>
    #template_name = 'news/news_detail.html'

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    #succes_url = reverse_lazy('home')
    login_url = '/admin/'#reverse_lazy('home')
    raise_exception = True



# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, template_name='news/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {"news_item": news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             #news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})