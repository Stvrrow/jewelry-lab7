from decimal import Decimal, InvalidOperation

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect, render

from .models import Client, Composition, Jewelry, JewelryType, Material

MATERIAL_ROWS = 3  # сколько строк «материал — количество» показывать в форме


def archive(request):
    return render(request, 'archive.html', {"posts": Jewelry.objects.all()})


def get_article(request, article_id):
    try:
        post = Jewelry.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Jewelry.DoesNotExist:
        raise Http404


def to_decimal(value):
    """Преобразует строку из формы в положительное число или возвращает None."""
    try:
        number = Decimal(value.replace(',', '.'))
    except (InvalidOperation, AttributeError):
        return None
    return number if number > 0 else None


def form_context(form):
    rows = [{'material': form.get('material_%d' % i, ''), 'amount': form.get('amount_%d' % i, '')}
            for i in range(MATERIAL_ROWS)]
    return {'form': form, 'rows': rows, 'types': JewelryType.objects.all(), 'materials': Material.objects.all()}


def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {key: request.POST.get(key, '').strip()
                    for key in ('title', 'text', 'jewelry_type', 'weight', 'work_price')}
            for i in range(MATERIAL_ROWS):
                form['material_%d' % i] = request.POST.get('material_%d' % i, '')
                form['amount_%d' % i] = request.POST.get('amount_%d' % i, '').strip()
            # в словаре form хранится информация, введенная пользователем
            errors = []
            if not (form['title'] and form['text'] and form['jewelry_type'] and form['weight'] and form['work_price']):
                errors.append(u"Не все поля заполнены")
            elif Jewelry.objects.filter(title__iexact=form['title']).exists():
                errors.append(u"Изделие с таким названием уже есть, придумайте другое название")
            weight, work_price = to_decimal(form['weight']), to_decimal(form['work_price'])
            if form['weight'] and weight is None:
                errors.append(u"Вес должен быть положительным числом")
            if form['work_price'] and work_price is None:
                errors.append(u"Стоимость работы должна быть положительным числом")
            composition = {}
            for i in range(MATERIAL_ROWS):
                material_id, amount = form['material_%d' % i], form['amount_%d' % i]
                if not material_id and not amount:
                    continue
                if not material_id or to_decimal(amount) is None:
                    errors.append(u"Для каждого материала укажите количество больше нуля")
                elif material_id in composition:
                    errors.append(u"Один и тот же материал указан несколько раз")
                else:
                    composition[material_id] = to_decimal(amount)
            if not composition:
                errors.append(u"Изделие должно состоять хотя бы из одного материала")
            if errors:
                # если введенные данные некорректны
                form['errors'] = errors
                return render(request, 'create_post.html', form_context(form))
            article = Jewelry.objects.create(
                title=form['title'], text=form['text'], jewelry_type_id=form['jewelry_type'],
                weight=weight, work_price=work_price, customer=request.user)
            for material_id, amount in composition.items():
                Composition.objects.create(jewelry=article, material_id=material_id, amount=amount)
            # перейти на страницу нового изделия
            return redirect('get_article', article_id=article.id)
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', form_context({}))
    else:
        raise Http404


def register(request):
    if request.method == "POST":
        form = {key: request.POST.get(key, '').strip()
                for key in ('username', 'email', 'first_name', 'last_name', 'phone')}
        password, password2 = request.POST.get('password', ''), request.POST.get('password2', '')
        errors = []
        if not (form['username'] and form['email'] and password and password2):
            errors.append(u"Заполните логин, email и оба поля пароля")
        elif password != password2:
            errors.append(u"Пароли не совпадают")
        else:
            try:
                User.objects.get(username=form['username'])
                # если пользователь существует, то ошибки не произойдет и программа доберется до этой строчки
                errors.append(u"Пользователь с таким именем уже есть")
            except User.DoesNotExist:
                pass  # этот логин свободен
        if errors:
            form['errors'] = errors
            return render(request, 'register.html', {'form': form})
        user = User.objects.create_user(form['username'], form['email'], password,
                                        first_name=form['first_name'], last_name=form['last_name'])
        Client.objects.create(user=user, phone=form['phone'])
        login(request, user)
        return redirect('archive')
    return render(request, 'register.html', {'form': {}})


def login_view(request):
    if request.method == "POST":
        form = {'username': request.POST.get('username', '').strip()}
        password = request.POST.get('password', '')
        if not form['username'] or not password:
            form['errors'] = [u"Введите логин и пароль"]
            return render(request, 'login.html', {'form': form})
        user = authenticate(username=form['username'], password=password)
        if user is None:
            form['errors'] = [u"Такого аккаунта не существует или пароль неверный"]
            return render(request, 'login.html', {'form': form})
        login(request, user)
        return redirect('archive')
    return render(request, 'login.html', {'form': {}})


def logout_view(request):
    logout(request)
    return redirect('archive')
