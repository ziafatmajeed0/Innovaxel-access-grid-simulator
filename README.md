# Access Grid - Employee Access Simulator

A time-based employee access control system for secure rooms in a building. This application simulates employee access requests based on access levels, time windows, and cooldown periods.

## Features

- **Room Access Rules**: Each room has specific access level requirements, operating hours, and cooldown periods
- **Employee Management**: Load and process employee access requests with detailed results
- **Real-time Simulation**: Click "Simulate Access" to process all requests and see detailed results
- **Visual Interface**: Clean, professional UI with color-coded results and statistics

## Room Configuration

| Room | Min Access Level | Operating Hours | Cooldown Period |
|------|------------------|-----------------|-----------------|
| ServerRoom | 2 | 09:00 - 11:00 | 15 minutes |
| Vault | 3 | 09:00 - 10:00 | 30 minutes |
| R&D Lab | 1 | 08:00 - 12:00 | 10 minutes |

## Access Rules

An employee can access a room only if:
1. Their access level is greater than or equal to the room requirement
2. The room is open at the request time
3. They have not accessed the same room within the cooldown period

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ziafatmajeed0/Innovaxel-access-grid-simulator.git
cd Innovaxel-access-grid-simulator
```

2. Switch to the dev branch:
```bash
git checkout dev
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **View Room Rules**: See the access requirements for each room
2. **Review Employee Requests**: Check the list of employee access requests
3. **Run Simulation**: Click "Simulate Access" to process all requests
4. **View Results**: See detailed results with grant/deny status and reasons
5. **Check Statistics**: View summary statistics of the simulation

## API Endpoints

- `GET /` - Main application interface
- `POST /simulate` - Run access simulation
- `GET /api/employees` - Get employee data
- `GET /api/rooms` - Get room rules

## Employee Data Format

```json
{
  "id": "EMP001",
  "access_level": 2,
  "request_time": "09:15",
  "room": "ServerRoom"
}
```

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with gradient design
- **Data**: JSON-based configuration

## Project Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Frontend interface
└── README.md          # This file
```

## Development

The application is built with Flask and uses a simple in-memory data structure for tracking access history and cooldown periods. The simulation processes requests in chronological order to properly handle cooldown logic.

## License

This project is created as a take-home assessment for Innovaxel.
