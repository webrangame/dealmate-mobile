#!/bin/bash

# Ensure backend/uploaded_docs exists
mkdir -p backend/uploaded_docs

# Copy PDFs to the upload directory
echo "Copying PDFs to backend/uploaded_docs..."
cp Coles.pdf backend/uploaded_docs/
cp Woolworths.pdf backend/uploaded_docs/

# Execute the ingestion script inside the backend container
echo "Running ingestion script in backend container..."
docker-compose exec backend python manual_ingest.py
