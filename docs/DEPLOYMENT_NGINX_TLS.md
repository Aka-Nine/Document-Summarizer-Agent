# Deployment: Nginx Reverse Proxy and TLS (Let's Encrypt)

This document explains how to run the application behind Nginx with TLS using Let's Encrypt.

Prerequisites
- Docker and Docker Compose installed on the deployment host
- A registered domain name pointing to your server's public IP
- Ports 80 and 443 open in your firewall

Quick steps (Docker Compose)

1. Place your domain in `infra/nginx/nginx.conf` (replace `example.com`).

2. Start the app and nginx services:

```bash
docker-compose -f infra/nginx/docker-compose-nginx.yml up -d --build
```

3. Obtain a Let's Encrypt certificate (example using certbot container):

```bash
docker run --rm -it \
  -v "$(pwd)/letsencrypt:/etc/letsencrypt" \
  -v "$(pwd)/letsencrypt-var:/var/lib/letsencrypt" \
  certbot/certbot certonly --standalone \
  -d example.com -m your-email@example.com --agree-tos --no-eff-email
```

4. Reload nginx (inside container or host):

```bash
docker exec doc_nginx nginx -s reload
```

Notes
- If you use orchestration (Kubernetes), replace the nginx service with an Ingress controller and use cert-manager for certificates.
- For automated renewal, the `certbot` service in `docker-compose-nginx.yml` runs `certbot renew` periodically.
- Ensure file permissions for `/etc/letsencrypt` are correct for the `nginx` container to read certificates.

Security hardening
- Use strong TLS ciphers and TLSv1.2+ only.
- Monitor certificate expiry and renewal logs.
- Use HTTP -> HTTPS redirects and HSTS (configured in `nginx.conf`).
