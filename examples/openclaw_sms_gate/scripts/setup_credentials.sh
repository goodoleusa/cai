#!/bin/bash
# Setup SMSGATE_AUTH environment variable (Linux/macOS)
# Usage: source setup_credentials.sh
# Or add to ~/.bashrc or ~/.zshrc:
#   export SMSGATE_AUTH=$(echo -n "USERNAME:PASSWORD" | base64)

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: export SMSGATE_AUTH=\$(echo -n 'USERNAME:PASSWORD' | base64)"
    echo "Or: source setup_credentials.sh USERNAME PASSWORD"
    exit 1
fi

export SMSGATE_AUTH=$(echo -n "$1:$2" | base64)
echo "SMSGATE_AUTH set. Add to ~/.bashrc for persistence:"
echo "  export SMSGATE_AUTH=\$(echo -n '$1:PASSWORD' | base64)"
