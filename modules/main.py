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
        template = EmailTemplate.ORG_INVITE
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


dl.setenv('rc')
notification_input = {
    "notificationInfo": {
        "notificationCode": "test",
        "context": {
            "project": "329a6e2f-914f-40c7-9a21-10cfc1089789",
            "org": "org"
        },
        "priority": 50,
        "eventMessage": {
            "title": "test title",
            "description": "test description",
            "resourceAction": "test resourceAction",
            "resourceId": "test resourceId",
            "resourceType": "test resourceType",
            "resourceName": "test resourceName"
        }
    },
    "recipients": ["shlomi.s@dataloop.ai"],
    "notificationId": 1
}


project_input = {
    "notificationInfo": {
        "notificationCode": "test",
        "context": {
            "project": "329a6e2f-914f-40c7-9a21-10cfc1089789",
            "org": "org"
        },
        "priority": 50,
        "eventMessage": {
            "title": "Project Invite",
            "description": "test description",
            "resourceAction": "test resourceAction",
            "resourceId": "shlomi.s@dataloop.ai",
            "resourceType": "test resourceType",
            "resourceName": "test resourceName"
        }
    },
    "recipients": ["shlomi.s@dataloop.ai"],
    "notificationId": 1
}

org_input = {
    "notificationInfo": {
        "notificationCode": "test",
        "context": {
            "project": "329a6e2f-914f-40c7-9a21-10cfc1089789",
            "org": "6e8f5d61-5960-4677-bb21-d0ddbd94aed3"
        },
        "priority": 50,
        "eventMessage": {
            "title": "test title",
            "description": "test description",
            "resourceAction": "test resourceAction",
            "resourceId": "shlomi.s@dataloop.ai",
            "resourceType": "test resourceType",
            "resourceName": "test resourceName"
        }
    },
    "recipients": ["shlomi.s@dataloop.ai"],
    "notificationId": 1
}

ServiceRunner().email(org_input)
