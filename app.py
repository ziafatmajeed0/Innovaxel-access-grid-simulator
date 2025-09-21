from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
from data import ROOM_RULES, EMPLOYEE_DATA

app = Flask(__name__)
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

@app.route('/api/simulate-single', methods=['POST'])
def simulate_single():
    """API endpoint to simulate access for a single employee"""
    try:
        data = request.get_json()
        employee = data.get('employee')
        
        if not employee:
            return jsonify({
                'success': False,
                'error': 'Employee data is required'
            }), 400
        
        # Reset access history for single simulation
        global access_history
        access_history = []
        
        granted, reason = check_access_permission(employee, ROOM_RULES)
        
        result = {
            'employee_id': employee['id'],
            'room': employee['room'],
            'request_time': employee['request_time'],
            'access_level': employee['access_level'],
            'status': 'Granted' if granted else 'Denied',
            'reason': reason
        }
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Access Grid Simulator...")
    print("📍 Server running at: http://localhost:5000")
    print("🔒 Ready to simulate employee access control!")
    app.run(debug=True, port=5000)
