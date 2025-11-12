Guidance to use least-privilege service account for Vision API & Cloud Run:

1. Create a service account with roles: Cloud Run Invoker (if needed), Vision API User, Storage Object Viewer (only if you use temporary GCS buckets).
2. Do NOT grant broad roles like Owner.
3. Use short-lived signed URLs or direct upload to Cloud Run to keep processing stateless.
4. Apply data retention policies: delete any temporary files immediately after processing.
5. Log access to a centralized audit log and redact PII from logs.
