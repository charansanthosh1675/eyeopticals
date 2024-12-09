from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Order, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order

# Home Page View
def home(request):
    return render(request, 'home.html')

# Product List View
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Add Product View
@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        image = request.FILES['image']
        Product.objects.create(
            name=name, description=description, price=price, stock=stock, image=image
        )
        return redirect('product_list')
    return render(request, 'add_product.html')

# Update Product View
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('product_list')
    return render(request, 'update_product.html', {'product': product})

# Delete Product View
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})

# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# User Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Account created successfully!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'register.html')

# User Login View
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# User Logout View
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

# Add Product to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

# View Cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'view_cart.html', {'cart_items': cart_items})

# Place Order
@login_required
def place_order(request):
    # Ensure the cart exists or create one
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('product_list')

    # Ensure the customer record exists
    customer, created = Customer.objects.get_or_create(user=request.user)

    # Save orders before clearing the cart
    for item in cart_items:
        Order.objects.create(
            customer=customer,
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity
        )

    # Clear the cart after saving the order
    cart_items.delete()
    cart.delete()

    messages.success(request, "Your order has been placed successfully!")
    return redirect('product_list')


# Order History View
@login_required
def order_history(request):
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer).order_by('-order_date')
    return render(request, 'order_history.html', {'orders': orders})
