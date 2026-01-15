# Dell Technologies Deep Research Dashboard - Streamlit Version

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Create a new folder** for your Streamlit app:
```bash
mkdir dell-research-dashboard
cd dell-research-dashboard
```

2. **Copy the files** from this project:
   - Copy `streamlit_app.py` 
   - Copy `requirements.txt`

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
streamlit run streamlit_app.py
```

5. **Open your browser**:
   - Streamlit will automatically open `http://localhost:8501`
   - If not, manually navigate to that URL

## 📋 Features Included

✅ **All 8 Dashboard Sections:**
- Company Overview with key metrics
- Revenue Breakdown with interactive pie chart
- Business Segments Analysis with bar charts
- Geographic Exposure (3 tabs: Revenue, Manufacturing, Facilities)
- Supply Chain Dependencies (3 tabs: Suppliers, Contract Manufacturers, Components)
- Concentration & Risk Analysis with color-coded badges

✅ **Interactive Elements:**
- Sidebar with research history
- New Research button with company search
- Progress tracking for in-progress analyses
- Navigation to report sections
- Export PDF button (placeholder)
- Scenario Analysis button (placeholder)

✅ **BlackRock Institutional Design:**
- Dark slate header with gradient
- Professional typography and spacing
- Minimal color palette (blues and grays)
- Clean bordered sections
- Responsive layout

## 🎨 Customization

### Change Company Data
Edit the data in `streamlit_app.py` to display different companies. Look for these sections:
- Line 138: Main header (company name)
- Line 165: Company overview metrics
- Line 184: Revenue breakdown data
- Line 207: Business segments data
- And so on...

### Modify Colors
Update the custom CSS in the `st.markdown()` section (lines 15-130) to change:
- Header colors: Look for `#1e293b` and `#334155`
- Accent colors: Look for `#0ea5e9` and `#059669`
- Chart colors: Update `color_discrete_sequence` in Plotly charts

### Add More Companies to History
Modify the `st.session_state.company_history` initialization (lines 134-149):
```python
st.session_state.company_history = [
    {
        "id": 1,
        "name": "Your Company Name",
        "status": "completed",
        "date_completed": "Jan 15, 2025",
        "confidence": 85
    },
    # Add more companies here...
]
```

## 🔧 Common Issues & Solutions

**Issue:** `ModuleNotFoundError: No module named 'streamlit'`
- **Solution:** Make sure you ran `pip install -r requirements.txt`

**Issue:** Port 8501 already in use
- **Solution:** Run with different port: `streamlit run streamlit_app.py --server.port 8502`

**Issue:** Charts not displaying
- **Solution:** Ensure plotly is installed: `pip install plotly`

## 📊 Data Structure

The dashboard uses Pandas DataFrames for all tables. Example structure:

```python
suppliers_df = pd.DataFrame({
    'Supplier': ['Intel Corporation', 'AMD', ...],
    'Component': ['CPUs', 'CPUs', ...],
    'Estimated % of COGS': ['15-20%', '5-8%', ...],
    'Geographic Risk': ['Medium', 'Low', ...]
})
```

Modify these DataFrames to update the displayed data.

## 🌐 Deployment Options

### Streamlit Community Cloud (Free)
1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Deploy!

### Other Options
- **Heroku:** Follow Streamlit's Heroku deployment guide
- **AWS/GCP/Azure:** Deploy as containerized app
- **Local Network:** Use `--server.address 0.0.0.0` to share on local network

## 📝 Next Steps

1. **Replace mock data** with real company data from APIs or databases
2. **Add authentication** if deploying publicly (use `streamlit-authenticator`)
3. **Connect to database** for persistent research history (PostgreSQL, MongoDB, etc.)
4. **Implement actual PDF export** using libraries like `reportlab` or `fpdf`
5. **Add real research API** to actually fetch company data when "New Research" is clicked

## 🆘 Support

For Streamlit documentation and help:
- Official docs: https://docs.streamlit.io
- Community forum: https://discuss.streamlit.io
- Gallery: https://streamlit.io/gallery

## 📄 License

This code is provided as-is for your use. Modify freely to fit your needs.
