# Use a Python base image
FROM python:3.11-slim

# Install system dependencies, zstd, and Ollama
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    libgomp1 \
    && curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Script to start Ollama, download the model, then start Streamlit
# Added a longer sleep to ensure the server is fully ready
CMD ollama serve & sleep 10 && ollama run llama3 && python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0