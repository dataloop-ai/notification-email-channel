from modules.notificationInfo import EmailTemplate


class TemplateResolver:
    @staticmethod
    def get_project_invitation_code():
        return 'Platform.Invitations.ProjectInvitation'

    @staticmethod
    def get_organization_invitation_code():
        return 'Platform.Invitations.OrganizationInvitation'

    @staticmethod
    def resolve_template(notification_code):
        if notification_code == TemplateResolver.get_project_invitation_code():
            return EmailTemplate.PROJECT_INVITE
        elif notification_code == TemplateResolver.get_organization_invitation_code():
            return EmailTemplate.ORG_INVITE
        else:
            return EmailTemplate.NOTIFICATION