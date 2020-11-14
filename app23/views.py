from django.shortcuts import render,redirect
from django.views.generic.base import View
from app23.models import ProductModel, UserModel, CartModel, BillModel
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


def show(request):
    return render(request, "homepage.html")


def login(request):
    return render(request, "admin_login.html")


def logined(request):
    user = request.POST['u1']
    pas = request.POST['u2']
    print(user)
    if user == "admin" and pas == "admin":
        request.session["admin_id"] = True
        # request.session.set_expiry(30)
        return redirect('logincheck')
    else:
        return render(request, "admin_login.html", {"data": "You are Entered Wrong Username and password..."})


def logincheck(request):
    res = request.session.get("admin_id", None)
    if res:
        return render(request, "logined_page.html", {"msg": "Admin Login Successfully..."})
    else:
        return redirect('login')


def logout(request):
    del request.session["admin_id"]
    return redirect('Home')


def get_product(request):
    # if request.method=='POST':
        id=request.POST.get('t1')
        name=request.POST['t2']
        price=request.POST['t3']
        quantity=request.POST['t4']
        category=request.POST['t5']
        img=request.FILES['t6']
        describe=request.POST['t7']
        try:
            ProductModel(id=id, name=name, price=price, quantity=quantity,
                         category=category, img=img, details_description=describe).save()
            return render(request, "logined_page.html", {"msg": "Product Added..."})
        except IntegrityError:
            return render(request, "logined_page.html", {"msg": "Product Id Already Available Try with Another id"})


def view_product(request):
    cat=request.GET['cate']
    qs=ProductModel.objects.filter(category=cat)
    return render(request, "view_product.html", {"data": qs})


def cart_added(request):
    pid = request.GET.get('pid')
    user = request.session.get('user_id', None)
    print(user)
    print(pid)
    val = CartModel.objects.filter(pid=pid, email=user)
    if val:
        return render(request,"error.html", {"msg": "Item Already Added To Cart..."})
    else:
        CartModel(email=user, pid=pid).save()
        return redirect('cart_items')


def cart_items(request):
    user = request.session.get('user_id',None)
    res = CartModel.objects.all().filter(email=user)
    items = []
    count = 0
    total = 0
    for x in res:
        obj = ProductModel.objects.get(id=x.pid)
        count = count+1
        items.append(obj)
        total = total+obj.price
    print(items)
    print(total)
    return render(request, "cart.html", {"data": items, "c_data": count})


def remove_cart(request):
    pid = request.GET.get('pid')
    user = request.session.get('user_id', None)
    CartModel.objects.filter(pid=pid, email=user).delete()
    response = redirect('cart_items')
    return response


def user_login(request):
    return render(request, "user_login.html")


def register_user(request):
    return render(request, "register_user.html")


def registered_user(request):
    name = request.POST['t1']
    contact_no = request.POST['t2']
    address = request.POST['t3']
    email = request.POST['t4']
    password = request.POST['t5']
    pincode = request.POST['t6']

    UserModel(name=name, contact_no=contact_no, address=address, email=email, password=password, pincode=pincode).save()
    return render(request, "register_user.html", {"msg": "The User Account Created successfully..."})


def user_logined(request):
    email = request.POST['u1']
    password=request.POST['u2']
    ef = UserModel.objects.filter(email=email, password=password)
    if ef:
        request.session["user_id"] = email
        return redirect('cart_items')
    else:
        return render(request, "user_login.html", {"data": "Username and Password are wrong..."})


def user_logout(request):
    del request.session["user_id"]
    return redirect('Home')


def buy_product(request):
    user = request.session.get('user_id', None)
    users = UserModel.objects.get(email=user)
    res = CartModel.objects.all().filter(email=user)
    items = []
    total = 0
    count = 0
    for x in res:
        obj = ProductModel.objects.get(id=x.pid)
        items.append(obj)
        count=count+1
        total = total + obj.price
    print(items)
    if total>10000:
        total=total-500
    print(total)
    return render(request, "buy_product.html", {"data": items, "user": users, "total_bill": total,
                                                "actual": total, "count": count})


class UserCarts(View):
    def get(self, request):
        users = CartModel.objects.all()
        items = []
        for x in users:
            if x.email not in items:
                items.append(x.email)
            else:
                continue
        return render(request, "userlist_cart.html", {"users": items})

    def post(self,request):
        pass


def open_cart(request):
    user = request.GET.get('user')
    res = CartModel.objects.all().filter(email=user)
    items = []
    count = 0
    for x in res:
        obj = ProductModel.objects.get(id=x.pid)
        count = count + 1
        items.append(obj)
    print(items)
    return render(request, "Open_cart.html", {"data": items, "c_data": count})


def confirm_bill(request):
    user = request.session.get('user_id', None)
    users = UserModel.objects.get(email=user)
    res = CartModel.objects.all().filter(email=users.email)
    items = []
    total = 0
    actual = 0
    count = 0
    for x in res:
        obj = ProductModel.objects.get(id=x.pid)
        items.append(obj)
        count = count + 1
        total = total + obj.price
        actual = actual + obj.price
    print(items)
    discount = 0
    if total > 10000:
        total = total - 500
        discount = 500
    BillModel(email=user, name=users.name, products_quantity=count, discounted=discount, actual_price=actual,
              total_bill=total).save()
    CartModel.objects.all().filter(email=users.email).delete()
    return redirect('cart_items')


def UserBills(request):
    data=BillModel.objects.all()
    return render(request,"user_bills.html", {"data": data})
