bind = "0.0.0.0:8000"
workers = 4
worker_class = "gunicorn.workers.gthread.ThreadWorker"
threads = 2
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
