# Hotel Scraper - Technical Test

Web application for scraping hotel data from Booking.com with a React frontend and Django REST API backend.

## Quick Start

### Local Development

1. **Clone and run with Docker:**
   ```bash
   git clone <repository>
   cd athlos-technical-test
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000
   - Swagger Documentation: http://localhost:8000/api/schema/swagger-ui/

## Architecture

- **Frontend:** React.js with modern hooks and CSS
- **Backend:** Django REST Framework with Selenium web scraping
- **Database:** SQLite
- **Containerization:** Docker with multi-stage builds

## API Endpoints

### Hotels
- `GET /api/v1/hotels/` - List all saved hotels
- `POST /api/v1/hotels/` - Create a new hotel
- `GET /api/v1/hotels/{id}/` - Get hotel by ID
- `DELETE /api/v1/hotels/{id}/` - Delete hotel by ID

### Scraping
- `GET /api/v1/hotels/scrape/?name={hotel_name}` - Scrape hotel data from Booking.com

## Response Format

All endpoints return standardized JSON responses:
```json
{
  "ok": true,
  "data": {...},
  "msg": "Success message",
  "count": 10
}
```

## Features

- Search hotels on Booking.com by name
- Extract hotel details (name, location, price, rating, amenities, photos)
- Save hotels to database
- View saved hotels with image gallery
- Delete saved hotels
- Responsive design
- Error handling and validation

## Technology Stack

**Backend:**
- Django 4.2
- Django REST Framework
- Selenium WebDriver
- BeautifulSoup
- PostgreSQL/SQLite

**Frontend:**
- React 18
- Modern React Hooks
- CSS3 with Grid/Flexbox
- Fetch API

**DevOps:**
- Docker & Docker Compose
- Multi-stage builds
- Static file serving with Nginx