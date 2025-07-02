# API Indoor Duration

A FastAPI application for tracking indoor duration with PostgreSQL database and Docker setup.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ with virtual environment
- PostgreSQL client (optional, for direct database access)

### 1. Environment Setup

Copy the environment template and configure your database settings:

```bash
cp env.example .env
```

Edit `.env` file with your database configuration:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=indoor_duration_db

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
APP_RELOAD=true
```

### 2. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirement.txt
```

### 3. Database Setup

Use the database management script for easy setup:

```bash
# Complete setup (start database and run migrations)
python db_manage.py setup

# Or step by step:
python db_manage.py start-db    # Start PostgreSQL
python db_manage.py migrate     # Run migrations
```

### 4. Run the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: http://localhost:8000

## 📊 Database Management

### Using the Management Script

The `db_manage.py` script provides easy database operations:

```bash
# Start PostgreSQL database
python db_manage.py start-db

# Stop PostgreSQL database
python db_manage.py stop-db

# Run all pending migrations
python db_manage.py migrate

# Create a new migration
python db_manage.py create-mig "Add new table"

# Show migration status
python db_manage.py status

# Show migration history
python db_manage.py history

# Reset database (WARNING: deletes all data)
python db_manage.py reset

# Complete setup
python db_manage.py setup
```

### Manual Alembic Commands

If you prefer using Alembic directly:

```bash
# Initialize migrations (first time only)
alembic init alembic

# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Run migrations
alembic upgrade head

# Downgrade to previous version
alembic downgrade -1

# Show current status
alembic current

# Show history
alembic history
```

## 🐳 Docker Setup

### PostgreSQL Container

The `docker-compose.yml` file sets up a PostgreSQL 15 container with:

- Database: `indoor_duration_db`
- User: `postgres`
- Password: `postgres123`
- Port: `5432`
- Timezone: `Asia/Jakarta`

### Manual Docker Commands

```bash
# Start PostgreSQL
docker-compose up -d postgres

# Stop PostgreSQL
docker-compose down

# View logs
docker-compose logs postgres

# Access PostgreSQL shell
docker-compose exec postgres psql -U postgres -d indoor_duration_db
```

## 📁 Project Structure

```
api_indoor_duration/
├── main.py              # FastAPI application
├── models.py            # SQLAlchemy models
├── database.py          # Database configuration
├── db_manage.py         # Database management script
├── docker-compose.yml   # Docker Compose configuration
├── alembic.ini          # Alembic configuration
├── alembic/             # Migration files
│   ├── env.py           # Alembic environment
│   ├── script.py.mako   # Migration template
│   └── versions/        # Migration files
├── init.sql             # Database initialization script
├── env.example          # Environment variables template
├── requirement.txt      # Python dependencies
└── images/              # Uploaded images directory
```

## 🔧 Database Models

### APIKeys
- `id`: Primary key
- `api_key`: Unique API key string
- `created_at`: Creation timestamp
- `expires_at`: Expiration timestamp (1 year from creation)

### PersonDurations
- `id`: Primary key
- `labeled_image`: Image filename
- `nim`: Student ID
- `name`: Person name
- `start_time`: Entry timestamp
- `end_time`: Exit timestamp (nullable)

## 🔐 API Authentication

The API uses Bearer token authentication with API keys:

1. Generate an API key: `POST /generate-api-keys`
2. Use the API key in the Authorization header: `Bearer <api_key>`

## 📝 API Endpoints

- `GET /` - Welcome message
- `POST /generate-api-keys` - Generate new API key
- `POST /person-duration` - Create person duration record
- `PATCH /person-duration/{id}` - Update end time
- `GET /person-durations` - Get all person durations
- `GET /person-duration/{id}` - Get specific person duration
- `GET /person-duration/show-labeled-image/` - Show uploaded image

## 🛠️ Development

### Adding New Models

1. Add the model to `models.py`
2. Create a migration:
   ```bash
   python db_manage.py create-mig "Add new model"
   ```
3. Run the migration:
   ```bash
   python db_manage.py migrate
   ```

### Database Schema Changes

1. Modify the model in `models.py`
2. Generate migration:
   ```bash
   python db_manage.py create-mig "Update schema"
   ```
3. Review the generated migration file in `alembic/versions/`
4. Run the migration:
   ```bash
   python db_manage.py migrate
   ```

## 🐛 Troubleshooting

### Common Issues

1. **Database connection failed**
   - Ensure PostgreSQL container is running: `python db_manage.py start-db`
   - Check environment variables in `.env`

2. **Migration errors**
   - Check if database is accessible
   - Verify model changes are correct
   - Use `python db_manage.py status` to check migration state

3. **Docker issues**
   - Ensure Docker is running
   - Check if port 5432 is available
   - Use `docker-compose logs postgres` to view logs

### Reset Everything

To completely reset the database and start fresh:

```bash
python db_manage.py reset
```

## 📄 License

This project is for educational purposes. 