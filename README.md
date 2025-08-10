# 🔥 Fire Detection Dashboard System

A comprehensive web-based dashboard system for monitoring fire detection sensors and drone surveillance in Greece. Built with Flask, Supabase, and modern web technologies.

## 🌟 Features

### 📊 **Dashboard Overview**
- **Real-time Map Visualization**: Interactive map showing sensor node locations
- **Database Connection Status**: Live monitoring of database connectivity
- **Regional Access Control**: Secure access based on user's region
- **Professional UI**: Modern, responsive design with Greek localization

### 🛰️ **Sensor Network Management**
- **Node Monitoring**: Real-time status of fire detection sensors
- **Parent-Child Hierarchy**: Organized sensor network structure
- **Historical Data**: Access to sensor readings and history
- **Regional Filtering**: View nodes specific to user's region

### 🚁 **Drone Surveillance (ΣΜΗΕΑ)**
- **Live Telemetry**: Real-time drone position and status
- **Fire Detection**: Automated fire detection with confidence levels
- **Flight Monitoring**: Battery status, altitude, and speed tracking
- **Interactive Map**: Visual drone location and movement

### 🔐 **Security & Access Control**
- **Session Management**: Secure user sessions
- **Regional Permissions**: Access control based on user region
- **Database Security**: Encrypted connections and secure queries
- **Error Handling**: Comprehensive error management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd dashboard_code
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the dashboard**
   - Open your browser and go to `http://localhost:5000`
   - Select your region and start monitoring

## 📁 Project Structure

```
dashboard_code/
├── app/                          # Application package
│   ├── __init__.py              # Application factory
│   ├── main.py                  # Main web routes
│   ├── api.py                   # API endpoints
│   ├── database.py              # Database management
│   └── errors.py                # Error handlers
├── templates/                    # HTML templates
│   ├── index.html               # Dashboard main page
│   ├── nodes.html               # Sensor nodes page
│   ├── drone.html               # Drone surveillance page
│   ├── node.html                # Individual node details
│   ├── parent_node.html         # Parent node reports
│   ├── history.html             # Historical data
│   ├── login.html               # Login page
│   └── error.html               # Error pages
├── Database/                     # SQL scripts
│   ├── CreateTable(ALL).sql    # Database schema
│   ├── Functions.sql           # Database functions
│   └── Insert(ALL).sql        # Sample data
├── config.py                    # Configuration management
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── env.example                  # Environment variables example
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🎯 Key Components

### **Application Factory (`app/__init__.py`)**
- **Blueprint Registration**: Modular route organization
- **Configuration Management**: Environment-based settings
- **Extension Initialization**: Cache and other extensions
- **Error Handler Registration**: Centralized error management

### **Database Layer (`app/database.py`)**
- **Connection Management**: Automatic retry and error handling
- **Mock Data Support**: Fallback when database is unavailable
- **Query Abstraction**: Clean interface for database operations
- **Logging Integration**: Comprehensive error logging

### **Main Routes (`app/main.py`)**
- **Session Management**: User authentication and region selection
- **Route Organization**: Clean separation of concerns
- **Error Handling**: Proper HTTP status codes
- **Security Validation**: Regional access control

### **API Endpoints (`app/api.py`)**
- **RESTful Design**: Clean API structure
- **Health Checks**: System monitoring endpoints
- **Real-time Data**: Drone telemetry and sensor data
- **Error Responses**: Proper error handling

## 🔧 Configuration

### Environment Variables
Create a `.env` file based on `env.example`:

```bash
# Flask Configuration
FLASK_CONFIG=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Database Configuration
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

### Database Setup
1. Create a Supabase project
2. Update the connection details in your `.env` file
3. Run the SQL scripts in the `Database/` folder

### Regional Configuration
The system supports 13 Greek fire departments:
- Ανατολικής Μακεδονίας και Θράκης
- Κεντρικής Μακεδονίας
- Δυτικής Μακεδονίας
- Ηπείρου
- Θεσσαλίας
- Ιονίων Νήσων
- Δυτικής Ελλάδας
- Στερεάς Ελλάδας
- Αττικής
- Πελοποννήσου
- Βορείου Αιγαίου
- Νοτίου Αιγαίου
- Κρήτης

## 📊 Features in Detail

### **Dashboard (`/dashboard`)**
- Interactive map with sensor locations
- Real-time database status indicator
- Node list with quick access links
- System information footer

### **Nodes Management (`/nodes`)**
- Comprehensive node listing
- Statistics dashboard
- Parent/child node distinction
- Quick access to details and history

### **Drone Surveillance (`/drone`)**
- Live drone telemetry
- Real-time position tracking
- Fire detection alerts
- Flight information display

### **Individual Node Details (`/node/<id>`)**
- Detailed sensor information
- Latest readings
- Historical data access
- Node-specific actions

## 🛠️ Development

### Project Structure Benefits
- **Modularity**: Blueprint-based organization
- **Maintainability**: Clear separation of concerns
- **Scalability**: Easy to add new features
- **Testing**: Isolated components for testing
- **Configuration**: Environment-based settings

### Adding New Features
1. **Backend**: Add routes in appropriate blueprint
2. **Database**: Extend `DatabaseManager` class
3. **Frontend**: Create templates in `templates/`
4. **Configuration**: Update `config.py` if needed

### Testing
```bash
# Run with mock data (no database required)
FLASK_CONFIG=testing python run.py

# Run with development settings
FLASK_CONFIG=development python run.py

# Run with production settings
FLASK_CONFIG=production python run.py
```

### Deployment
1. Set production environment variables
2. Configure proper database credentials
3. Enable HTTPS for security
4. Set up monitoring and logging
5. Use a production WSGI server (Gunicorn, uWSGI)

## 🔒 Security Considerations

- **Session Security**: Secure session management
- **Database Security**: Encrypted connections
- **Access Control**: Regional permission system
- **Input Validation**: Sanitized user inputs
- **Error Handling**: Secure error messages
- **Environment Variables**: Sensitive data protection

## 📈 Performance

- **Caching**: Flask-Caching for improved performance
- **Optimized Queries**: Efficient database queries
- **Responsive Design**: Fast loading on all devices
- **Real-time Updates**: Efficient data polling
- **Connection Pooling**: Database connection optimization

## 🧪 API Documentation

### Health Check
```http
GET /api/health
```
Returns system health status and database connection status.

### Drone Telemetry
```http
GET /api/drone_telemetry
```
Returns real-time drone telemetry data including position, battery, and fire detection status.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the project structure
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

## 📞 Support

For technical support or questions:
- **Email**: kopisto@cs.duth.gr
- **Version**: 2.0.0
- **Last Updated**: 02/08/2025

## 📄 License

This project is developed for the Greek Fire Department system. All rights reserved.

---

**Built with ❤️ for Fire Safety in Greece** 