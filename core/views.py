from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from . forms import ProductForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.views.generic import DeleteView





def search(request):
    queryset = Product.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_result.html', context)



def index(request):
    items = Product.objects.filter(featured=True)

    context = {
        'items':items
        }
    return render(request, 'index.html', context)


def product_list(request):
    items = Product.objects.all().order_by('-timestamp')
    recently_viewed = Product.objects.order_by('-total_views')[0:3]
    if request.GET.get('order') == 'total_views':
        item = Product.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        items = Product.objects.all()
        order = 'normal'
    paginator = Paginator(items, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'order': order,
        'recently_viewed':recently_viewed
        }
    return render(request, 'category.html', context)



def product_detail(request, id):  
    recently_viewed = Product.objects.order_by('-total_views')[0:3]
    shares = Product.objects.filter(show_to_friends=True)
    item = get_object_or_404(Product, id=id)
    item.total_views += 1
    item.save(update_fields=['total_views'])
    context = { 
        'item':item,  
        'recently_viewed':recently_viewed,
        'shares':shares
    }
    return render(request, 'detail.html', context)



def product_create(request):
    title = 'Post'
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.author = User.objects.get(id=request.user.id)
            new_item.save()
            return redirect("core:product_list")
        else:
            return HttpResponse("The form is incorrect, please fill it in again.")
    else:
        form = ProductForm()
        context = { 'form': form, 'title': title }
        return render(request, 'new_item.html', context)


def product_update(request, id):
    title = 'Edit'
    item = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=item)
    author = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("core:product_detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'form': form,
        'title': title
    }
    return render(request, "new_item.html", context)



class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/'
    template_name = 'post_confirm_delete.html'