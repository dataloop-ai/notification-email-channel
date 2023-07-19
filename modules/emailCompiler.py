import base64
from abc import ABC, abstractmethod
from modules.main import assets_folder
from modules.notificationEmailCompiler import NotificationEmailCompiler
from modules.types import EmailTemplate, ApplicationInput


class EmailCompiler(ABC):
    @abstractmethod
    def __init__(self, application_input: ApplicationInput):
        super().__init__()
        self.application_input = application_input

    def build_logo_attachment(self):
        image_id = 'logo'
        logo_file_content = open(assets_folder + '/logo.png', 'rb').read()
        logo_base64_utf8_str = base64.b64encode(logo_file_content).decode('utf-8')
        return {
            "filename": "logo",
            "contentType": "image/png",
            "content_id": image_id,
            "content": logo_base64_utf8_str,
            "disposition": "inline"
        }

    def append_logo_attachment(self, compiled):
        attachments = []
        logo_attachment = self.build_logo_attachment()
        attachments.append(logo_attachment)
        compiled = compiled.replace('@@logo@@', 'cid:'+logo_attachment['content_id'])
        return [compiled, attachments]

    def append_attachments(self, compiled):
        [compiled, attachments] = self.append_logo_attachment(compiled)
        return [compiled, attachments]

    @abstractmethod
    def compile_html(self, template: EmailTemplate):
        with open(assets_folder + '/{0}.html'.format(template), 'r') as file:
            compiled = file.read()
        compiled = compiled.replace('##title##', self.application_input.get_title())
        compiled = compiled.replace(
            '##description##', self.application_input.get_description())
        [compiled, attachments] = self.append_attachments(compiled)
        return [compiled, attachments]

    @staticmethod
    def get_compiler(template: EmailTemplate, application_input):
        if template == EmailTemplate.NOTIFICATION:
            return NotificationEmailCompiler(application_input)
        else:
            raise ValueError('Failed to resolve email compiler, template: {0} is not supported'
                             .format(template))
