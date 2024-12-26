
# Airport Management System API

This project is a Django REST Framework-based API for managing airport operations, including airplanes, flights, routes, orders, and more. The API supports role-based access control where regular users can only create orders, while administrators have full access to all endpoints.

---

## **Features**

- **Airplane Management**: Manage airplane types, airplanes, and their capacities.
- **Airport Management**: Manage airports and their closest big cities.
- **Route Management**: Create and retrieve flight routes between airports.
- **Flight Management**: Manage flight schedules and availability.
- **Order Management**: Users can book tickets for flights.
- **Authentication**: JWT-based authentication with email as the primary login field.

---

## **Installation**

### **Step 1: Clone the repository**

```bash
git clone <repository_url>
cd <repository_name>
```

### **Step 2: Set up a virtual environment**

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Environment Variables**

Create a `.env` file in the project root directory and add the following variables:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
```

---

## **Database Setup**

Run the following commands to apply migrations and populate the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## **Superuser Creation**

To access admin-level endpoints, create a superuser:

```bash
python manage.py createsuperuser
```

---

## **Run the Server**

Start the development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## **API Endpoints**

### **Authentication**

- **Login**: `/api/user/token/` (POST)  
  Request a JWT token by providing email and password.  
- **Refresh Token**: `/api/user/token/refresh/` (POST)  
  Refresh an expired token.

---

### **Airplane Types**

- **List Airplane Types**: `/api/airplane-types/` (GET)  
  Accessible to all users.
- **Create Airplane Type**: `/api/airplane-types/` (POST)  
  Admin only.

---

### **Airplanes**

- **List Airplanes**: `/api/airplanes/` (GET)  
  Accessible to all users.
- **Create Airplane**: `/api/airplanes/` (POST)  
  Admin only.

---

### **Airports**

- **List Airports**: `/api/airports/` (GET)  
  Accessible to all users.
- **Create Airport**: `/api/airports/` (POST)  
  Admin only.

---

### **Routes**

- **List Routes**: `/api/routes/` (GET)  
  Accessible to all users.
- **Create Route**: `/api/routes/` (POST)  
  Admin only.

---

### **Flights**

- **List Flights**: `/api/flights/` (GET)  
  Accessible to all users.  
  Supports filters:
  - `route_source`: Filter by source airport.
  - `route_destination`: Filter by destination airport.
  - `departure_date`: Filter by departure date.
  - `arrival_date`: Filter by arrival date.

- **Create Flight**: `/api/flights/` (POST)  
  Admin only.

---

### **Orders**

- **List Orders**: `/api/orders/` (GET)  
  Accessible to authenticated users.  
- **Create Order**: `/api/orders/` (POST)  
  Accessible to authenticated users.

---

## **Testing**

Run the test suite to ensure everything is working as expected:

```bash
python manage.py test
```

---

## **Project Structure**

```
project/
├── airport/
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── permissions.py     # Custom permissions
│   ├── urls.py            # API routes
│   └── tests/
│       ├── test_models.py # Model tests
│       ├── test_views.py  # ViewSet tests
│       ├── test_serializers.py # Serializer tests
│       └── test_permissions.py # Permission tests
├── manage.py
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## **Technologies Used**

- **Backend**: Django, Django REST Framework
- **Authentication**: Simple JWT
- **Database**: SQLite (default), can be replaced with PostgreSQL or MySQL
- **Testing**: Django TestCase

---

## **Contributing**

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.
