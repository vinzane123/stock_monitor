# Install virtual environment
sudo apt install python-virtualenv

# Setup virtual environment with python 3.6+
python3 -m venv env

# Install python dependencies
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Run server
python manage.py runserver 8000

# Test on browser
http://localhost:8000

# Future Enhancements
Job scheduler to update stock values every 5 mins.

