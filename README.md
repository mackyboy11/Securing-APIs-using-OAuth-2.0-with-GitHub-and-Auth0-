# Securing APIs using OAuth 2.0 with GitHub and Auth0

System Integration and Architecture

This project is the laboratory activity for implementing OAuth 2.0 login with GitHub, protecting Flask API endpoints with sessions, and documenting Auth0 as an alternative identity provider.

## Objectives

- Explain OAuth 2.0.
- Implement OAuth login using GitHub.
- Secure API endpoints using authenticated sessions.
- Compare GitHub OAuth and Auth0.
- Demonstrate protected API access.

## GitHub OAuth Setup

1. Open GitHub.
2. Go to **Settings** > **Developer settings** > **OAuth Apps**.
3. Click **New OAuth App**.
4. Use these values:
   - Homepage URL: `http://localhost:5000`
   - Authorization callback URL: `http://localhost:5000/callback`
5. Save the app.
6. Copy the generated **Client ID** and **Client Secret**.

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

The application automatically reads a local `.env` file when it starts. Create `.env` with:

```powershell
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
FLASK_SECRET_KEY=replace-this-with-a-random-secret
```

Do not commit `.env` to GitHub. It is already listed in `.gitignore`.

## Run the Application

```bash
python app.py
```

Open:

```text
http://localhost:5000/login
```

## Routes

- `/login` - Login page before authentication.
- `/login/github` - Starts GitHub OAuth authorization.
- `/callback` - Handles GitHub OAuth callback.
- `/profile` - Protected route that returns the authenticated GitHub user data.
- `/api/secure-data` - Bonus protected API route.
- `/logout` - Clears the session and logs out the user.

## Testing Procedure

1. Run the Flask application.
2. Open `http://localhost:5000/login`.
3. Click **Login with GitHub**.
4. Authorize the application on GitHub.
5. Confirm that `/profile` returns user data.
6. Open `/api/secure-data` and confirm protected data is returned.
7. Visit `/logout`.
8. Try opening `/profile` again. It should return `Unauthorized` with status code `401`.

## Auth0 Alternative

Auth0 can be used as an OAuth provider by setting these environment variables:

```powershell
$env:AUTH0_DOMAIN="your-tenant.auth0.com"
$env:AUTH0_CLIENT_ID="your_auth0_client_id"
$env:AUTH0_CLIENT_SECRET="your_auth0_client_secret"
```

The app includes an Auth0 OAuth registration block to show the alternative configuration. The active login flow uses GitHub because the lab requires GitHub screenshots and GitHub OAuth setup.

## Screenshots Required

Place screenshots in the `screenshots` folder:

1. `01-login-page.png` - `/login` before authentication.
2. `02-github-authorization.png` - GitHub permission page.
3. `03-profile-success.png` - `/profile` after successful login.
4. `04-unauthorized-profile.png` - `/profile` without login.
5. `05-logout-result.png` - `/profile` after logout.
6. `06-secure-data.png` - `/api/secure-data` after login.

## Critical Thinking Answers

i. What happens when a user accesses /profile without logging in?
The application blocks the request and returns Unauthorized. This happens because the session does not contain a logged-in user.

ii. What data is returned after successful login?
After successful login, the app returns the user’s GitHub profile data. This includes details like the GitHub username, user ID, display name, avatar URL, and profile link.

iii. Why is OAuth considered more secure than traditional login?
OAuth is more secure because the app does not collect or store the user’s password. Instead, GitHub handles authentication and only sends the app an authorization token.

iv. What challenges did you encounter?
One challenge was setting up the correct callback URL for GitHub OAuth. Another challenge was understanding how the session is used to protect routes like /profile.

v. What did you learn from this activity?
I learned how OAuth 2.0 allows users to log in using a trusted provider like GitHub. I also learned how to protect API routes so only authenticated users can access them.
## Repository Submission Checklist

- `app.py`
- `requirements.txt`
- `README.md`
- `screenshots/` folder
- Completed screenshots
- Bonus route: `/api/secure-data`
