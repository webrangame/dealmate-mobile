# Local AI Setup Guide

This folder contains everything needed to run the Supermarket RAG system completely offline on a local PC.

## Prerequisites
- **Docker Desktop** installed and running.
- **Hardware**: 8GB+ RAM recommended. NVIDIA GPU preferred for speed.

## Installation
1.  Open a terminal in this folder (`supermarket-rag/local_llm_setup`).
2.  Run the installer:
    ```bash
    ./install.sh
    ```
    This will:
    - Start the database, backend, and AI engine (Ollama).
    - Download the smart and fast **Llama 3.1 8B** model (approx 4.7GB).

## Usage
- **Start**: `./start.sh`
- **Stop**: `./stop.sh`

## Verification
Once running, the API will be available at `http://localhost:8001`.
The AI is running at `http://localhost:11434`.

## Customization
To change the model (e.g., to a smaller one for old PCs), edit `docker-compose.yml`:
- Change `LLM_MODEL_NAME` to `ollama/llama3.2:3b`
- Update `install.sh` to pull that model instead.
