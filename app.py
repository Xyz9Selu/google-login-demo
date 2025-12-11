from flask import Flask, redirect, request, session
import os
from google_auth_oauthlib.flow import Flow
import json

# Allow insecure transport for localhost development (HTTP instead of HTTPS)
# WARNING: Only use this for local development, never in production!
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# OAuth 2.0 configuration
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']
REDIRECT_URI = 'http://localhost:3000/google-login-redirect'

# OAuth 2.0 flow configuration
CLIENT_CONFIG = {
    "web": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [REDIRECT_URI]
    }
}

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login')
def login():
    if not CLIENT_ID or not CLIENT_SECRET:
        return 'Google OAuth credentials not configured', 500
    
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    session['state'] = state
    return redirect(authorization_url)

@app.route('/google-login-redirect')
def google_login_redirect():
    state = session.get('state')
    
    if not state or state != request.args.get('state'):
        return 'Invalid state parameter', 400
    
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=state
    )
    
    flow.fetch_token(authorization_response=request.url)
    
    from googleapiclient.discovery import build
    service = build('oauth2', 'v2', credentials=flow.credentials)
    user_info = service.userinfo().get().execute()
    
    return f"""<html><head><title>Login Success</title></head><body>
    <script>
        sessionStorage.setItem('google_user', JSON.stringify({json.dumps(user_info)}));
        window.location.href = '/';
    </script>
    </body></html>"""

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(port=3000, debug=True)

