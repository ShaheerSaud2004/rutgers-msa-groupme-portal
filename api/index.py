import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variable for Vercel
os.environ['VERCEL'] = '1'

from app import app

# Vercel handler - this is the correct way to handle Flask apps on Vercel
def handler(request):
    return app(request.environ, lambda *args: None)