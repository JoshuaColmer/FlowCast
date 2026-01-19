# FlowCast Report Generator 📊

A simple tool to automatically generate beautiful financial charts from your Xero exports.

![FlowCast Demo](demo.png)

## What it does

Upload your Xero Profit & Loss export and instantly get:
- **Operating Profit Chart** - Monthly bar chart showing profit vs costs
- **Admin Costs Breakdown** - Pie chart of your administrative expenses  
- **Books & Balances** - Area chart showing turnover, gross profit and net profit
- **Trend Analysis** - Cumulative trend chart with R² projections

Plus an Excel report with all your data organised and ready to share.

---

## 🚀 Quick Start (5 minutes)

### Step 1: Install Python (one-time setup)

**Windows:**
1. Go to [python.org/downloads](https://python.org/downloads)
2. Download Python 3.11 or later
3. Run the installer
4. ⚠️ **IMPORTANT:** Tick "Add Python to PATH" during installation

**Mac:**
1. Open Terminal
2. Run: `brew install python` (if you have Homebrew)
3. Or download from [python.org/downloads](https://python.org/downloads)

### Step 2: Run FlowCast

**Windows:**
- Double-click `RUN_FLOWCAST.bat`

**Mac/Linux:**
- Open Terminal in this folder
- Run: `./run_flowcast.sh`
- (If permission denied, first run: `chmod +x run_flowcast.sh`)

### Step 3: Use the app

1. Your web browser will open automatically
2. Upload your Xero export file
3. Download your charts!

---

## 📁 How to export from Xero

1. Log into Xero
2. Go to **Reporting** → **All Reports**
3. Click **Profit and Loss**
4. Select **"Current financial Year Month by Month"**
5. Set your date range
6. Click **Update**
7. Click **Export** → **Excel**

---

## 📥 What you can download

| Output | Description |
|--------|-------------|
| Individual charts | PNG images of each chart |
| Excel Report | Spreadsheet with summary data |
| Complete ZIP | Everything in one download |

---

## ❓ Troubleshooting

**"Python is not recognized"**
- Make sure you ticked "Add Python to PATH" when installing
- Restart your computer and try again

**"Module not found" errors**
- Open Command Prompt/Terminal
- Run: `pip install -r requirements.txt`

**Charts look wrong**
- Make sure your Xero export is "Month by Month" format
- Check that the file hasn't been modified

**App won't start**
- Make sure no other app is using port 8501
- Try: `streamlit run flowcast_app.py --server.port 8502`

---

## 🔧 For technical users

```bash
# Manual installation
pip install -r requirements.txt

# Run the app
streamlit run flowcast_app.py

# Run on a different port
streamlit run flowcast_app.py --server.port 8080
```

---

## 📞 Support

Having issues? Contact your friendly neighbourhood developer who set this up for you!
