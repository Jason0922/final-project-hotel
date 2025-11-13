# Software Requirements for Last Resort Hotels Website

## Required Software

### 1. Python (Programming Language)
- **Version**: Python 3.9 or higher
- **Download**: https://www.python.org/downloads/
- **Why needed**: The Flask web application is written in Python
- **Check if installed**: Open terminal/command prompt and type `python --version`

### 2. pip (Python Package Manager)
- **Usually comes with**: Python 3.4+
- **Why needed**: To install Python packages (Flask, database connectors, etc.)
- **Check if installed**: Type `pip --version` in terminal

### 3. Code Editor / IDE (Choose one)

#### Option A: PyCharm (Recommended for this project)
- **Type**: Professional IDE
- **Download**: https://www.jetbrains.com/pycharm/
- **Why recommended**: 
  - Free Community Edition available
  - Great for Python development
  - Built-in database tools
  - Project structure management
  - Required for final submission

#### Option B: Visual Studio Code (Free)
- **Download**: https://code.visualstudio.com/
- **Extensions needed**:
  - Python extension
  - Flask extension (optional)
- **Why good**: Lightweight, free, popular

#### Option C: Other Options
- **Sublime Text**: https://www.sublimetext.com/
- **Atom**: https://atom.io/
- **Notepad++**: https://notepad-plus-plus.org/ (Windows only)

### 4. Web Browser (Any modern browser)
- **Chrome**: https://www.google.com/chrome/
- **Firefox**: https://www.mozilla.org/firefox/
- **Edge**: Comes with Windows 10/11
- **Safari**: Comes with macOS
- **Why needed**: To view and test the website

### 5. Terminal / Command Prompt
- **Windows**: Command Prompt or PowerShell (built-in)
- **Mac/Linux**: Terminal (built-in)
- **Why needed**: To run Python commands, install packages, start the server

## Optional but Recommended

### 6. Git (Version Control)
- **Download**: https://git-scm.com/downloads
- **Why useful**: 
  - Required for GitHub repository
  - Track changes to your code
  - Collaborate with team members

### 7. Database Software (For later when connecting to real database)

#### Option A: MySQL
- **Download**: https://dev.mysql.com/downloads/
- **Or use**: XAMPP (includes MySQL, PHP, Apache)
- **Download XAMPP**: https://www.apachefriends.org/

#### Option B: PostgreSQL
- **Download**: https://www.postgresql.org/download/

#### Option C: MySQL Workbench (GUI for MySQL)
- **Download**: https://dev.mysql.com/downloads/workbench/
- **Why useful**: Visual database management

### 8. Database Management Tool (Optional)
- **phpMyAdmin**: Comes with XAMPP
- **DBeaver**: https://dbeaver.io/ (Free, works with multiple databases)
- **Why useful**: Easier database management than command line

## Installation Checklist

### For Prototype (Current Phase)
- [ ] Python 3.9+ installed
- [ ] pip working (`pip --version`)
- [ ] Code editor installed (PyCharm recommended)
- [ ] Web browser installed
- [ ] Terminal/Command Prompt accessible

### For Full Project (Later)
- [ ] Git installed (for GitHub)
- [ ] Database software (MySQL or PostgreSQL)
- [ ] Database GUI tool (optional but helpful)

## Quick Installation Guide

### Windows Users

1. **Install Python**:
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: Open Command Prompt, type `python --version`

2. **Install PyCharm**:
   - Download Community Edition (free) from https://www.jetbrains.com/pycharm/
   - Install and open
   - Open your project folder

3. **Install Git** (if using GitHub):
   - Download from https://git-scm.com/download/win
   - Use default settings during installation

### Mac Users

1. **Python**:
   - Usually pre-installed, check with `python3 --version`
   - If not, install from https://www.python.org/downloads/

2. **PyCharm**:
   - Download from https://www.jetbrains.com/pycharm/
   - Install and open

3. **Git**:
   - Usually pre-installed
   - Check with `git --version`

### Linux Users

1. **Python**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   ```

2. **PyCharm**:
   - Download from https://www.jetbrains.com/pycharm/
   - Or use snap: `sudo snap install pycharm-community --classic`

3. **Git**:
   ```bash
   sudo apt-get install git
   ```

## Verifying Installation

### Check Python
```bash
python --version
# or
python3 --version
```

### Check pip
```bash
pip --version
# or
pip3 --version
```

### Check Git (if installed)
```bash
git --version
```

## Running the Website

### Step 1: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Browser
Navigate to: http://localhost:5000

## Troubleshooting

### Python not found
- **Windows**: Reinstall Python and check "Add to PATH"
- **Mac/Linux**: Use `python3` instead of `python`

### pip not found
- **Windows**: `python -m pip install --upgrade pip`
- **Mac/Linux**: `python3 -m pip install --upgrade pip`

### Port 5000 already in use
- Change port in `app.py`: `app.run(debug=True, port=5001)`

### Module import errors
- Make sure you ran: `pip install -r requirements.txt`
- Check you're in the correct directory

## System Requirements

### Minimum Requirements
- **OS**: Windows 7+, macOS 10.12+, or Linux
- **RAM**: 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Internet**: Required for downloading packages and CDN resources

### Recommended Requirements
- **OS**: Windows 10+, macOS 11+, or modern Linux
- **RAM**: 8GB+
- **Storage**: 2GB+ free space
- **Internet**: Stable connection for development

## Summary

### Essential (Must Have)
1. ✅ Python 3.9+
2. ✅ pip (comes with Python)
3. ✅ Code Editor (PyCharm recommended)
4. ✅ Web Browser
5. ✅ Terminal/Command Prompt

### For Full Project (Later)
6. ⏳ Git (for GitHub)
7. ⏳ Database (MySQL or PostgreSQL)
8. ⏳ Database GUI Tool (optional)

---

**You're ready to start!** Install Python and a code editor, then follow the QUICK_START.md guide.



