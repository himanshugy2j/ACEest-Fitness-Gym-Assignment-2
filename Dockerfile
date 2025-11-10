FROM python:3.11-slim

# Install system dependencies for tkinter
RUN apt-get update && \
    apt-get install -y \
    python3-tk \
    tk \
    tcl \
    libtk8.6 \
    libtcl8.6 \
    x11-common \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Upgrade pip and install Python dependencies
RUN python3 -m pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && pip install pytest pytest-cov


CMD ["python3", "app/ACEest_Fitness.py"]