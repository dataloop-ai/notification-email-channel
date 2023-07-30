from modules.emailCompiler import EmailCompiler
from modules.notificationInfo import EmailTemplate, ApplicationInput


class OrgInviteCompiler(EmailCompiler):
    def __init__(self, application_input: ApplicationInput):
        super().__init__(application_input)
        self.application_params = self.application_input.application_params
        if self.application_params is None:
            raise 'Missing application params, unable to compile project email template'
        self.avatar = self.application_params.get('avatar', None)
        self.role = self.application_params.get('role', None)
        self.domain = self.application_params.get('domain', None)
        if self.avatar is None:
            raise 'Missing avatar param, unable to compile project email template'
        if self.role is None:
            raise 'Missing role param, unable to compile project email template'
        if self.domain is None:
            raise 'Missing domain param, unable to compile project email template'

    def compile_html(self, template: EmailTemplate):
        [compiled, attachments] = super().compile_html(template=template)
        return compiled
