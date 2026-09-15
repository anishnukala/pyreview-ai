import os
import time
from html import escape

import markdown
from dotenv import load_dotenv
from flask import Flask, render_template, request
from google import genai


load_dotenv()

app = Flask(__name__, template_folder="web_pages")


def format_error_message(error):
    error_text = str(error)
    if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
        return (
            "<p><strong>Gemini quota was exceeded.</strong></p>"
            "<p>Your app is working, but Google rejected the request because this "
            "API key/project has no remaining quota for the selected model. Try "
            "again later, choose a different model with <code>GEMINI_MODEL</code> "
            "in your <code>.env</code> file, or check the quota for this key in "
            "Google AI Studio.</p>"
        )

    if "UNAVAILABLE" in error_text or "503" in error_text:
        return (
            "<p><strong>Gemini is busy right now.</strong></p>"
            "<p>The app is working, but Google says the selected model is "
            "temporarily overloaded. Please try again in a minute, or set "
            "<code>GEMINI_MODEL=gemini-2.5-flash-lite</code> in your "
            "<code>.env</code> file for a lighter fallback model.</p>"
        )

    return (
        "<p><strong>Unable to generate feedback right now.</strong></p>"
        f"<p>{escape(error_text)}</p>"
    )


def get_model_choices():
    configured_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    fallback_models = os.getenv("GEMINI_FALLBACK_MODELS", "gemini-2.5-flash-lite")
    models = [configured_model]

    for model in fallback_models.split(","):
        model = model.strip()
        if model and model not in models:
            models.append(model)

    return models


def generate_feedback(client, prompt):
    last_error = None

    for model in get_model_choices():
        for attempt in range(2):
            try:
                return client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
            except Exception as error:
                last_error = error
                error_text = str(error)
                is_temporary = "UNAVAILABLE" in error_text or "503" in error_text
                if is_temporary and attempt == 0:
                    time.sleep(1)
                    continue
                break

    raise last_error


def review_python_code(code):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "<p>Missing GEMINI_API_KEY. Add it to your .env file and try again.</p>"

    prompt = f"""
You are a beginner-friendly Python code reviewer.

Review this Python code:

```python
{code}
```

Give feedback in clear sections:
- What the code does
- Possible errors or bugs
- Readability improvements
- A beginner-friendly improved version, if helpful
    """

    client = genai.Client(api_key=api_key)
    gemini_response = generate_feedback(client, prompt)

    return markdown.markdown(
        gemini_response.text or "No feedback was returned.",
        extensions=["fenced_code"],
    )


@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.form.get("code", "")

        if not user_input.strip():
            response = "<p>Please enter some Python code.</p>"
        else:
            try:
                response = review_python_code(user_input)
            except Exception as error:
                response = format_error_message(error)

    return render_template(
        "index.html",
        response=response,
        user_input=user_input,
    )


if __name__ == "__main__":
    app.run(debug=True)
