# Burger Rush Restaurant

Burger Rush is a full-stack web application for managing a modern restaurant, including menu, orders, rewards, and delivery. The project is built with Python (Flask), MySQL, and a responsive HTML/CSS/JS frontend.

## Features
- User registration and authentication
- Menu browsing and dynamic cart
- Points and rewards system
- Order and delivery management
- Admin and support modules
- Responsive web design

## Project Structure
```
Restaurante/
├── Base_de_Datos/           # Database scripts and diagrams
├── Logica/                  # Backend logic (Flask app)
│   ├── app/                 # Main application code
│   │   ├── routes/          # API endpoints (Flask Blueprints)
│   │   ├── services/        # Business logic/services
│   │   ├── utils/           # Utilities and validators
│   │   ├── models.py        # SQLAlchemy models
│   │   └── ...
│   └── ...
├── Pagina_Web/              # Frontend (HTML, CSS, JS)
│   └── template_folder/
│       ├── templates/       # HTML templates
│       └── static/          # Static files (css, js, images)
├── requirements.txt         # Python dependencies
├── main.py                  # App entry point
└── README.md                # Project documentation
```

## Setup Instructions
1. **Clone the repository**
2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the database**
   - Use the SQL script in `Base_de_Datos/RestauranteWKDB.sql` to create the MySQL schema.
   - Update your database URI in the Flask config if needed.
4. **Run the backend**
   ```bash
   python main.py
   ```
5. **Access the frontend**
   - Open `Pagina_Web/template_folder/templates/index.html` in your browser, or set up Flask to serve templates.

## Technologies Used
- Python 3, Flask, SQLAlchemy
- MySQL
- HTML5, CSS3, JavaScript (Vanilla)
- Stripe (for payment simulation)

## Authors
- Developed by Megaroba, YadielTorres, OscarLopez2002

## License
This project is for educational purposes.

## Link de un video explicando el proyecto en YouTube
https://youtu.be/1Xa00wyyTdM 

