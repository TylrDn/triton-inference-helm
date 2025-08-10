#!/usr/bin/env bash
URL=${1:-http://localhost:8000/predict}
BODY='{"features":[1,2,3]}'
if command -v hey >/dev/null 2>&1; then
  hey -n 100 -c 10 -m POST -H "Content-Type: application/json" -d "$BODY" "$URL"
else
  echo "hey not installed; skipping load test"
fi
