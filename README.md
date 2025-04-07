# **Notification Email Channel**

<img height="40mm" src="https://mk0dataloop4fni44fjg.kinstacdn.com/wp-content/uploads/2020/03/logo.svg">

---

![Notification Dialog](./docs/notificationDialog.png)

---

An application that provides an email notification channel for receiving all subscribed notifications within the Dataloop platform.

---

## **Table of Contents**

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Contribution Guidelines](#contribution-guidelines)
- [Troubleshooting](#troubleshooting)

---

## **Overview**

The `Notification Email Channel` app allows Dataloop users to set up dedicated email channels, ensuring timely receipt of platform notifications based on user subscriptions.

---

## **Prerequisites**

- **Dataloop Python SDK** ([Installation Guide](https://github.com/dataloop-ai/dtlpy))
- **Dataloop CLI** ([CLI Documentation](https://sdk-docs.dataloop.ai/en/latest/cli.html))
- **Git**

---

## **Setup & Installation**

Clone the repository and install the app:

```bash
git clone https://github.com/dataloop-ai-apps/notification-email-channel.git
cd notification-email-channel
```

Publish and install the application using the Dataloop CLI:

```bash
dlp app publish --project-name <PROJECT_NAME>
dlp app install --dpk-id <DPK_ID> --project-name <PROJECT_NAME>
```

Replace `<PROJECT_NAME>` with your project's name and `<DPK_ID>` with the specific ID of the app package.

---

## **Usage**

Once installed, the email notification channel automatically integrates with your Dataloop subscriptions. Notifications will be delivered directly to the configured email address.

For more detailed instructions, visit the [Dataloop Documentation](https://docs.dataloop.ai/docs/modality).

---

## **Contribution Guidelines**

We welcome community contributions:

- Reporting bugs
- Suggesting new features
- Enhancing existing functionality

To contribute, follow the detailed guidelines provided in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## **Troubleshooting**

- **Installation Issues:**
  - Ensure the correct SDK and CLI versions are installed.

- **Notification Issues:**
  - Check your subscription settings on the Dataloop platform.

---
