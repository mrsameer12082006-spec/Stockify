# Stockify

Stockify is a Streamlit-based smart inventory management and analytics application. It combines data ingestion, cleaning, analytics, stock alerts, visual dashboards, and a point-of-sale experience into one project.

## What it does

- Upload and clean inventory/sales files
- Run analytics on inventory and sales data
- Show KPIs, trends, insights, and stock alerts
- Provide a POS page for real-time sales flow
- Present a modern Streamlit UI with separate pages for different workflows

## Main features

- **Authentication UI** with Sign In / Sign Up flow
- **Landing page** and guided app navigation
- **Data upload** for inventory and sales files
- **Analytics dashboard** with KPIs and trends
- **Product and category visualizations**
- **Stock alerts** and decision support recommendations
- **POS module** for point-of-sale actions

## Tech stack

- **Python**
- **Streamlit**
- **Pandas**
- **Plotly**
- **OpenPyXL** for Excel file support

## Project structure

- `frontend/` — Streamlit pages and app UI
- `analytics/` — demand, trend, KPI, and runner logic
- `decision_support/` — stock alerts and recommendation rules
- `visualization/` — charts and visualization pages
- `pos/` — point-of-sale features
- `Ingestion/` — data ingestion, cleaning, validation, and sample files
- `data/processed/` — cleaned datasets used by analytics
- `utils/` — shared helpers and constants

## Getting started

### 1) Create and activate the virtual environment

On Windows:

```bash
.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
streamlit run frontend/app.py
```

Then open the local URL shown in the terminal, usually:

- `http://localhost:8501`

## Login

Use the default demo credentials on the sign-in page:

- **Username:** `admin`
- **Password:** `admin`

## How to use

1. Open the app
2. Sign in
3. Navigate through the pages in the sidebar/top navigation
4. Upload inventory or sales files in the Upload page
5. View dashboards, trends, insights, alerts, charts, and POS features

## Sample data

Sample ingestion files are available in the `Ingestion/` folder.

## Notes

- The project currently uses `Ingestion/` with a capital **I** in the workspace.
- If you are working on Windows, keep folder casing consistent when importing modules.
- The app is designed to run locally through Streamlit.

## Troubleshooting

### Streamlit does not start

- Make sure the virtual environment is activated
- Reinstall packages with `pip install -r requirements.txt`
- Confirm Python and Streamlit are available in the environment

### Import errors

- Check that you are running from the project root
- Verify the `Ingestion/` and `frontend/` paths exist
- Keep folder casing consistent on case-sensitive systems

### Blank page or missing data

- Refresh the browser
- Check the terminal for errors
- Upload valid inventory and sales files first

## Quick links

- Main app: `frontend/app.py`
- Upload page: `frontend/upload.py`
- Analytics runner: `analytics/analytics_runner.py`
- Visualizations: `visualization/visualizations.py`
- POS page: `pos/pos_page.py`

---

Happy inventory managing 📦
