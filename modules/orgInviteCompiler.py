from modules.emailCompiler import EmailCompiler
from modules.notificationInfo import EmailTemplate, ApplicationInput


class OrgInviteCompiler(EmailCompiler):
    def __init__(self, application_input: ApplicationInput):
        super().__init__(application_input)
        self.user_id = self.application_input.get_member()
        org_id = self.application_input.get_resource_id()
        self.org = self.get_org(org_id=org_id)
        self.member = self.get_org_member(org=self.org, user_id=self.user_id)
        self.role = self.member.get('role', None) or 'Unknown Role'

    def replace_params(self, compiled):
        params = [
            {"name": "userEmail", "value": self.user_id},
            {"name": "role", "value": self.role},
            {"name": "domain", "value": self.env_prefix},
            {"name": "orgName", "value": self.org.name or 'Unknown name'},
            {"name": "orgId", "value": self.org.id}
        ]
        for param in params:
            compiled = compiled.replace('##{0}##'.format(param['name']), param['value'])
        return compiled

    def replace_avatar(self, compiled):
        compiled = compiled.replace('@@userImage@@', self.member['avatar'])
        return compiled

    def compile_html(self, template: EmailTemplate):
        [compiled, attachments] = super().compile_html(template=template)
        compiled = self.replace_params(compiled)
        compiled = self.replace_avatar(compiled)
        return [compiled, attachments]
