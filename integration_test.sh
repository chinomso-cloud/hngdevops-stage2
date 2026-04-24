#!/bin/bash
echo "Running integration tests..."
# A simple check to see if the API is responding
curl -f http://localhost:8000/health || exit 1
echo "Integration tests passed!"