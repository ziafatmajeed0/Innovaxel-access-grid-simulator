# Room configuration with access rules
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

# Employee access request data
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
