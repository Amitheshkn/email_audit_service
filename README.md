# Email Audit Service

## How to Run

1. Ensure Docker and Docker Compose are installed.
2. Run:
   ```bash
   docker-compose up --build
   ```
3. Use a tool like Postman or `curl` to POST a `.eml` file to:
   ```
   http://localhost:5000/audit
   ```

## Input

- `.eml` files (with plain text or HTML body and image attachment)

## Output

- JSON with scoring and rule justifications
