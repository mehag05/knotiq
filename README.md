# Knot Data Demo

## Setup Instructions

### Backend Setup
1. Create and activate a Python virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask backend server:
```bash
python3 api.py
```

### Frontend Setup
1. Navigate to the client directory:
```bash
cd client
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the React frontend:
```bash
npm run start
```

### Modal Server Setup
1. Install Modal (if not already installed):
```bash
pip install modal
```

2. Run the Modal server:
```bash
modal serve text_to_image.py
```

## Running the Project
Make sure all three components are running:
1. Flask Backend (port 5001)
2. React Frontend (port 3000)
3. Modal Server

The application will be available at http://localhost:3000

## Troubleshooting
- If you see connection errors, ensure all three servers are running
- Check that ports 3000 and 5001 are available
- Make sure you're using the virtual environment when running Python commands

## Additional Comments
There are some unneccesary files in the repository, such as the `mock.py` file, which is a mock transaction generator. Please ignore, we had lots of iterations!