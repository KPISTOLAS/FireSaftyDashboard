# Project Structure Documentation

## Overview

The Fire Detection Dashboard System has been reorganized into a professional, modular structure following Flask best practices and modern development standards.

## Directory Structure

```
dashboard_code/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory and blueprint registration
│   ├── main.py                  # Main web routes and pages
│   ├── api.py                   # API endpoints and RESTful services
│   ├── database.py              # Database connection and query management
│   └── errors.py                # Error handlers and custom error pages
├── templates/                    # HTML templates and frontend
│   ├── index.html               # Dashboard main page
│   ├── nodes.html               # Sensor nodes listing
│   ├── drone.html               # Drone surveillance interface
│   ├── node.html                # Individual node details
│   ├── parent_node.html         # Parent node reports
│   ├── history.html             # Historical data views
│   ├── login.html               # Authentication page
│   └── error.html               # Error page templates
├── Database/                     # Database scripts and migrations
│   ├── CreateTable(ALL).sql    # Database schema creation
│   ├── Functions.sql           # Database functions and procedures
│   └── Insert(ALL).sql        # Sample data insertion
├── tests/                       # Test suite
│   ├── __init__.py             # Test package initialization
│   └── test_database.py        # Database functionality tests
├── config.py                    # Configuration management
├── run.py                       # Application entry point
├── setup.py                     # Automated setup script
├── migrate.py                   # Migration helper script
├── requirements.txt             # Python dependencies
├── env.example                  # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # Main project documentation
├── PROJECT_STRUCTURE.md         # This file
└── MIGRATION_GUIDE.md          # Migration instructions
```

## Key Components

### Application Package (`app/`)

#### `app/__init__.py`
- **Purpose**: Application factory pattern implementation
- **Features**:
  - Blueprint registration
  - Configuration management
  - Extension initialization
  - Error handler registration
- **Benefits**: Modular, testable, scalable architecture

#### `app/main.py`
- **Purpose**: Main web routes and page handlers
- **Features**:
  - Session management
  - Regional access control
  - Route organization
  - Security validation
- **Routes**:
  - `/` - Redirect to login
  - `/login` - Authentication page
  - `/dashboard` - Main dashboard
  - `/nodes` - Node listing
  - `/node/<id>` - Individual node details
  - `/parent/<id>` - Parent node reports
  - `/history/<id>` - Historical data
  - `/drone` - Drone surveillance

#### `app/api.py`
- **Purpose**: RESTful API endpoints
- **Features**:
  - JSON responses
  - Error handling
  - Health checks
  - Real-time data
- **Endpoints**:
  - `/api/drone_telemetry` - Drone telemetry data
  - `/api/health` - System health status

#### `app/database.py`
- **Purpose**: Database connection and query management
- **Features**:
  - Connection pooling
  - Automatic retry logic
  - Mock data fallback
  - Comprehensive logging
  - Query abstraction
- **Classes**:
  - `DatabaseManager` - Main database interface

#### `app/errors.py`
- **Purpose**: Centralized error handling
- **Features**:
  - Custom error pages
  - Logging integration
  - User-friendly messages
- **Handlers**:
  - 404 Not Found
  - 500 Internal Server Error
  - 403 Forbidden
  - Generic exception handler

### Configuration (`config.py`)

#### Configuration Classes
- **Config**: Base configuration with environment variables
- **DevelopmentConfig**: Development-specific settings
- **ProductionConfig**: Production-specific settings
- **TestingConfig**: Testing-specific settings

#### Environment Variables
- `SECRET_KEY`: Flask secret key
- `SUPABASE_URL`: Database connection URL
- `SUPABASE_KEY`: Database authentication key
- `FLASK_DEBUG`: Debug mode toggle
- `HOST`: Server host address
- `PORT`: Server port number
- `DB_RETRY_ATTEMPTS`: Database retry attempts
- `DB_RETRY_DELAY`: Database retry delay

### Entry Point (`run.py`)

#### Features
- Environment-based configuration
- Logging setup
- Application factory usage
- Production-ready startup

### Setup and Migration

#### `setup.py`
- **Purpose**: Automated project setup
- **Features**:
  - Dependency installation
  - Environment file creation
  - Directory setup
  - Version checking

#### `migrate.py`
- **Purpose**: Migration from old structure
- **Features**:
  - File backup
  - Structure validation
  - Migration guide generation

## Benefits of New Structure

### 1. **Modularity**
- Blueprint-based organization
- Clear separation of concerns
- Easy to extend and maintain

### 2. **Scalability**
- Easy to add new features
- Isolated components
- Professional standards

### 3. **Maintainability**
- Clear file organization
- Consistent patterns
- Comprehensive documentation

### 4. **Testing**
- Isolated components
- Mock data support
- Test suite structure

### 5. **Configuration**
- Environment-based settings
- Multiple deployment configurations
- Secure credential management

### 6. **Professional Standards**
- Flask best practices
- Modern Python patterns
- Industry-standard structure

## Development Workflow

### Adding New Features

1. **Backend Routes**
   ```python
   # In app/main.py or app/api.py
   @main.route('/new-feature')
   def new_feature():
       # Implementation
   ```

2. **Database Operations**
   ```python
   # In app/database.py
   def get_new_data(self):
       # Database query
   ```

3. **Frontend Templates**
   ```html
   <!-- In templates/new_feature.html -->
   <!-- Template implementation -->
   ```

4. **Configuration**
   ```python
   # In config.py if needed
   NEW_FEATURE_SETTING = os.environ.get('NEW_FEATURE_SETTING')
   ```

### Testing

```bash
# Run tests
python -m unittest tests/

# Run with specific configuration
FLASK_CONFIG=testing python run.py
```

### Deployment

```bash
# Production deployment
FLASK_CONFIG=production python run.py

# With WSGI server
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Security Considerations

### 1. **Environment Variables**
- Sensitive data in `.env` file
- Not committed to version control
- Production-specific values

### 2. **Session Management**
- Secure session handling
- Regional access control
- Input validation

### 3. **Database Security**
- Encrypted connections
- Query parameterization
- Access control

### 4. **Error Handling**
- Secure error messages
- Comprehensive logging
- User-friendly responses

## Performance Optimizations

### 1. **Caching**
- Flask-Caching integration
- Database query optimization
- Static file caching

### 2. **Connection Management**
- Database connection pooling
- Automatic retry logic
- Resource cleanup

### 3. **Response Optimization**
- Efficient JSON responses
- Minimal data transfer
- Compressed responses

## Monitoring and Logging

### 1. **Application Logging**
- Structured logging
- Error tracking
- Performance monitoring

### 2. **Health Checks**
- `/api/health` endpoint
- Database connectivity
- System status

### 3. **Error Tracking**
- Comprehensive error handlers
- User-friendly messages
- Developer debugging information

## Future Enhancements

### 1. **API Documentation**
- Swagger/OpenAPI integration
- Automated documentation
- Interactive API explorer

### 2. **Testing Suite**
- Unit tests
- Integration tests
- End-to-end tests

### 3. **Deployment Automation**
- CI/CD pipeline
- Docker containerization
- Kubernetes deployment

### 4. **Monitoring Dashboard**
- Real-time metrics
- Performance analytics
- User activity tracking

---

This structure provides a solid foundation for a professional, scalable, and maintainable Flask application following industry best practices. 