import os
import sys

# Add your project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variable to point to your settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'justnaijablog.settings'

# Activate your virtual environment
# This path might vary based on your cPanel setup, adjust as needed
# Example: venv_path = '/home/yourcpanelusername/virtualenv/your_app_name/3.x'
# Be careful with this, cPanel's Python app manager usually handles it.
# For now, you might leave it commented or adjust later if needed.
# activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
# with open(activate_this) as f:
#     exec(f.read(), dict(__file__=activate_this))


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Optional: Fix for PATH_INFO if your app is in a subdirectory
# from urllib.parse import unquote
# class PassengerPathInfoFix(object):
#     def __init__(self, app):
#         self.app = app
#     def __call__(self, environ, start_response):
#         environ['SCRIPT_NAME'] = unquote(environ.get('SCRIPT_NAME', ''))
#         return self.app(environ, start_response)
# application = PassengerPathInfoFix(application)