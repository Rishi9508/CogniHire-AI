#!/bin/bash
echo "==================================================="
echo "  SemantiHire AI - Setup Script"
echo "==================================================="
echo ""

echo "[1/4] Setting up Python virtual environment in backend..."
cd backend
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment. Make sure Python 3.10+ is installed."
    exit 1
fi

echo ""
echo "[2/4] Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies."
    exit 1
fi

echo ""
echo "[3/4] Downloading spaCy English model..."
python -m spacy download en_core_web_sm
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to download spaCy language model."
    exit 1
fi

echo ""
echo "[4/4] Creating environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
fi
cd ..

echo ""
echo "==================================================="
echo "  Backend setup complete!"
echo "==================================================="
echo ""
echo "To run the Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "To run the Frontend:"
echo "  cd frontend"
echo "  npm install"
echo "  npm run dev"
echo ""
echo "==================================================="
