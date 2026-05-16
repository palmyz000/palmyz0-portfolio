# SKILLS.md (System Toolkits & Specific Capabilities)

## Core Capabilities
The system has the following active main features and capabilities:
- **Dynamic Content Injection**: Dynamic web page rendering (Server-side rendering) using Django Template Language based on personal data from a centralized `DATA` dictionary in `views.py`.
- **Contact Form Message Dispatching**: An Asynchronous contact form system (using Client-side Fetch API) that supports JSON data transmission to the server without refreshing the page, displaying operational results back to the user (Success/Error handling).
- **Interactive UI Components**: Supports a terminal-style coding environment loading animation (Terminal-like Loading Screen) and includes special interactive scripts like "Robot Pet" embedded in the web pages.
- **Web Analytics Integration**: Includes embedded tracking scripts for monitoring website visitor statistics via Vercel Web Analytics.

## System Functions
Crucial backend functions and tools for advanced operations:
- **Email Notification System via SMTP**: 
  The backend features a `contact_view` function to receive messages from the Contact Form and send email notifications to the website owner, utilizing the `django.core.mail.send_mail` module.
  - **Operation**: Upon receiving form data, the server connects to the **Gmail** SMTP Server (port 587, TLS enabled).
  - **Authentication**: The system currently uses an App Password for authentication (configured via the `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` variables in `settings.py`).
  - **Usage Warning**: AI Agents modifying this part must recognize that password data used for sending emails should not be exposed in the source code. Additional Error Handling should be implemented in case emails fail to send or there are network issues to prevent application crashes.
