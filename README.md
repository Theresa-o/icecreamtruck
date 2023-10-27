
# Ice Cream Truck Management System

This is the README file for the Ice Cream Truck Management System. This system is designed to manage the operations of ice cream trucks, including tracking food items, sales, and customer purchases.


## Installation

To set up the Ice Cream Truck Management System, follow these steps:

- Clone the Repository: First, clone the repository to your local machine.

```bash
git clone https://github.com/Theresa-o/icecreamtruck.git
```

- Create a Virtual Environment: It's a good practice to create a virtual environment to manage your project's dependencies. You can use virtualenv or venv. Here's how to create one using venv:

```bash
python -m venv ice-cream-venv
```

- Activate the virtual environment:

- Windows:

```bash
ice-cream-venv\Scripts\activate
```

- Linux/macOS:

```bash
source ice-cream-venv/bin/activate
```
    
- Install Dependencies: While in your virtual environment, navigate to the project's root directory (where requirements.txt is located) and install the required packages using pip:

```bash
cd icecreamcommerce
pip install -r requirements.txt
```
- Database Setup: Configure your database settings in the project's settings.py file. By default, the project is configured to use the SQLite database. You can change this to another database system (e.g., PostgreSQL or MySQL) if needed.

- Migrate Database: Apply the database migrations to create the necessary tables in the database:

```bash
python manage.py migrate
```

- Create an Admin User: You can create a superuser who can access the Django admin interface to manage the application:

```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin user.

- Run the Development Server: Start the Django development server:

```bash
python manage.py runserver
```
The development server should now be running, and you can access the application at http://localhost:8000/.

- Access the Admin Interface: You can access the Django admin interface at http://localhost:8000/admin/ and log in with the superuser account you created earlier.

- API Endpoints: You can access the API endpoints as described in the README at the appropriate URLs, such as http://localhost:8000/api/purchase/ or http://localhost:8000/api/inventory/.

Your Ice Cream Truck Management System is now set up and ready for use. You can customize the system, add data, and interact with the API endpoints as needed.
    
## Models
### Truck
The Truck model represents an ice cream truck. Each truck has a name and can be associated with multiple sales. The total_sales method calculates the total sales for the truck.

### FoodItem
The FoodItem model tracks different food items sold by the ice cream truck. It includes fields for the name, price, quantity, item type (e.g., ice cream, shaved ice, snack bar), image, and a foreign key reference to the truck it belongs to. The FoodFlavor model is used to represent flavors associated with food items.

### Sale
The Sale model tracks individual purchase transactions made by customers. It includes fields for the truck, food item, user (if authenticated), quantity, and purchase time.

### Serializers
The system uses serializers to convert model data into JSON format for API endpoints.

- FoodFlavorSerializer: Serializes food item flavors.
- FoodItemSerializer: Serializes food items and their associated flavors.
- UserSerializer: Serializes customer data.
- TruckSerializer: Serializes the truck model, including total sales and associated food items.
- PurchaseSerializer: Validates and serializes purchase data.
- CreateTruckSerializer: Serializes data for creating a new truck.
- CreateFoodItemSerializer: Serializes data for creating a new food item.
- SaleSerializer: Serializes sales data.

## API Endpoints
The system provides the following API endpoints:
-
### Purchase
- URL: /api/purchase/
- Method: POST
- Description: Allows customers to make a purchase from the ice cream truck by specifying the food item ID and the quantity they want to purchase. If the food item is found and the quantity is available, the purchase is successful, and the response message is 'ENJOY!'. If the food item is not found, a 404 Not Found response is returned. If the quantity is not available, a 400 Bad Request response is returned with the message 'SORRY!'.

### Inventory
- URL: /api/inventory/
- Method: GET
- Description: Returns a list of all ice cream trucks along with their inventory of food items and total sales.

### Trucks
- URL: /api/trucks/
- Method: GET
- Description: Allows users to view a list of all ice cream trucks.
### Create Truck
- URL: /api/create-truck/
- Method: POST
- Description: Allows users to create a new ice cream truck by providing a name for the truck. If the name is provided, a new ice cream truck is created, and the response message is 'Ice cream truck created successfully'. If the name is missing, a 400 Bad Request response is returned with the message 'Truck name is required.'
### Create Food Item
- URL: /api/create-food-item/<truck_id>/
- Method: POST
- Description: Allows users to add new food items to a specific ice cream truck. The endpoint expects a JSON body containing the data for the new food items.
## Running Tests

### Testing
The system includes unit tests for models, serializers, and API views. These tests ensure that the system's components are functioning correctly. To run the tests, you can use the Django test framework.

``` bash
python manage.py test 
```

Please ensure you have set up your development environment and configured your database before running the tests.

