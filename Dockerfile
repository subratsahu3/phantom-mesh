# ==============================================================================
# Multi-stage, ultra-lightweight, hardened Dockerfile for PhantomMesh
# Designed for 24/7 Free Deployment on Render, Koyeb, Railway, or Hugging Face
# ==============================================================================
FROM python:3.12-slim AS runtime

# Set security environment flags
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8888 \
    PHANTOM_ADMIN_NAME="Subrat Sahu" \
    PHANTOM_ADMIN_EMAIL="subratsahu195@gmail.com"

WORKDIR /app

# Create unprivileged security user (defense-in-depth)
RUN groupadd -g 10001 phantom && \
    useradd -u 10001 -g phantom -s /bin/bash -m phantom

# Copy project files
COPY . /app

# Set permissions
RUN chown -R phantom:phantom /app

USER phantom

# Expose web service port
EXPOSE 8888

# Healthcheck to verify the deception daemon is alive
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:' + str(os.environ.get('PORT', 8888))).read()" || exit 1

# Launch the Deception Daemon & SOC Command Center
CMD ["sh", "-c", "python -m phantom_mesh.cli tarpit --host 0.0.0.0 --port ${PORT}"]
