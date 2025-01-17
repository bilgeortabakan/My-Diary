# My Diary - Digital Journal Application

## Project Overview
My Diary is a web-based digital journal application that allows users to record their daily thoughts, memories, and experiences. Built with Flask and modern web technologies, it provides an intuitive interface for maintaining a personal diary with both text and image entries.

## Features
- **Monthly Calendar View**: Interactive calendar interface showing all months of the year
- **Daily Entries**: Add thoughts and images for any day
- **Profile Management**: Customize your profile with a photo
- **Responsive Design**: Works seamlessly on both desktop and mobile devices
- **Image Support**: Upload and manage images for both profile and daily entries
- **Secure Storage**: All data is stored securely in a local database

## Technology Stack
- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Tailwind CSS
- **Icons**: Font Awesome

## Installation

1. Clone the repository
```bash
git clone https://github.com/your-username/my-diary.git
cd my-diary
```

2. Create and activate virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
python app.py
```

5. Run the application
```bash
flask run
# or
python app.py
```

## Project Structure
```
my-diary/
├── static/
│   ├── uploads/
│   └── styles.css
├── templates/
│   ├── index.html
│   └── thoughts.html
├── app.py
├── requirements.txt
└── README.md
```

## Usage
1. Start the application and navigate to `http://localhost:5001`
2. Upload a profile picture (optional)
3. Click on any date in the calendar to add an entry
4. Add text and/or images to your daily entry
5. Save your entry and view it in the calendar

## Contributing
Feel free to fork the repository and submit pull requests for any improvements you make. Please ensure you follow the existing code style and add appropriate tests for new features.

## License
This project is licensed under the MIT License - see the LICENSE file for details.# My-Diary
