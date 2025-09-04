#!/bin/bash
set -e

# Check if Vault is already initialized
if docker exec vault vault status | grep -q 'Initialized.*true'; then
  echo "✅ Vault already initialized"
else
  echo "🔐 Initializing Vault..."
  docker exec vault vault operator init -key-shares=1 -key-threshold=1 -format=json > vault-keys.json
  echo "✅ Keys written to vault-keys.json"
fi

# Grab root token + unseal key
ROOT_TOKEN=$(jq -r '.root_token' vault-keys.json)
UNSEAL_KEY=$(jq -r '.unseal_keys_b64[0]' vault-keys.json)

echo "🔓 Unsealing Vault..."
docker exec vault vault operator unseal $UNSEAL_KEY

echo "🔑 Logging in with root token..."
docker exec vault vault login $ROOT_TOKEN

echo "🎉 Vault is ready at https://vault.helix.local"
echo "   Root Token: $ROOT_TOKEN"
echo "   Unseal Key: $UNSEAL_KEY"
echo "   (Also stored in vault-keys.json)"  