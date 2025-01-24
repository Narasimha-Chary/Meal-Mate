from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from delivery.models import Customer, Restaurant, MenuItem, Cart

from django.contrib import messages  # To display messages to the user


import razorpay
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, "delivery/index.html")

def signin(request):
    return render(request, "delivery/signin.html")

def signup(request):
    return render(request, "delivery/signup.html")

def handle_login(request):

    if request.method == 'POST':
        #client's data
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            Customer.objects.get(username=username, password=password)
            if username == 'admin':
                return render(request, "delivery/login_success.html", {"username": username})
            else:
                restaurants = Restaurant.objects.all()
                context = {"restaurants": restaurants, "username": username}
                return render(request, "delivery/customer_home.html", context)            
        except:
            return render(request, "delivery/login_fail.html")
    else:
        return HttpResponse("Invalid request")
    
def handle_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        # c.save()
        try:
            #username already exists
            Customer.objects.get(username=username)
            return render(request, "delivery/signup_fail.html")
        except:
            c = Customer(username = username, password = password, email = email, mobile = mobile, address = address)
            c.save()


        # data = {
        #     'username': username,
        #     'password': password,
        #     'email': email, 
        #     'address': address, 
        #     'mobile': mobile
        #     }

        return render(request, "delivery/signin.html")
        # return HttpResponse(f"Username: {username}   Password: {password}  Email: {email}  Mobile: {mobile}  Address: {address}")
    else:
        return HttpResponse("Invalid request")
    

def restaurant_page(request):
    return render(request, "delivery/add_restaurant.html")


def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')


        try:
            #Restaurant already exists
            Restaurant.objects.get(name=name)
            return render(request, "delivery/adding_rest_fail.html")
        except:
            rest = Restaurant(name=name, picture=picture, cuisine=cuisine, rating=rating)
            rest.save()

        restaurants = Restaurant.objects.all()

        return render(request, "delivery/show_restaurants.html", {'restaurants': restaurants})
        
        # return render(request, "delivery/signin.html")
    else:
        return HttpResponse("Invalid request")
    

def show_restaurant_page(request):
    restaurants = Restaurant.objects.all()
    return render(request,'delivery/show_restaurants.html', {"restaurants":restaurants})

def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        # Handle adding new menu item
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        picture = request.POST.get('picture')

        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            is_veg=is_veg,
            picture=picture
        )

        return redirect('restaurant_menu', restaurant_id=restaurant.id)

    # Fetch all menu items for this restaurant
    menu_items = restaurant.menu_items.all()

    return render(request, 'delivery/menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
    })
    

# Update Restaurant Page
def update_restaurant_page(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'delivery/update_restaurant_page.html', {"restaurant": restaurant})

# Update Restaurant
def update_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.picture = request.POST.get('picture')
        restaurant.cuisine = request.POST.get('cuisine')
        restaurant.rating = request.POST.get('rating')
        restaurant.save()

        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})
    
def delete_restaurant(request, restaurant_id):
    rest = get_object_or_404(Restaurant, id=restaurant_id)
    rest.delete()
    restaurants = Restaurant.objects.all()
    return render(request, "delivery/show_restaurants.html", {'restaurants': restaurants})

# Update Menu Item Page
def update_menuItem_page(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)
    return render(request, 'delivery/update_menuItem_page.html', {"menuItem": menuItem})

# Update Menu item
def update_menuItem(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)

    if request.method == 'POST':
        menuItem.name = request.POST.get('name')
        menuItem.description = request.POST.get('description')
        menuItem.price = request.POST.get('price')
        menuItem.is_veg = request.POST.get('is_veg') == 'on'
        menuItem.picture = request.POST.get('picture')
        menuItem.save()
        
        # menu_items = MenuItem.objects.all()
        # return render(request, 'delivery/menu.html', {"menu_items": menu_items})
        restaurants = Restaurant.objects.all()
        return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})
    
    
# Delete Menu Item
def delete_menuItem(request, menuItem_id):
    menuItem = get_object_or_404(MenuItem, id=menuItem_id)
    menuItem.delete()
    # menu_items = MenuItem.objects.all()
    # return render(request, "delivery/menu.html", {'menu_items': menu_items})
    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html', {"restaurants": restaurants})

#Restaurant menu for Customer 
def customer_menu(request, restaurant_id, username):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()

    return render(request, 'delivery/customer_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'username' : username
    })

# view cart page
def show_cart_page(request, username):
    #fetch items in cart
    return render(request, "delivery/cart.html", {'username':username})

# # #add to cart
# def add_to_cart(request, username, item_id):
#     #check user and item
#     customer = get_object_or_404(Customer, username=username)
#     item = get_object_or_404(MenuItem, id=item_id)
#     #Get or create a cart for the customer
#     cart, created = Cart.objects.get_or_create(customer=customer)
#     #Add item to the cart 
#     cart.items.add(item)
#     #Add a success message
#     messages.success(request, f"{item.name} added to your cart!")
#     return redirect('customer_menu', restaurant_id=item.restaurant.id, username=username)

# Add items to cart
def add_to_cart(request, item_id, username):
    # Check user and item
    customer = get_object_or_404(Customer, username=username)
    item = get_object_or_404(MenuItem, id=item_id)

    # Get or create a cart for the customer
    cart, created = Cart.objects.get_or_create(customer=customer)

    # Add the item to the cart
    cart.items.add(item)

    # Add a success message
    messages.success(request, f"{item.name} added to your cart!")

    # Stay on the same menu page
    return redirect('customer_menu', restaurant_id=item.restaurant.id, username=username)

#Show Cart
def show_cart_page(request, username):
    #Fetch the customers cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    #Fetch cart items and total price
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'delivery/cart.html', {
        'items' : items,
        'total_price' : total_price,
        'username' : username,
    })

def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'Your cart is empty!',
        })

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)
    # Pass the order details to the frontend
    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
    })

# Orders Page
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    # Fetch cart items and total price before clearing the cart
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    # Clear the cart after fetching its details
    if cart:
        cart.items.clear()

    return render(request, 'delivery/orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })