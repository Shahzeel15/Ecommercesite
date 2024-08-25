from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
from django.contrib.auth import authenticate,login
from django.shortcuts import  render,redirect
from django.contrib import messages
import json
from .models import Product, Booking
 


#home page
# if the user is admin then redirect to admin dashborad or user dashboard
def home(request):
    if request.user.is_staff:
        return redirect('admindashboard')
    else:
        return redirect('main')
    return render(request,'home.html')
    #return HttpResponse("hello")


# navigation bar
def index(request):
    return render(request,'navigation.html')


# about page
def about(request):
    return render(request,'about.html')


# main home page
def main_index(request):
    data = Carousel.objects.all()
    dic = {'data':data}
    return render(request,'index.html',dic)


# admin login page
def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "User login successfully")
        
                # msg = "User login successfully"
                return redirect('admindashboard')
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'admin_login.html', dic)

# admin home page after login 
def adminHome(request):
    return render(request, 'admin_base.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


#add category insert the data into categorys table 
from .models import Category
def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category added")
        return redirect('view_category')
    return render(request, 'add_category.html', locals())

# view catagory
def view_category(request):
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

#edit category
def edit_category(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request, "Category updated")
        
        return redirect('view_category')
    return render(request, 'edit_category.html', locals())


#delete category
def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request, "Category deleted")
    return redirect('view_category')


#add product 
from .models import Product
def add_product(request):
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name'] 
        price = request.POST['price']
        cat = request.POST['category']
        # discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Product.objects.create(name=name, price=price, discount=0, category=catobj, description=desc, image=image)
        messages.success(request, "Product added")
       
    return render(request, 'add_product.html', locals())

#view product
def view_product(request):
    product = Product.objects.all()
    return render(request, 'view_product.html', locals())

#edit product
def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        # discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, discount=0, category=catobj, description=desc)
        messages.success(request, "Product Updated")
        return redirect('view_product')
    return render(request, 'edit_product.html', locals())

#delete product
def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')


#user registration page
def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
        UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
        messages.success(request, "Registeration Successful")
    return render(request, 'registration.html', locals())


#user login fun
def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'userlogin.html', locals())


#admin login fun
def profile(request):
    
    # user=user.objects.get(id=request.user.id)
    # if not redirect.User.is_authenticated:
    #     return redirect('userlogin')
    data = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        try:
            image = request.FILES['image']
            data.image = image
            data.save()
        except:
            pass
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        UserProfile.objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile updated")
        return redirect('profile')
    return render(request, 'profile.html', locals())


#logout
from django.contrib.auth import authenticate, login, logout
def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('main')

#change password check
def change_password(request):
    if request.method == 'POST':
        o = request.POST.get('old')
        n = request.POST.get('new')
        c = request.POST.get('confirm')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')

#user product page
def user_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "user-product.html", locals())

#product details page
def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "product_detail.html", locals())

#add to cart fun
def addToCart(request, pid):
    myli = {"objects":[]}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid):1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')


#incredecre
def incredecre(request, pid):
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')


#cart fun
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
        print(product)
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'cart.html', locals())


#delete cart
def deletecart(request, pid):
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')



#bookings page
def booking(request):
    user = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))
    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')
    for i,j in productid.items():
        product = Product.objects.get(id=i)
        quantity=int(j)
        total += int(j) * int(product.price)
    if request.method == "POST":
        return redirect('/payment/?total='+str(total))
    return render(request, "booking.html", locals()) 


# my order page at user side
def myOrder(request):
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())

#order tracking at user side
def user_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())

#order tracking at admin side
def change_order_status(request, pid):
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

#dummy payment page
def payment(request):
    total = request.GET.get('total')
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=total)
        cart.product = {'objects': []}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('myorder')
    return render(request, 'payment.html', locals())

#manage order at admin side
def manage_order(request):
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 


#deelete order at admin side
def delete_order(request, pid):
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))


#admin order tracking page
def admin_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin-order-track.html', locals()) 


#admin manage user page
def manage_user(request):
    user = UserProfile.objects.all()
    return render(request, 'manage_user.html', locals()) 

#admin delete user page
def delete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_user') 

#admin change password page
def admin_change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')

#admin dashboard

def admin_dashboard(request):
    user = UserProfile.objects.filter()
    category = Category.objects.filter()
    product = Product.objects.filter()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    cancel_order = Booking.objects.filter(status=5)
    return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
   
    return render(request, 'admin_dashboard.html', locals())



from django.db.models import Sum
def query_page(request):
    query_result = Booking.objects.values('user', 'product') \
        .annotate(total_quantity=Sum('quantity'), 
                  total_item_value=Sum('quantity') * Product.price) \
        .order_by('user', 'product')
    return render(request, 'query1.html', {'query_result': query_result})


# booking list
from django.shortcuts import render
from .models import Booking
import ast

def booking_list(request):
    bookings = Booking.objects.all()
    booking_data = []

    for booking in bookings:
        # Initialize quantity to 'N/A' if no product data
        quantity = 'N/A'
        
        if booking.product:
            try:
                # Safely evaluate the product field to convert it to a dictionary
                product_data = ast.literal_eval(booking.product)
                
                # Extract the quantity from the product_data dictionary
                # Assuming the format is {'objects': [{'4': 2}]}
                objects = product_data.get('objects', [])
                if objects and isinstance(objects, list):
                    # Get the quantity from the first item in the list
                    quantity_dict = objects[0] if objects else {}
                    quantity = next(iter(quantity_dict.values()), 'N/A')
            except (SyntaxError, ValueError):
                quantity = 'Invalid format'

        booking_data.append({
            'user': booking.user.username if booking.user else 'Unknown',
            'quantity': quantity,
            'total': booking.total,
            'status': dict(ORDERSTATUS).get(booking.status, 'Unknown'),
            'created': booking.created,
            'updated': booking.updated,
        })

    return render(request, 'booking_list.html', {'bookings': booking_data})

#user_product summary
from django.shortcuts import render
from .models import Booking
import ast
from collections import defaultdict

def user_product_summary(request):
    # Initialize a dictionary to hold aggregated data
    summary = defaultdict(lambda: defaultdict(lambda: {'total_quantity': 0, 'total_value': 0}))

    # Retrieve all bookings
    bookings = Booking.objects.all()
    
    for booking in bookings:
        user = booking.user.username if booking.user else 'Unknown'
        if booking.product:
            try:
                # Safely evaluate the product field to convert it to a dictionary
                product_data = ast.literal_eval(booking.product)
                
                # Extract product ID or name from the product_data dictionary
                objects = product_data.get('objects', [])
                if objects and isinstance(objects, list):
                    quantity_dict = objects[0] if objects else {}
                    quantity = next(iter(quantity_dict.values()), 0)  # Default to 0 if not found
                    
                    # For simplicity, assume product name is a key in the dictionary
                    product_name = next(iter(quantity_dict.keys()), 'Unknown Product')

                    # Aggregate quantities and total values
                    summary[user][product_name]['total_quantity'] += quantity
                    summary[user][product_name]['total_value'] += float(booking.total) if booking.total else 0
            except (SyntaxError, ValueError):
                continue  # Skip invalid product data

    # Convert defaultdict to a regular dict for template rendering
    summary = {user: dict(products) for user, products in summary.items()}
    
    return render(request, 'user_product_summary.html', {'summary': summary})



from django.shortcuts import render
from .models import Booking
from django.db.models import Sum
import json

def get_product_orders(request):
    # Assuming that the product ID you are interested in is passed as a query parameter
    product_id = request.GET.get('product_id')
    
    # Initialize a dictionary to store the aggregated data
    aggregated_data = {}

    # Fetch all bookings
    bookings = Booking.objects.all()

    # Iterate through bookings and aggregate data
    for booking in bookings:
        if booking.product:
            try:
                # Assuming the product field is a JSON string
                products = json.loads(booking.product)
                for item in products:
                    prod_id = item.get('id')  # Adjust key names based on your JSON structure
                    quantity = item.get('quantity')
                    if prod_id == product_id:
                        if prod_id in aggregated_data:
                            aggregated_data[prod_id] += quantity
                        else:
                            aggregated_data[prod_id] = quantity
            except json.JSONDecodeError:
                continue  # Handle invalid JSON formats

    # Render results to a template
    return render(request, 'product_orders.html', {'aggregated_data': aggregated_data})


   

#query no 3 
from django.shortcuts import render
from .models import Booking, Product
import ast
from collections import defaultdict

def product_quantity_summary(request):
    # Initialize dictionary to hold aggregated data
    summary = defaultdict(lambda: {'order_count': 0, 'name': 'Unknown'})
    order_counts = defaultdict(int)  # To track the number of orders for each product

    # Retrieve all bookings
    bookings = Booking.objects.all()

    for booking in bookings:
        if booking.product:
            try:
                # Safely evaluate the product field to convert it to a dictionary
                product_data = ast.literal_eval(booking.product)

                # Extract product ID from the product_data dictionary
                objects = product_data.get('objects', [])
                if objects and isinstance(objects, list):
                    quantity_dict = objects[0] if objects else {}
                    # Assume product ID is a key in the dictionary
                    product_id = next(iter(quantity_dict.keys()), 'Unknown Product')

                    # Retrieve product name
                    product = Product.objects.filter(id=product_id).first()
                    product_name = product.name if product else 'Unknown Product'

                    # Aggregate order counts
                    summary[product_id]['order_count'] += 1
                    summary[product_id]['name'] = product_name

                    # Track order count
                    order_counts[product_id] += 1
            except (SyntaxError, ValueError):
                continue  # Skip invalid product data

    # Filter out products with fewer than 5 orders
    filtered_summary = {product_id: details for product_id, details in summary.items() if order_counts[product_id] >= 5}

    # Sort products by the number of orders in descending order
    sorted_summary = sorted(filtered_summary.items(), key=lambda item: item[1]['order_count'], reverse=True)

    # Convert the sorted list of tuples back to a dictionary
    sorted_summary = dict(sorted_summary)

    return render(request, 'product_quantity_summary.html', {'summary': sorted_summary})



#weekly order data 
from django.db.models import Count
from django.db.models.functions import ExtractWeek
from .models import Booking
import datetime

def get_weekly_orders_q1_2024():
    # Define the start and end dates for Q1 2024
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 3, 31)

    # Calculate the week number for each booking
    bookings = Booking.objects.filter(
        created__date__range=(start_date, end_date)
    ).annotate(
        week_number=ExtractWeek('created')
    ).values(
        'week_number'
    ).annotate(
        total_orders=Count('id')
    ).order_by('week_number')

    # Calculate the range of weeks
    weeks_range = range(
        start_date.isocalendar()[1],  # Starting week number
        end_date.isocalendar()[1] + 1  # Ending week number (inclusive)
    )

    # Generate all weeks in the range with default orders set to 0
    weeks = {week: 0 for week in weeks_range}

    # Populate weeks with actual data
    for booking in bookings:
        week_number = booking['week_number']
        if week_number in weeks:
            weeks[week_number] = booking['total_orders']

    # Convert weeks to a list of dicts for easy use in the template
    weekly_data = [{'week_number': week, 'total_orders': orders} for week, orders in weeks.items()]
    
    return weekly_data


from django.shortcuts import render

def weekly_orders_q1_2024(request):
    bookings = get_weekly_orders_q1_2024()
    return render(request, 'weekly_orders_q1_2024.html', {'bookings': bookings})







#query 4
from django.shortcuts import render
from .models import Booking
from collections import defaultdict
import ast

def parse_product_field(product_field):
    """Parse the product field to return a dictionary of product IDs and quantities."""
    try:
        # Example parsing logic; adjust according to the actual format of your `product` field
        return ast.literal_eval(product_field)
    except (ValueError, SyntaxError):
        return {}

def product_sales_view(request):
    # Define a dictionary to count product sales
    product_sales = defaultdict(int)
    
    # Filter bookings for the first quarter of 2024
    bookings = Booking.objects.filter(created__year=2024, created__month__lte=3)
    
    for booking in bookings:
        # Parse product data from the booking
        products = parse_product_field(booking.product)
        
        for product_id, qty in products.items():
            product_sales[product_id] += qty
    
    # Find products sold more than 7 times
    sold_more_than_7 = {product_id: qty for product_id, qty in product_sales.items() if qty > 5}
    
    # For the sake of this example, assume we have a set of all possible product IDs.
    # If you don't have this, you might need to get this information from your data source.
    all_product_ids = set(product_sales.keys())
    
    # Assuming you have a list of all possible product IDs (this is a placeholder)
    all_possible_product_ids = set()  # Replace with actual product IDs from a data source if available

    # Find products not sold yet
    not_sold_yet = all_possible_product_ids - all_product_ids
    
    context = {
        'sold_more_than_7': sold_more_than_7,
        'not_sold_yet': not_sold_yet,
    }
    return render(request, 'product_sales.html', context)


#sold_product at dashboard
from django.shortcuts import render
from .models import Booking, Product
import ast
from collections import defaultdict

def sold_product(request):
    # Initialize dictionary to hold aggregated data
    product_summary = defaultdict(lambda: {'order_count': 0, 'total_quantity': 0, 'name': 'Unknown'})

    # Retrieve all bookings
    bookings = Booking.objects.all()

    for booking in bookings:
        if booking.product:
            try:
                # Safely evaluate the product field to convert it to a dictionary
                product_data = ast.literal_eval(booking.product)

                # Extract product ID from the product_data dictionary
                objects = product_data.get('objects', [])
                if objects and isinstance(objects, list):
                    quantity_dict = objects[0] if objects else {}
                    # Assume product ID is a key in the dictionary
                    for product_id, quantity in quantity_dict.items():
                        # Aggregate order counts and quantities
                        product_summary[product_id]['order_count'] += 1
                        product_summary[product_id]['total_quantity'] += quantity
            except (SyntaxError, ValueError):
                continue  # Skip invalid product data

    # Retrieve product names and combine with aggregated data
    for product_id in product_summary:
        product = Product.objects.filter(id=product_id).first()
        product_summary[product_id]['name'] = product.name if product else 'Unknown Product'

    # Sort products by total quantity in descending order
    sorted_summary = sorted(product_summary.items(), key=lambda item: item[1]['total_quantity'], reverse=True)

    # Convert the sorted list of tuples back to a dictionary
    sorted_summary = dict(sorted_summary)

    return render(request, 'sold_product.html', {'summary': sorted_summary})




#unsold products
from django.shortcuts import render
from .models import Product, Booking
import ast
from collections import defaultdict

def unsold_product(request):
    # Initialize dictionaries to hold aggregated data
    product_summary = defaultdict(lambda: {'order_count': 0, 'total_quantity': 0, 'name': 'Unknown'})
    
    # Get all bookings and aggregate data for sold products
    bookings = Booking.objects.all()
    for booking in bookings:
        if booking.product:
            try:
                product_data = ast.literal_eval(booking.product)
                objects = product_data.get('objects', [])
                if objects and isinstance(objects, list):
                    quantity_dict = objects[0] if objects else {}
                    for product_id, quantity in quantity_dict.items():
                        # Aggregate order counts and quantities for sold products
                        product_summary[product_id]['order_count'] += 1
                        product_summary[product_id]['total_quantity'] += quantity
            except (SyntaxError, ValueError):
                continue

    # Retrieve all products and ensure both sold and unsold products are included
    all_products = Product.objects.all()
    for product in all_products:
        product_id = str(product.id)
        # Add product data to the summary, if it wasn't already added (i.e., unsold product)
        if product_id not in product_summary:
            product_summary[product_id] = {'order_count': 0, 'total_quantity': 0, 'name': product.name}
        else:
            product_summary[product_id]['name'] = product.name

    # Sort products by total quantity in descending order
    sorted_summary = sorted(product_summary.items(), key=lambda item: item[1]['total_quantity'], reverse=True)

    # Convert the sorted list of tuples back to a dictionary
    sorted_summary = dict(sorted_summary)

    return render(request, 'query5.html', {'summary': sorted_summary})


from django.shortcuts import render
from .models import Product, Booking
import ast

def query5(request):
    # Get all product IDs from bookings
    sold_product_ids = set()
    bookings = Booking.objects.all()
    for booking in bookings:
        if booking.product:
            try:
                product_data = ast.literal_eval(booking.product)
                objects = product_data.get('objects', [])
                if objects and isinstance(objects, list):
                    quantity_dict = objects[0] if objects else {}
                    sold_product_ids.update(quantity_dict.keys())
            except (SyntaxError, ValueError):
                continue
    
    # Get all products and filter out the ones that have been sold
    all_products = Product.objects.all()
    unsold_products = [product for product in all_products if str(product.id) not in sold_product_ids]

    return render(request, 'query5.html', {'unsold_products': unsold_products})


from django.shortcuts import render
from .models import Product, Booking
import ast
from collections import defaultdict

def query6(request):
    # Initialize a dictionary to hold aggregated data for products
    product_summary = defaultdict(lambda: {'order_count': 0, 'total_quantity': 0, 'name': 'Unknown'})
    
    # Retrieve all bookings and aggregate data for sold products
    bookings = Booking.objects.all()
    for booking in bookings:
        if booking.product:
            try:
                product_data = ast.literal_eval(booking.product)
                objects = product_data.get('objects', [])
                if objects and isinstance(objects, list):
                    quantity_dict = objects[0] if objects else {}
                    for product_id, quantity in quantity_dict.items():
                        # Aggregate order counts and quantities for sold products
                        product_summary[product_id]['order_count'] += 1
                        product_summary[product_id]['total_quantity'] += quantity
            except (SyntaxError, ValueError):
                continue

    # Retrieve all products and include them in the summary
    all_products = Product.objects.all()
    for product in all_products:
        product_id = str(product.id)
        # Add product data to the summary, if it wasn't already added (i.e., unsold product)
        if product_id not in product_summary:
            product_summary[product_id] = {'order_count': 0, 'total_quantity': 0, 'name': product.name}
        else:
            product_summary[product_id]['name'] = product.name

    # Apply the constraints:
    # 1. Product is unsold (i.e., `order_count` is 0)
    # 2. Product has a total quantity greater than 7
    filtered_summary = {
        product_id: data for product_id, data in product_summary.items()
        if data['order_count'] == 0 or data['total_quantity'] > 7
    }

    # Sort filtered products by total quantity in descending order
    sorted_summary = sorted(filtered_summary.items(), key=lambda item: item[1]['total_quantity'], reverse=True)

    # Convert the sorted list of tuples back to a dictionary
    sorted_summary = dict(sorted_summary)

    return render(request, 'query5.html', {'summary': sorted_summary})

#final query no 4
from django.shortcuts import render
from .models import Product, Booking
import ast
from collections import defaultdict
from datetime import datetime

def query7(request):
    # Define the start and end dates (time part will be handled by Django automatically)
    start_date = datetime(2024, 1, 1).date()
    end_date = datetime(2024, 3, 31).date()

    # Initialize a dictionary to hold aggregated data for products
    product_summary = defaultdict(lambda: {'order_count': 0, 'total_quantity': 0, 'name': 'Unknown'})
    
    # Retrieve bookings within the specified date range and aggregate data
    bookings = Booking.objects.filter(created__date__range=(start_date, end_date))
    for booking in bookings:
        if booking.product:
            try:
                product_data = ast.literal_eval(booking.product)
                objects = product_data.get('objects', [])
                if objects and isinstance(objects, list):
                    quantity_dict = objects[0] if objects else {}
                    for product_id, quantity in quantity_dict.items():
                        # Aggregate order counts and quantities for sold products within date range
                        product_summary[product_id]['order_count'] += 1
                        product_summary[product_id]['total_quantity'] += quantity
            except (SyntaxError, ValueError):
                continue

    # Retrieve all products and include them in the summary
    all_products = Product.objects.all()
    for product in all_products:
        product_id = str(product.id)
        if product_id not in product_summary:
            product_summary[product_id] = {'order_count': 0, 'total_quantity': 0, 'name': product.name}
        else:
            product_summary[product_id]['name'] = product.name

    # Apply the constraints:
    # 1. Product is unsold (i.e., `order_count` is 0)
    # 2. Product has a total quantity greater than 7
    # 3. Product must be sold between April and August 2024
    filtered_summary = {
        product_id: data for product_id, data in product_summary.items()
        if data['order_count'] == 0 or data['total_quantity'] > 7
    }

    # Sort filtered products by total quantity in descending order
    sorted_summary = sorted(filtered_summary.items(), key=lambda item: item[1]['total_quantity'], reverse=True)

    # Convert the sorted list of tuples back to a dictionary
    sorted_summary = dict(sorted_summary)

    return render(request, 'query7.html', {'summary': sorted_summary})

# update the date of the booking
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from .models import Booking

def update_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        created_str = request.POST.get('created')
        updated_str = request.POST.get('updated')

        if created_str:
            created_date = parse_datetime(created_str)
            if created_date:
                booking.created = created_date
        if updated_str:
            updated_date = parse_datetime(updated_str)
            if updated_date:
                booking.updated = updated_date
        
        booking.save()
        return redirect('booking_list')  # Redirect to a list view or any other page

    context = {
        'booking': booking,
    }
    return render(request, 'update_booking.html', context)




#final query 2 
from django.shortcuts import render
from datetime import datetime, timedelta
from collections import defaultdict

# Set date range for the first quarter of 2024
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 3, 31, 23, 59, 59)

# Weekly Orders Query without Postgres
def query2(request):
    # Filter bookings within Q1 of 2024
    bookings = Booking.objects.filter(created__range=[start_date, end_date])
    
    # Generate all weeks of Q1 2024
    all_weeks = defaultdict(int)  # Default dict with all weeks of Q1
    
    # Loop through Q1 weeks and initialize with 0 orders
    current_date = start_date
    while current_date <= end_date:
        week_number = int(current_date.strftime('%U'))+1  # Get week number
        all_weeks[week_number] = 0  # Initialize with 0 orders
        current_date += timedelta(days=7)  # Move to next week
    
    # Count the number of orders per week
    for booking in bookings:
        week_number = int(booking.created.strftime('%U'))  + 1 # Get week number of the booking
        all_weeks[week_number] +=1
          # Increment order count for that week
    
    # Convert the dictionary to a sorted list for display
    weekly_orders = sorted(all_weeks.items())
    
    context = {
        'weekly_orders': weekly_orders
    }
    
    return render(request, 'query2.html', context)


#final query 1
from django.shortcuts import render
from .models import Booking
import ast
from collections import defaultdict

def user_product_summary2(request):
    # Initialize a dictionary to hold aggregated data
    summary = defaultdict(lambda: {'total_quantity': 0, 'total_value': 0, 'product_count': 0})

    # Retrieve all bookings
    bookings = Booking.objects.all()
    
    for booking in bookings:
        user = booking.user.username if booking.user else 'Unknown'
        if booking.product:
            try:
                # Safely evaluate the product field to convert it to a dictionary
                product_data = ast.literal_eval(booking.product)
                print(f"Product Data: {product_data}")  # Debug print

                # Extract product ID or name from the product_data dictionary
                objects = product_data.get('objects', [])
                if objects and isinstance(objects, list):
                    quantity_dict = objects[0] if objects else {}
                    quantity = next(iter(quantity_dict.values()), 0)  # Default to 0 if not found
                    product_name = next(iter(quantity_dict.keys()), 'Unknown Product')

                    # Aggregate quantities and total values
                    summary[user]['total_quantity'] += quantity
                    summary[user]['total_value'] += float(booking.total) if booking.total else 0
                    summary[user]['product_count'] += 1  # Count each product purchased
            except (SyntaxError, ValueError):
                print(f"Invalid product data: {booking.product}")  # Debug print
                continue  # Skip invalid product data

    # Convert defaultdict to a regular dict for template rendering
    summary = dict(summary)
    
    print(f"Summary: {summary}")  # Debug print

    return render(request, 'user_product_summary2.html', {'summary': summary})


