# Use a lightweight Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install curl (required to install uv) and clean cache
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (a lightweight web server)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first (for better caching)
COPY pyproject.toml requirements.txt* ./

# Install dependencies using uv (system-wide)
RUN if [ -f requirements.txt ]; then uv pip install --system -r requirements.txt; fi \
    && if [ -f pyproject.toml ]; then uv pip install --system -r pyproject.toml; fi

# Copy project files
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app",  "--host", "0.0.0.0", "--port", "8000", "--reload"]
