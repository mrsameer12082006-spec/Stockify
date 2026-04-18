# Stockify - Getting Started Guide

Welcome to **Stockify**! This is a smart inventory management system built with Streamlit. Follow this guide to get the app running on your computer.

---

## Prerequisites

Before running Stockify, make sure you have:

- ✅ **Python 3.8 or higher** installed ([Download Python](https://www.python.org/downloads/))
- ✅ **pip** (Python package manager - comes with Python)
- ✅ **Git** (optional, for cloning the repository)

### Check if Python is installed:
```bash
python --version
```

If you see a version number (e.g., `Python 3.13.0`), you're ready to go!

---

## Installation Steps

### Step 1: Navigate to the Project Folder

Open your terminal/command prompt and go to the Stockify folder:

```bash
cd path/to/Kaam
```

**Example on Windows:**
```bash
cd C:\Users\YourUsername\OneDrive\Documents\GitHub\Kaam
```

**Example on Mac/Linux:**
```bash
cd ~/Documents/GitHub/Kaam
```

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment keeps dependencies isolated from your system Python:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line when activated.

### Step 3: Install Dependencies

Install all required Python packages:

```bash
pip install -r frontend/requirements.txt
```

Or manually install the key packages:

```bash
pip install streamlit==1.45.1 pandas==2.2.3 plotly==11.2.0 openpyxl
```

**Wait for the installation to complete** (this may take a few minutes).

---

## Running the Application

### Start the Streamlit Server

From the project root folder (`Kaam`), run:

```bash
streamlit run frontend/app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.xxx.x.x:8501
```

### Open in Browser

- Automatically opens at: `http://localhost:8501`
- Or manually open your browser and go to: **http://localhost:8501**

---

## Login to Stockify

When the app loads, you'll see the login page.

**Use these test credentials:**
```
Email: admin
Password: admin
```

Click **🚀 Sign In** to proceed.

---

## What You Can Do in Stockify

Once logged in, you'll see a navigation bar with these options:

| Button | Feature | What It Does |
|--------|---------|--------------|
| 🏠 Home | Dashboard Welcome | Overview and quick stats |
| 📂 Upload | CSV Upload | Upload inventory & sales CSV files |
| 💳 POS | Point of Sale | Scan products & ring up sales in real-time |
| 📊 Overview | Dashboard | View KPIs and summary metrics |
| 📦 Products | Product Catalog | Browse all products in inventory |
| 📈 Trends | Trends Analysis | See sales trends over time |
| 💡 Insights | Recommendations | Get smart stock & ordering recommendations |
| 🚨 Alerts | Stock Alerts | View low-stock and reorder alerts |
| 📉 Charts | Visualizations | Interactive charts and graphs |

---

## Quick Start Workflow

### Option A: Using CSV Upload

1. **Prepare CSV files:**
   - Inventory file: `sample_inventory.csv` (in `Ingestion/` folder)
   - Sales file: `sample_sales.csv` (in `Ingestion/` folder)

2. **Upload to Stockify:**
   - Click **📂 Upload**
   - Upload both CSV files
   - Watch the dashboard update automatically

3. **View Analytics:**
   - Click **📊 Overview** to see KPIs
   - Click **📈 Trends** to see sales trends
   - Click **💡 Insights** for recommendations

### Option B: Using POS (Point of Sale)

1. **Go to POS:**
   - Click **💳 POS** button

2. **Add Products:**
   - Enter product code (e.g., `P001`)
   - Enter quantity
   - Click **Lookup Product**

3. **Manage Cart:**
   - Click **Add to cart**
   - Browse cart section
   - Click **Confirm sale** when done

4. **Check Dashboard:**
   - Sales automatically appear in analytics
   - Inventory updates in real-time

---

## File Uploads

### Sample CSV Format

**Inventory CSV** (`inventory.csv`):
```
sku,name,category,price,stock,reorder_point
P001,Laptop,Electronics,1200.00,5,10
P002,Mouse,Electronics,25.00,50,20
P003,Desk Chair,Furniture,300.00,3,5
```

**Sales CSV** (`sales.csv`):
```
date,sku,quantity,price,total
2026-04-10,P001,1,1200.00,1200.00
2026-04-10,P002,2,25.00,50.00
2026-04-11,P003,1,300.00,300.00
```

Sample files are provided in the `Ingestion/` folder.

---

## Troubleshooting

### Issue: "Command not found: streamlit"
**Solution:** Make sure you've:
1. Activated the virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
2. Installed requirements: `pip install -r frontend/requirements.txt`

### Issue: "Port 8501 already in use"
**Solution:** Streamlit is running on another port. Either:
- Close other Streamlit instances
- Or run with a different port:
```bash
streamlit run frontend/app.py --server.port 8502
```

### Issue: "Module not found" error
**Solution:** Install missing packages:
```bash
pip install pandas streamlit plotly openpyxl
```

### Issue: Blank page or POS not loading
**Solution:** 
1. Try refreshing the browser (Ctrl+R or Cmd+R)
2. Check the terminal for error messages
3. Look at the debug expander for detailed error info

### Issue: Can't access app from another computer
**Streamlit loads on localhost by default.** To make it accessible:

```bash
streamlit run frontend/app.py --server.address 0.0.0.0
```

Then access from other computers using your IP address shown in the output.

---

## Stopping the Application

To stop the Streamlit server:

1. **Press `Ctrl+C`** in the terminal (or `Cmd+C` on Mac)
2. You'll see: `Stopping...`

To deactivate the virtual environment:
```bash
deactivate
```

---

## Project Structure

**Key folders inside Stockify:**

```
Kaam/
├── frontend/              # Streamlit UI pages
│   ├── app.py            # Main entry point
│   ├── upload.py         # CSV upload interface
│   ├── dashboard.py      # KPI dashboard
│   └── ...
├── pos/                   # Point of Sale system
│   ├── pos_page.py       # POS interface
│   ├── cart.py           # Shopping cart
│   ├── database.py       # POS database
│   └── ...
├── analytics/            # Data analysis
│   ├── trends.py         # Trend analysis
│   ├── insights.py       # Recommendations
│   └── ...
├── Ingestion/            # Data import
│   ├── sample_inventory.csv
│   ├── sample_sales.csv
│   └── ...
└── data/                 # Processed data storage
    └── processed/        # Clean data files
```

---

## Next Steps

1. ✅ Run the app: `streamlit run frontend/app.py`
2. ✅ Login with `admin` / `admin`
3. ✅ Upload sample CSV files or test the POS
4. ✅ Explore the different pages and features
5. ✅ Check the recommendations for your inventory

---

## Need Help?

- **Check error messages** in the terminal where Streamlit is running
- **Look at debug details** - many pages have expandable error information
- **Review log files** - Streamlit creates detailed logs for troubleshooting
- **Check the repo documentation** - See `README.md` and other `.md` files for more info

---

## Keyboard Shortcuts in Terminal

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Stop the Streamlit server |
| `Ctrl+L` | Clear terminal screen |
| `Ctrl+A` | Select all text |
| `Ctrl+V` | Paste text |

---

**Enjoy using Stockify! Happy inventory management!** 📦

Last Updated: April 13, 2026
