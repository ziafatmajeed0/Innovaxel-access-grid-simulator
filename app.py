from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Room configuration with rules
ROOM_RULES = {
    "ServerRoom": {
        "min_access_level": 2,
        "open_time": "09:00",
        "close_time": "11:00",
        "cooldown_minutes": 15
    },
    "Vault": {
        "min_access_level": 3,
        "open_time": "09:00",
        "close_time": "10:00",
        "cooldown_minutes": 30
    },
    "R&D Lab": {
        "min_access_level": 1,
        "open_time": "08:00",
        "close_time": "12:00",
        "cooldown_minutes": 10
    }
}

# Employee data
EMPLOYEE_DATA = [
    {"id": "EMP001", "access_level": 2, "request_time": "09:15", "room": "ServerRoom"},
    {"id": "EMP002", "access_level": 1, "request_time": "09:30", "room": "Vault"},
    {"id": "EMP003", "access_level": 3, "request_time": "10:05", "room": "ServerRoom"},
    {"id": "EMP004", "access_level": 3, "request_time": "09:45", "room": "Vault"},
    {"id": "EMP005", "access_level": 2, "request_time": "08:50", "room": "R&D Lab"},
    {"id": "EMP006", "access_level": 1, "request_time": "10:10", "room": "R&D Lab"},
    {"id": "EMP007", "access_level": 2, "request_time": "10:18", "room": "ServerRoom"},
    {"id": "EMP008", "access_level": 3, "request_time": "09:55", "room": "Vault"},
    {"id": "EMP001", "access_level": 2, "request_time": "09:28", "room": "ServerRoom"},
    {"id": "EMP006", "access_level": 1, "request_time": "10:15", "room": "R&D Lab"}
]

# Track access history for cooldown management
access_history = []

def time_to_minutes(time_str):
    """Convert time string (HH:MM) to minutes since midnight"""
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def check_access_permission(employee, room_rules):
    """Check if employee can access the requested room"""
    room = employee['room']
    
    if room not in room_rules:
        return False, f"Room '{room}' does not exist"
    
    rules = room_rules[room]
    request_time_minutes = time_to_minutes(employee['request_time'])
    open_time_minutes = time_to_minutes(rules['open_time'])
    close_time_minutes = time_to_minutes(rules['close_time'])
    
    # Check access level
    if employee['access_level'] < rules['min_access_level']:
        return False, f"Denied: Access level {employee['access_level']} below required level {rules['min_access_level']}"
    
    # Check if room is open
    if not (open_time_minutes <= request_time_minutes <= close_time_minutes):
        return False, f"Denied: Room closed at {employee['request_time']} (Open: {rules['open_time']}-{rules['close_time']})"
    
    # Check cooldown period
    cooldown_minutes = rules['cooldown_minutes']
    current_request_time = request_time_minutes
    
    for access in access_history:
        if (access['employee_id'] == employee['id'] and 
            access['room'] == room and
            abs(current_request_time - access['request_time_minutes']) < cooldown_minutes):
            return False, f"Denied: Cooldown period active (must wait {cooldown_minutes} minutes between accesses)"
    
    return True, f"Access granted to {room}"

def simulate_access(employees):
    """Simulate access for all employees and return results"""
    global access_history
    access_history = []  # Reset history for each simulation
    results = []
    
    # Sort employees by request time to process in chronological order
    sorted_employees = sorted(employees, key=lambda x: time_to_minutes(x['request_time']))
    
    for employee in sorted_employees:
        granted, reason = check_access_permission(employee, ROOM_RULES)
        
        result = {
            'employee_id': employee['id'],
            'room': employee['room'],
            'request_time': employee['request_time'],
            'access_level': employee['access_level'],
            'status': 'Granted' if granted else 'Denied',
            'reason': reason
        }
        
        results.append(result)
        
        # If access is granted, add to history for cooldown tracking
        if granted:
            access_history.append({
                'employee_id': employee['id'],
                'room': employee['room'],
                'request_time_minutes': time_to_minutes(employee['request_time'])
            })
    
    return results

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', employees=EMPLOYEE_DATA, room_rules=ROOM_RULES)

@app.route('/simulate', methods=['POST'])
def simulate():
    """API endpoint to simulate access for all employees"""
    try:
        # Use the predefined employee data
        results = simulate_access(EMPLOYEE_DATA)
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/employees')
def get_employees():
    """API endpoint to get employee data"""
    return jsonify(EMPLOYEE_DATA)

@app.route('/api/rooms')
def get_rooms():
    """API endpoint to get room rules"""
    return jsonify(ROOM_RULES)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
