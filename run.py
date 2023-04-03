from web import app
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    if sys.argv[1] != "80":
        port = int(sys.argv[1])
    else:
        port = 80
except IndexError:
    port = 80

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
