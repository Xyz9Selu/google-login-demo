# Google Login Demo

A simple Google OAuth login demo using plain HTML + JavaScript as frontend and Python + Flask as backend.

## Features

- Google OAuth 2.0 authentication
- User profile information display
- Clean, modern UI

## Setup Instructions

### 1. Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API or Google Identity API
4. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
5. Configure the consent screen if prompted
6. Create an OAuth 2.0 Client ID:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:3000/google-login-redirect`
7. Copy the Client ID and Client Secret

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file or export environment variables:

```bash
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export SECRET_KEY="your-secret-key-for-session"
```

Or create a `.env` file:

```
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
SECRET_KEY=your-secret-key-for-session
```

### 5. Run the Application

```bash
python app.py
```

The application will run on `http://localhost:3000`

### 6. Test the Login

1. Open `http://localhost:3000` in your browser
2. Click "Sign in with Google"
3. Authorize the application
4. You should see your user information displayed

## Project Structure

```
google-login-demo/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore         # Git ignore file
├── venv/              # Python virtual environment (created after setup)
└── static/
    └── index.html     # Frontend HTML/JS
```

## How It Works

1. User clicks "Sign in with Google" button
2. Backend redirects to Google OAuth authorization page
3. User authorizes the application
4. Google redirects back to `/google-login-redirect` with authorization code
5. Backend exchanges the code for user information
6. User information is sent to frontend and displayed

## Notes

- The redirect URL is hardcoded as `http://localhost:3000/google-login-redirect`
- User information is stored in browser `sessionStorage` for demo purposes
- In production, you should store user sessions securely on the server side
- Make sure to change the `SECRET_KEY` in production

