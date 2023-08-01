from modules.notificationInfo import EmailTemplate


class TemplateResolver:
    @staticmethod
    def resolve_template(notification_code):
        if notification_code == 'Platform.Invitations.ProjectInvitation':
            return EmailTemplate.PROJECT_INVITE
        elif notification_code == 'Platform.Invitations.OrganizationInvitation':
            return EmailTemplate.ORG_INVITE
        else:
            return EmailTemplate.NOTIFICATION
