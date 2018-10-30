from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from read_record.models import ReadNum, ReadDetail
from pure_pagination import Paginator,  PageNotAnInteger
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from ludadablog.forms import LoginForm


def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_counts = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year).count()
        blog_dates_counts[blog_date] = blog_count

    context['blog_dates'] = blog_dates_counts
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(context['blogs'], 5, request=request)

    context['page_of_blogs'] = p.page(page)
    return render(request, 'blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, id=blog_pk)
    login_form = LoginForm()
    context['login_form'] = login_form
    context['blog'] = blog
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        ct = ContentType.objects.get_for_model(Blog)
        if ReadNum.objects.filter(content_type=ct, object_id=blog.id).count():
           readnum = ReadNum.objects.get(content_type=ct, object_id=blog.id)
        else:
            readnum = ReadNum(content_type=ct, object_id=blog.id)
        readnum.read_num +=1
        readnum.save()
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=blog.id, date=date)
        readDetail.read_num +=1
        readDetail.save()
    context['blog'].save()
    context['previous_blog'] = Blog.objects.filter(created_time__gt=context['blog'].created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=context['blog'].created_time).first()
    response = render(request,'blog_detail.html', context)
    response.set_cookie('blog_%s_readed' % blog_pk, 'true')
    return response


def blog_type_list(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, id=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_counts = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__month=blog_date.month).count()
        blog_dates_counts[blog_date] = blog_count

    context['blog_dates'] = blog_dates_counts
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(context['blogs'], 3, request=request)

    context['page_of_blogs'] = p.page(page)
    return render(request,'blog_type_list.html', context)


def blog_dates_list(request, year, month):
    context = {}
    context['blogs'] = Blog.objects.filter(created_time__year=year)
    context['blog_types'] = BlogType.objects.all()
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_counts = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_counts[blog_date] = blog_count

    context['blog_dates'] = blog_dates_counts
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(context['blogs'], 3, request=request)

    context['page_of_blogs'] = p.page(page)
    return render(request,'blog_date_list.html', context)
