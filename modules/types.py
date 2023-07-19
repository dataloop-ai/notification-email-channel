from enum import Enum


class NotificationResourceType(str, Enum):
    EXECUTIONS = "executions",
    PIPELINES = "pipelines",
    CYCLES = "pipeline.run",
    SERVICES = "services",
    TASKS = "tasks",
    ASSIGNMENTS = "assignments"


class EventMessage:
    def __init__(self, event_message: dict):
        if event_message is None:
            raise ValueError('event_message is None')
        if event_message.get('title', None) is None:
            raise ValueError('title is None')
        if event_message.get('description', None) is None:
            raise ValueError('description is None')
        self.title = event_message.get('title')
        self.description = event_message.get('description')
        self.resource_action = event_message.get('resourceAction', None)
        self.resource_id = event_message.get('resourceId', None)
        self.resource_type = event_message.get('resourceType', None)
        self.resource_name = event_message.get('resourceName', None)


class NotificationInfo:
    def __init__(self, notification_info: dict):
        if notification_info is None:
            raise ValueError('notification_info is None')
        if notification_info.get('notificationCode', None) is None:
            raise ValueError('notificationCode is None')
        if notification_info.get('context', None) is None:
            raise ValueError('context is None')
        if notification_info.get('priority', None) is None:
            raise ValueError('priority is None')
        if notification_info.get('eventMessage', None) is None:
            raise ValueError('eventMessage is None')
        self.notification_code = notification_info.get('notificationCode')
        self.type = notification_info.get('type', None)
        self.context = notification_info.get('context')
        self.priority = notification_info.get('priority')
        self.event_message = EventMessage(notification_info.get('eventMessage'))


class ApplicationInput:
    def __init__(self, application_input: dict):
        if application_input is None:
            raise ValueError('application_input is None')
        if application_input.get('notificationInfo', None) is None:
            raise ValueError('notificationInfo is None')
        if application_input.get('recipients', None) is None:
            raise ValueError('recipients is None')
        if application_input.get('notificationId', None) is None:
            raise ValueError('notificationId is None')
        self.notification_info = NotificationInfo(application_input.get('notificationInfo'))
        self.recipients = application_input.get('recipients')
        self.notification_id = application_input.get('notificationId')

    def get_title(self):
        return self.notification_info.event_message.title

    def get_description(self):
        return self.notification_info.event_message.description

    def get_priority(self):
        return self.notification_info.priority

    def get_resource_id(self):
        return self.notification_info.event_message.resource_id

    def get_project(self):
        return self.notification_info.context.get('project', None)

    def get_resource_type(self):
        return self.notification_info.event_message.resource_type

    def get_service(self):
        return self.notification_info.context.get('service', None)

    def get_pipeline(self):
        return self.notification_info.context.get('pipeline', None)

    def get_user(self):
        return self.notification_info.context.get('user', dict())

    def get_user_email(self):
        return self.get_user().get('email', None)

    def get_user_avatar(self):
        return self.get_user().get('avatar', None)

    def get_user_role(self):
        return self.get_user().get('role', None)


class EmailTemplate(str, Enum):
    NOTIFICATION = "notification_template"
