from app import create_app

app = create_app()

if __name__ == '__main__':
    # Bind to 0.0.0.0 to be accessible externally (e.g., from Docker)
    # Port 5000 is specified to match Dockerfile EXPOSE and common practice.
    app.run(host='0.0.0.0', port=5000, debug=True)
