from waitress import serve
from grad.wsgi import application

serve(application, listen='82.165.181.100:81')
