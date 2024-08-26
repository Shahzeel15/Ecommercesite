<h1>E-Commerce Website</h1>

<h2>Description</h2>
This is a fully functional e-commerce website developed using Python with Django and SQLite for the database schema. The platform supports a comprehensive range of features, including user sign-up, login, and account management. Users can browse and filter products by various categories, manage their shopping cart, place orders, view order history, and track their shipments.
The website also includes an administrative interface that allows administrators to manage users, categories, products, and orders. Additionally, the admin panel provides analytical features to generate insights and data. The backend ensures a smooth and efficient experience for handling user accounts, processing orders, and managing shopping carts.

<h2>Admin and User Credentials</h2>
<h4> admin password := </h4>
    username : admin <br>
    password : admin

<h4>User password</h4>

user1 := <br>
username:nidhi@gmail.com<br>
password: nidhi <br>

user 2 := <br>
username : palak@gmail.com<br>
password : palak <br>

<h2>Models</h2>
<li><b>Carousel:</b> This model manages dynamic carousel items for the website's homepage, including a title, description, and image for each carousel item.</li>

<li><b>Category :</b> Represents product categories on the site, allowing products to be organized into distinct groups with names and creation timestamps.</li>

<li><b>Product:</b> Stores information about products available for purchase, including category, name, image, description, price, discount, and timestamps for creation and updates.</li>

<li><b>UserProfile:</b> Extends the default Django User model with additional user-specific details such as mobile number, address, and profile image.</li>

<li><b>Cart:</b> Keeps track of products added to a user's shopping cart, associated with a specific user and storing the products in a serialized format.</li>

<li><b>Booking:</b> Represents orders placed by users, including product details, quantity, total amount, status, and timestamps for order creation and updates.</li>

<h2>Pages and Features</h2>
 <li><b>User Login and Admin Login</b>: Secure login pages for users to access their accounts and administrators to manage site operations.</li> <li><b>User Signup</b>: Registration page for new users to create an account with necessary details.</li> <li><b>Product Viewing and Filtering</b>: Users can browse products, apply filters by category, and view detailed product information.</li> <li><b>Shopping Cart Management</b>: Users can add or remove items from their cart and proceed to checkout.</li> <li><b>Profile Management</b>: Users can update their personal information and profile image.</li> <li><b>Password Management</b>: Users can change their passwords for improved security.</li> <li><b>Order History</b>: Users can view their past orders, track their status, and review order details.</li> <li><b>Order Tracking</b>: Users can track the status of their current orders in real time.</li> <li><b>Admin Dashboard</b>: A comprehensive dashboard for administrators to view and analyze data from all tables with various perspectives.</li> <li><b>Category Management</b>: Admins can add, update, or delete product categories.</li> <li><b>Product Management</b>: Admins can add, update, or delete products from the inventory.</li> <li><b>Order Management</b>: Admins can analyze different order statuses, manage orders, and change their statuses as needed.</li> <li><b>Order Details</b>: Admins can view detailed information about each order and track its status.</li> <li><b>User Management</b>: Admins can manage user accounts, including the ability to delete users.</li> <li><b>Admin Password Management</b>: Admins can change their passwords to ensure account security.</li> 

<h2>Task : 2 </h2>
<li><b>query : 1 </b> Find User wise - product-wise ordering quantity with total item value</li>
<li><b>query : 2 </b>Weekly Orders analysis for the first quarter of 2024</li>
<li><b>query : 3 </b>Retrieve the Product name and No. of Orders from Sales. Exclude products with fewer than 5 Orders</li>
<li><b>query : 4 </b>Find the products that are sold more than 7 times or have not sold yet in the first quarter of 2024</li>
