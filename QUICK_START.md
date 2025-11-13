# Quick Start Guide - Prototype Website

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
Open your terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5000**

## ✨ What You'll See

The dashboard displays:
- **3 Summary Cards**: Total Revenue, Occupancy Rate, Customer Count
- **4 Interactive Charts**: Revenue trends, occupancy, service breakdown, seasonal analysis
- **4 Data Tables**: Top customers, top rooms, events, customer retention

## 📝 Modifying the Mock Data

All data is generated in `app.py`. To modify:

1. Open `app.py`
2. Find the function you want to change (e.g., `generate_top_customers()`)
3. Edit the data in the list/dictionary
4. Save and refresh your browser

### Example: Adding a Customer
```python
def generate_top_customers():
    customers = [
        {'customer_name': 'Your New Customer', 
         'party_type': 'organization', 
         'total_revenue': 50000, 
         'total_reservations': 5, 
         'last_visit_date': '2024-11-25'},
        # ... existing customers ...
    ]
    return customers
```

## 🔄 Converting to Real Database (Later)

When your database is ready:

1. **Create config.py** from `config.example.py`
2. **Replace mock functions** in `app.py` with database queries
3. **Update the route** to use real query functions

See `README_PROTOTYPE.md` for detailed instructions.

## 🎨 Customization

- **Colors**: Edit `static/css/style.css`
- **Layout**: Modify `templates/index.html`
- **Charts**: Adjust Chart.js options in the `<script>` section

## ⚠️ Troubleshooting

**Port 5000 already in use?**
- Change port in `app.py`: `app.run(debug=True, port=5001)`

**Charts not showing?**
- Check browser console (F12) for errors
- Ensure internet connection (CDN resources needed)

**Module not found?**
- Run: `pip install -r requirements.txt`

## 📁 File Structure

```
groupproject/
├── app.py              ← Main application (edit mock data here)
├── templates/
│   ├── base.html      ← Base template
│   └── index.html     ← Dashboard page
├── static/
│   └── css/
│       └── style.css  ← Custom styles
└── requirements.txt   ← Dependencies
```

## 🎯 Next Steps

1. ✅ Test the prototype
2. ✅ Customize mock data to match your needs
3. ✅ Adjust styling if desired
4. ⏳ Wait for database to be ready
5. ⏳ Replace mock data with real queries

---

**Ready to go!** Just run `python app.py` and open http://localhost:5000



