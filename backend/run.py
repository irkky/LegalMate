from app import create_app
from dotenv import load_dotenv; load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Original startup configuration preserved:
    # - Host and port matching original app.run()
    # - Debug mode remains False
    # - No additional middleware or hooks
    app.run(host='0.0.0.0', port=5000, debug=False)