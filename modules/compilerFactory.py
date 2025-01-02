from modules.notificationEmailCompiler import NotificationEmailCompiler
from modules.notificationInfo import EmailTemplate
from modules.inviteCompiler.orgInviteCompiler import OrgInviteCompiler
from modules.inviteCompiler.projectInviteCompiler import ProjectInviteCompiler


class CompilerFactory:
    @staticmethod
    def get_compiler(template: EmailTemplate, application_input):
        if template == EmailTemplate.NOTIFICATION:
            return NotificationEmailCompiler(application_input)
        elif template == EmailTemplate.PROJECT_INVITE:
            return ProjectInviteCompiler(application_input)
        elif template == EmailTemplate.ORG_INVITE:
            return OrgInviteCompiler(application_input)
        else:
            raise ValueError('Failed to resolve email compiler, template: {0} is not supported'
                             .format(template))