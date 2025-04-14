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

### Follow the steps below to set up and install the application:  
#### 1. Clone the repository

```bash
git clone https://github.com/dataloop-ai-apps/notification-email-channel.git
cd notification-email-channel
```
#### 2. Configure the application
Open the `dataloop.json` file and update the following fields:

- **`name`**: A unique identifier for your app.  
- **`displayName`**: A human-readable name for the app.  
- **`context`**: Update this section to reflect your project's configuration.

#### 3. Publish and install the application using the Dataloop CLI:

```bash
dlp app publish --project-name <PROJECT_NAME>
dlp app install --dpk-id <DPK_ID> --project-name <PROJECT_NAME>
```

Replace `<PROJECT_NAME>` with your project's name and `<DPK_ID>` with the specific ID of the app package.

---

## **Usage**

Once installed, the Email Notification Channel automatically integrates with your Dataloop subscriptions.  
Notifications will be delivered directly to the configured email address.

### Features

- 📬 **Receive Notifications**  
  Automatically receive real-time notifications based on your project's subscriptions.

- ✏️ **Create or Update the Notification**  
  You can also manually create or update the email notification channel via the Dataloop SDK to customize behavior.

### Additional Resources  

For detailed usage instructions and examples, please refer to the [Dataloop Documentation](https://docs.dataloop.ai/docs/customized-notifications).

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
