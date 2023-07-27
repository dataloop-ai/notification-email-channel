from modules.notificationEmailCompiler import NotificationEmailCompiler
from modules.notificationInfo import EmailTemplate


class CompilerFactory:
    @staticmethod
    def get_compiler(template: EmailTemplate, application_input):
        if template == EmailTemplate.NOTIFICATION:
            return NotificationEmailCompiler(application_input)
        else:
            raise ValueError('Failed to resolve email compiler, template: {0} is not supported'
                             .format(template))