# 📧 Email Audit Service

This service audits `.eml` email threads to check for professionalism, tone, grammar, attachments, and more using a flexible rules engine.

---

## 🚀 Features

- Dynamic, JSON-based rules engine
- Evaluates greeting, subject, tone, and attachment presence
- Scores each email and explains pass/fail reasons
- Accepts `.eml` file (plain-text or basic HTML with image attachments)
- Containerized with Docker

---

## ⚙️ Requirements

- Docker installed
- A valid `email_audit.conf` file on host machine (see mounting below)

---

## 🐳 Running with Docker

### 🔨 Build the image

```bash
docker build -t email-audit-service .
```

### ▶️ Run the container (mounting config)

```bash
docker run -v /etc/email_audit/email_audit.conf:/etc/email_audit/email_audit.conf -p 8000:8000 email-audit-service
```

- Replace `/etc/email_audit/email_audit.conf` with the actual path to your config on the host machine. This can be empty if no custom configuration is needed.

---

## 🧪 API Usage

### `POST /audit`

Upload a `.eml` file for audit.

#### 🔁 Example with `curl`:
```bash
curl -X POST http://localhost:8000/email/audit \
  -F "file=@your-email.eml"
```

#### ✅ Response:
```json
{
    "overall_score": 5.0,
    "rule_results": [
        {
            "justification": "No greeting found at the start of the email.",
            "passed": false,
            "rule_name": "Greeting Check",
            "score": 0.0
        },
        {
            "justification": "Subject line is present.",
            "passed": true,
            "rule_name": "Clear Subject",
            "score": 10.0
        },
        {
            "justification": "Tone appears professional.",
            "passed": true,
            "rule_name": "Professional Tone",
            "score": 10.0
        },
        {
            "justification": "No image attachment found.",
            "passed": false,
            "rule_name": "Attachment Check",
            "score": 0.0
        }
    ],
    "status": "success"
}
```

---

## 🔧 Customizing Rules

Edit the `rules.json` file to add, remove, or tweak evaluation logic.

Each rule includes:

```json
{
"name": "Greeting Check",
"description": "Check if email starts with a greeting",
"condition": "any(email.get('body', '').lower().strip().startswith(greeting) for greeting in ['hello', 'hi', 'dear'])",
"score": 10,
"justification_pass": "Greeting found.",
"justification_fail": "No greeting found at the start of the email."
}
```

---

## 🛠 Tech Stack

- Python 3.10
- Flask
- Docker (multi-stage build)

---

## 📬 Sample `.eml` Files

You can test this service using `.eml` files with image attachments. Sample files can be generated or downloaded using email clients like Gmail or Outlook.
We have also included a few sample `.eml` files in the `samples/` directory for quick testing.
