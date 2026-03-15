# Copilot Instructions for Kidney-Renalyze-Personal-Project

The purpose of this document is to give an AI coding assistant the minimum context required to work productively inside this workspace.  This project is a small Flask web application that predicts chronic kidney disease risk and exposes a simple chat interface backed by a Hugging Face inference API.

---

## 🚦 Architecture Overview

- **`app/app.py`** is the entry point.  It defines a single `Flask` instance and all of the routes used by the UX.
  - `GET /`, `/recommendations`, `/details` render templates from `app/templates`.
  - `GET /prediction` renders the prediction form; `POST /prediction` accepts JSON, converts form fields into a feature vector, and returns a probability computed by a pickled `RandomForestClassifier` stored at `app/model/model.pkl`.
  - `POST /chat` takes a JSON body with `message`, builds a prompt using the in‑process `chat_history` list and a fixed instruction, then calls the Hugging Face Inference API (`mistralai/Mistral-7B-Instruct-v0.3`) using the `HF_TOKEN` environment variable.

- **Data flow**
  1. Client-side JavaScript (`static/js/prediction.js` or `static/js/chatbot.js`) gathers user input.
  2. It uses `fetch` to POST a JSON payload to one of the Flask routes.
  3. Python code processes the data and responds with JSON or a rendered HTML template.
  4. Front‑end code updates the DOM based on the response.

- **Front‑end assets** live under `app/static`:
  - `css/*` for styles
  - `js/*` for behaviour
  - `templates/*` for Jinja2 HTML pages.

- **Machine learning assets**
  - `chronic_kidney_disease.csv` is the raw dataset used in `app/train_model.ipynb` to produce `model/model.pkl`.
  - Retraining is done manually in the notebook (no automated pipeline).  The notebook uses `SMOTE` to rebalance classes and a `RandomForestClassifier`.

- **Configuration**
  - `.env` (not checked in) should contain `HF_TOKEN` for the chat feature.  The app loads environment variables via `python-dotenv`.


## 🛠 Developer Workflows

1. **Install dependencies**
   ```powershell
   python -m pip install -r requirements.txt
   ```
   The `requirements.txt` includes many data‑science packages; only a subset are used at runtime.

2. **Run the server locally**
   ```powershell
   set HF_TOKEN=<your‑token>          # or use a .env file
   python app/app.py
   ```
   or
   ```powershell
   flask --app app.app run --debug
   ```
   Default host/port: `127.0.0.1:5000`.

3. **Exercise endpoints**
   - Open a browser and visit `/` for the home page.
   - Use the form on `/prediction` to send a request; the front end will POST JSON matching the keys used in `prediction.js` (age, BMIBaseline, sex, etc.).
   - The chat widget sends `POST /chat` with `{ "message": "..." }`; the JavaScript currently points at `http://127.0.0.1:5000/chat` which must match the running server, otherwise update it.

4. **Retrain the model**
   - Open `app/train_model.ipynb` in Jupyter and run the cells.  After training, pickle the model to `app/model/model.pkl` (the notebook already includes code to do this).

5. **Debugging tips**
   - Server logs will show the `print` debug lines in `app.py`.  Errors in prediction are returned as JSON with a 500 status.
   - Chat history is kept in a global list; restarting the server clears it.
   - The prediction route coerces missing JSON fields to zero; front‑end validation is very light.


## ⚙ Project-Specific Patterns

- **Feature mapping**: `sex` is converted to `1` for `'male'` and `0` otherwise.  Boolean fields from the form (`HistoryDiabetes`, `HistoryCHD`) are mapped to `1` or `0` in both `prediction.js` and `app.py` with the same names (`diabetes`, `chd`).  Keep these in sync when modifying the form or model features.

- **Error handling**: most failures are logged with `print` and return a generic JSON error.  There are no custom exception types.

- **Static URLs**: the chat widget uses an explicit `http://127.0.0.1:5000` base URL; if the server runs behind a reverse proxy or on a different host, adjust `chatbot.js` accordingly or switch to a relative URL.

- **No tests**: there is currently no automated test suite.  Unit tests for the prediction logic or chat prompt construction would be new work.

- **No CI/CD config**: repository lacks GitHub Actions or other build scripts.  If you add workflows, focus on installing requirements and running a smoke check against the Flask server.


## 🔌 Integration Points & External Dependencies

- **Hugging Face Inference API**: used for the chat feature.  The request payload is built in `query_model()` and hard‑codes `max_new_tokens`, `temperature`, and a stop sequence.  Environment variable `HF_TOKEN` must be available.

- **Pickle file**: untrusted pickle loading is normally dangerous; this repo trusts `model.pkl` because it is generated locally.  When modifying the training notebook, ensure the new model is compatible with the input feature order expected in `app.py`.


## 📁 Key Files to Reference

| Path | Role |
|------|------|
| `app/app.py` | Flask routes and prediction/chat logic |
| `app/train_model.ipynb` | Jupyter notebook used to clean data and produce `model.pkl` |
| `app/static/js/prediction.js` | Front‑end code that submits health form data |
| `app/static/js/chatbot.js` | Front‑end chat widget logic |
| `app/templates/*.html` | HTML views for the site |
| `app/model/model.pkl` | Serialized ML model used at runtime |


---

### ✅ What an AI assistant should do when editing the project

- Stay within the Flask application structure; add new code to `app/app.py` or `static/*` as appropriate.
- When adding new fields to the prediction form, update both JavaScript and backend mapping to ensure the JSON keys match.
- Respect the use of environment variables for secrets (HF_TOKEN) and avoid checking them into source control.
- Be cautious about modifying the chat prompt format or history handling – tests are not present, so manual verification is required.

### ❓ Asking for clarification

If any part of the request seems ambiguous (e.g. a new feature that touches frontend routing or model input), the assistant should prompt the user with follow‑up questions describing the current behavior and seeking confirmation on desired changes.

---

*Feel free to suggest updates to this file if the codebase changes.*
