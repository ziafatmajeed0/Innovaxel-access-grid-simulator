# Access Grid Simulator

This project is an employee access simulator for secure rooms in a building. It uses a Python/Flask backend to process access logic and a simple HTML/JavaScript frontend to display the simulation.

## Setup and Run

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd access-grid-simulator
    ```

2.  **Switch to the development branch:**
    The application code is on the `dev` branch.
    ```bash
    git checkout dev
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4.  **Install dependencies:**
    ```bash
    pip install Flask
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```

6.  **View in browser:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

## How it Works

- The frontend displays a static list of employee access requests.
- Clicking "Simulate Access" sends this list to the backend API (`/simulate`).
- The backend sorts the requests by time and processes each one against a set of room rules (access level, open hours, cooldown periods).
- The results are sent back to the frontend and displayed in a results table.
