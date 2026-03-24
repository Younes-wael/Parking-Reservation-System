# Parking Reservation System

A comprehensive parking reservation management system built for the Mercure Hotel Frankfurt Airport Langen. This Streamlit-based application provides an intuitive interface for managing hotel parking reservations, tracking occupancy, and monitoring availability.

## Features

- **Dashboard Overview**: Real-time KPIs including total parking spots, current reservations, peak occupancy, and availability metrics
- **Reservation Management**: View, search, and manage existing parking reservations
- **New Reservation Creation**: Add new parking reservations with validation and conflict checking
- **Availability Tracking**: Detailed availability calendar with occupancy charts and tables
- **Manager Configuration**: Administrative tools for system configuration and data management
- **Data Sources**: Support for both SQLite database (production) and JSON mock data (development/testing)
- **Responsive UI**: Clean, modern interface built with Streamlit

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.x
- **Database**: SQLite
- **Data Processing**: Pandas
- **Mock Data**: JSON (optional)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download the project files to your local machine

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. Install required dependencies:
   ```bash
   pip install streamlit pandas
   ```

## Usage

### Local Installation

1. Ensure you're in the project directory and virtual environment is activated

2. Run the application:
   ```bash
   streamlit run interface.py
   ```

3. Open your web browser to the URL displayed in the terminal (typically `http://localhost:8501`)

4. Use the sidebar navigation to access different sections:
   - **Home**: Dashboard with occupancy overview and KPIs
   - **Reservations**: View and manage existing reservations
   - **New Reservation**: Create new parking reservations
   - **Availability**: Check parking availability for specific date ranges
   - **Manager Config**: Administrative configuration options

### Online Deployment (Streamlit Cloud)

Deploy your app online for free using Streamlit Cloud:

1. **Connect your GitHub Repository**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Click "New app"
   - Connect your GitHub account
   - Select this repository: `Younes-wael/Parking-Reservation-System`
   - Set the main file to `interface.py`

2. **Deploy**:
   - Click "Deploy"
   - Streamlit Cloud will automatically detect and install dependencies from `requirements.txt`
   - Your app will be live at: `https://[your-username]-parking-reservation-system.streamlit.app`

3. **Share the Link**:
   - The deployment URL is accessible from anywhere
   - Share it with team members or hotel staff
   - No installation required - just open the link in a browser

**Live Demo**: Once deployed, your application will be accessible online 24/7 with automatic updates whenever you push to the GitHub repository.

### Local Hotel Server Deployment (No Internet Required)

Deploy this application on your hotel's internal server for operation without internet access:

#### Server Setup

1. **Install Python** on the hotel server (Python 3.8+)

2. **Clone or download the project** to the server:
   ```bash
   git clone https://github.com/Younes-wael/Parking-Reservation-System.git
   cd Parking-Reservation-System
   ```

3. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run on the hotel network**:
   ```bash
   streamlit run interface.py --server.address 0.0.0.0 --server.port 8501
   ```

#### Accessing the Application

**From Hotel Staff Computers**:
- Get the server's local IP address (e.g., `192.168.1.100`)
- Open browser and navigate to: `http://192.168.1.100:8501`
- No internet connection needed
- Accessible only within hotel network (more secure)

#### Advantages of Local Deployment

- ✅ **No Internet Required**: Operates completely offline once installed
- ✅ **Data Security**: All reservation data stays on hotel servers
- ✅ **Full Control**: Hotel maintains complete control over the system
- ✅ **Instant Access**: No network latency, fast response times
- ✅ **Cost Effective**: One-time installation, no subscription fees
- ✅ **Privacy**: No data goes to external cloud services

#### Persistence & Backups

- SQLite database (`parking_reservations.db`) stores all data locally
- Regularly backup the database file for disaster recovery
- Easy to migrate to another server by copying project folder

## Configuration

The system can be configured through the sidebar settings:

- **Data Source**: Choose between SQLite (real data) or JSON (mock data for testing)
- **Total Parking Spots**: Set the default parking capacity (default: 60 spots)

Configuration constants are defined in `configuration.py`:
- Hotel name
- Database file path
- JSON mock data file path
- Default parking capacity

## Data Structure

### SQLite Database
The system uses a SQLite database (`parking_reservations.db`) with the following structure:
- `reservations` table containing reservation details
- Automatic database initialization on first run

### JSON Mock Data
Sample data is provided in `data.json` for testing and development purposes.

## Project Structure

```
├── interface.py              # Main application entry point
├── Home_Page.py              # Dashboard and home page logic
├── reservation_Page.py       # Reservation listing and management
├── new_reservation.py        # New reservation creation
├── Manager_config_Page.py    # Administrative configuration
├── db_verwaltung.py          # Database operations and utilities
├── helpers.py                # Helper functions and utilities
├── configuration.py          # Application configuration constants
├── data.json                 # Mock data for testing
├── parking_reservations.db   # SQLite database (created automatically)
├── __init__.py               # Package initialization
└── __pycache__/              # Python bytecode cache
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is proprietary software for Mercure Hotel Frankfurt Airport Langen.

## Support

For technical support or questions, please contact the development team.</content>
<parameter name="filePath">c:\Users\youne\OneDrive\Desktop\Personal\Project\README.md