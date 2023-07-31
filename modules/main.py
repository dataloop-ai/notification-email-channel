import dtlpy as dl
from modules.compilerFactory import CompilerFactory
from modules.notificationInfo import ApplicationInput, EmailTemplate


class ServiceRunner(dl.BaseServiceRunner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def email(self, input: dict):
        application_input = ApplicationInput(input)
        if application_input.recipients is None or len(application_input.recipients) == 0:
            return
        template = EmailTemplate.NOTIFICATION
        compiler = CompilerFactory.get_compiler(template=template, application_input=application_input)
        [compiled_html, attachments] = compiler.compile_html(template=template)
        title = '[Dataloop] ' + str(application_input.get_title()).title()
        from_sender = 'notifications@dataloop.ai'
        from_name = 'Dataloop Notifications'
        req_data = {
            "to": application_input.recipients,
            "from": from_sender,
            "subject": title,
            "body": compiled_html,
            "attachments": attachments,
            "personalize": True,
            "senderName": from_name
        }
        dl.client_api.gen_request(req_type='post', json_req=req_data, path='/outbox')
