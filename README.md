# Die Control System

A comprehensive system for managing dies, workers, and maintenance in a manufacturing environment.

## Features

- **User Management**: Create and manage users with role-based access control
- **Worker Management**: Track workers and their positions
- **Role Management**: Define and assign roles to users
- **Position Management**: Manage worker positions and assignments

## Technical Stack

- Python 3.x
- PyQt5 for GUI
- MySQL for database
- bcrypt for password hashing

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the database:
- Create a MySQL database
- Update the connection settings in `src/database/connection.py`

5. Run the application:
```bash
python src/main.py
```

## Project Structure

```
DieControlSystem/
├── assets/              # Images and icons
├── src/
│   ├── database/       # Database connection and schema
│   ├── models/         # Data models
│   ├── views/          # GUI windows and dialogs
│   └── main.py         # Application entry point
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Contributing

1. Create a feature branch
2. Commit your changes
3. Push to the branch
4. Create a Pull Request

## License

This project is proprietary and confidential. 