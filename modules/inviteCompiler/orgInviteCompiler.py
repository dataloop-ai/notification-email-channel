from modules.emailCompiler import EmailCompiler
from modules.inviteCompiler.utils import InviteCompilerUtils
from modules.notificationInfo import EmailTemplate, ApplicationInput


class OrgInviteCompiler(EmailCompiler):
    def __init__(self, application_input: ApplicationInput):
        super().__init__(application_input)
        self.user_id = self.application_input.get_user_id()
        if self.user_id is None:
            raise ValueError('user_id is None')
        org_id = self.application_input.get_resource_id()
        if org_id is None:
            raise ValueError('org_id is None')
        self.org = self.get_org(org_id=org_id)
        self.member = self.get_org_member(org=self.org, user_id=self.user_id)
        self.redirect_link = InviteCompilerUtils.generate_redirect_link(
            body=self.application_input.notification_info.body,
            env_prefix=self.env_prefix,
            base_path='iam'
        )

    @staticmethod
    def api_role_to_display_role(api_role):
        return api_role.title()

    def replace_params(self, compiled):
        role = OrgInviteCompiler.api_role_to_display_role(
            self.application_input.notification_info.body.get('role', None) or 'Unknown role'
        )
        params = [
            {"name": "userEmail", "value": self.user_id},
            {"name": "role", "value": role},
            {"name": "orgName", "value": self.application_input.notification_info.body.get('name', None) or 'Unknown name'},
            {"name": "redirectLink", "value": self.redirect_link}
        ]
        for param in params:
            compiled = compiled.replace('##{0}##'.format(param['name']), param['value'])
        return compiled

    def replace_avatar(self, compiled):
        if self.member and self.member['avatar']:
            compiled = compiled.replace('@@userImage@@', self.member['avatar'])
        else:
            compiled = compiled.replace('@@userImage@@', self.default_avatar)
        return compiled

    def compile_html(self, template: EmailTemplate):
        [compiled, attachments] = super().compile_html(template=template)
        compiled = self.replace_params(compiled)
        compiled = self.replace_avatar(compiled)
        return [compiled, attachments]
