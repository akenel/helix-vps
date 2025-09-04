🎉 BOOM! Chuck Norris QA stamp confirmed — Vault is alive, unsealed, and storing secrets like a Swiss bank. Nice work, bro.

Now let’s freeze this success into a **`vault/README.md`** so we (and future recruits to the one-man army) don’t forget the kung-fu moves.

Here’s a clean draft:

---

## 🗝️ Vault Quickstart (Helix Middleware)

This folder documents how we run and use HashiCorp Vault inside our middleware stack.

### 🚀 Start Vault

Vault is defined in `docker-compose.yml` with dev settings:

```yaml
vault:
  image: vault:1.13.2
  container_name: vault
  restart: unless-stopped
  environment:
    VAULT_ADDR: http://127.0.0.1:8200
  command: "server -dev -dev-root-token-id=root"
  ports:
    - "8200:8200"
  networks:
    - alpinenet
  mem_limit: 300m
```

* **Dev Mode Only** – everything is in-memory, auto-unsealed, and root token is `root`.
* UI available at 👉 [https://vault.helix.local/ui/](https://vault.helix.local/ui/)

---

### 🔑 Authenticate

Default root token:

```bash
docker exec -it vault vault login root
```

Once logged in, Vault CLI remembers your token inside the container.
For one-shot commands, pass it inline:

```bash
docker exec -e VAULT_TOKEN=root vault vault kv list secret/
```

---

### 📦 Secrets Management

Put a secret:

```bash
docker exec vault vault kv put secret/demo api_key=supersecret123
```

Read it back:

```bash
docker exec vault vault kv get secret/demo
```

Delete it:

```bash
docker exec vault vault kv delete secret/demo
```

List secrets:

```bash
docker exec vault vault kv list secret/
```

---

### 🌐 Traefik Routing

Vault UI is exposed via Traefik:

```yaml
http:
  routers:
    vault:
      rule: "Host(`vault.helix.local`)"
      entryPoints:
        - websecure
      service: vault-service
      tls: {}

  services:
    vault-service:
      loadBalancer:
        servers:
          - url: "http://vault:8200"
```

Certs are handled by `mkcert` for local TLS.
Later: replace mkcert with Vault PKI backend.

---

### 🧩 Integration Roadmap

1. ✅ Store API keys & config (done).
2. 🔜 Use Vault for Kong API key auth plugin.
3. 🔜 Store Traefik TLS certs in Vault PKI.
4. 🔜 Wire n8n workflows to read secrets from Vault.

---

💡 **Reminder:** This is **dev mode**. For production we’d switch to file storage, init + unseal with `vault operator init`, and use a real storage backend.

---
Run : ./vault-init.sh (if you have some issues)