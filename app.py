import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, jsonify, redirect, render_template_string, session, url_for


def load_local_env(path=".env"):
    if not os.path.exists(path):
        return

    with open(path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_local_env()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

oauth = OAuth(app)

github = oauth.register(
    name="github",
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

auth0_domain = os.environ.get("AUTH0_DOMAIN")
auth0 = None
if auth0_domain:
    auth0 = oauth.register(
        name="auth0",
        client_id=os.environ.get("AUTH0_CLIENT_ID"),
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
        api_base_url=f"https://{auth0_domain}",
        access_token_url=f"https://{auth0_domain}/oauth/token",
        authorize_url=f"https://{auth0_domain}/authorize",
        client_kwargs={"scope": "openid profile email"},
    )


LOGIN_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OAuth 2.0 API Security Lab</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 760px;
      margin: 48px auto;
      padding: 0 20px;
      color: #1f2937;
      line-height: 1.5;
    }
    .panel {
      border: 1px solid #d1d5db;
      border-radius: 8px;
      padding: 24px;
      background: #f9fafb;
    }
    a.button {
      display: inline-block;
      padding: 10px 14px;
      background: #24292f;
      color: #fff;
      text-decoration: none;
      border-radius: 6px;
      font-weight: 700;
    }
    code {
      background: #e5e7eb;
      padding: 2px 5px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="panel">
    <h1>Securing APIs using OAuth 2.0</h1>
    <p>This page starts GitHub OAuth authentication for the protected API lab.</p>
    <p><a class="button" href="{{ url_for('github_login') }}">Login with GitHub</a></p>
    <p>After logging in, visit <code>/profile</code> or <code>/api/secure-data</code>.</p>
  </div>
</body>
</html>
"""


@app.route("/")
@app.route("/login")
def login():
    return render_template_string(LOGIN_PAGE)


@app.route("/login/github")
def github_login():
    if not os.environ.get("GITHUB_CLIENT_ID") or not os.environ.get("GITHUB_CLIENT_SECRET"):
        return (
            "Missing GitHub OAuth credentials. Set GITHUB_CLIENT_ID and "
            "GITHUB_CLIENT_SECRET, then restart the app.",
            500,
        )

    redirect_uri = url_for("callback", _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route("/callback")
def callback():
    token = github.authorize_access_token()
    user = github.get("user").json()

    session["user"] = {
        "id": user.get("id"),
        "login": user.get("login"),
        "name": user.get("name"),
        "avatar_url": user.get("avatar_url"),
        "profile_url": user.get("html_url"),
    }
    session["github_token"] = token
    return redirect("/profile")


@app.route("/profile")
def profile():
    if "user" not in session:
        return "Unauthorized", 401

    return jsonify(
        {
            "message": "Successfully logged in with GitHub OAuth.",
            "user": session["user"],
        }
    )


@app.route("/api/secure-data")
def secure_data():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(
        {
            "message": "This protected API data is only available to authenticated users.",
            "authenticated_user": session["user"]["login"],
            "data": {
                "course": "System Integration and Architecture",
                "activity": "Securing APIs using OAuth 2.0 with GitHub and Auth0",
            },
        }
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("github_token", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
