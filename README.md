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

## **Repository Governance**

This repository is governed according to our established guidelines to ensure consistency, security, and efficiency.

#### 1. Quarterly Reviews
Regular audits to verify repository activity, permissions, compliance, and health.

#### 2. Deprecation Process
Inactive or redundant repositories (no commits for 6+ months) are proposed for archival with stakeholder notification and a feedback period.

#### 3. Public/Private Evaluation
Annual assessments or upon significant changes, evaluating security, intellectual property, and compliance implications.

For repository issues or suggestions, please use the dedicated Slack channel (`#github-repo-governance`) or raise a ticket in the Repository Governance Jira board.

For detailed information, please see the [Repository Governance Document](https://dataloop.atlassian.net/wiki/spaces/DG/pages/1342799902/Git+Repository+Governance+Process?force_transition=34c5fc5b-725f-4d3e-8687-06e76a169d5e) or contact the DevOps Team.