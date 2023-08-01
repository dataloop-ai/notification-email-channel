import dtlpy as dl
from modules.main import ServiceRunner

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
        "notificationCode": 'Platform.Invitations.ProjectInvitation',
        "context": {
            "member": "shlomi.s@dataloop.ai",
        },
        "priority": 50,
        "eventMessage": {
            "title": "Project Invitation",
            "description": "test description",
            "resourceAction": "test resourceAction",
            "resourceId": "329a6e2f-914f-40c7-9a21-10cfc1089789",
            "resourceType": "test resourceType",
            "resourceName": "test resourceName"
        }
    },
    "recipients": ["shlomi.s@dataloop.ai"],
    "notificationId": 1
}

org_input = {
    "notificationInfo": {
        "notificationCode": 'Platform.Invitations.OrganizationInvitation',
        "context": {
            "userId": "shlomi.s@dataloop.ai"
        },
        "priority": 50,
        "eventMessage": {
            "title": "Org Invitation",
            "description": "test description",
            "resourceAction": "test resourceAction",
            "resourceId": "6e8f5d61-5960-4677-bb21-d0ddbd94aed3",
            "resourceType": "test resourceType",
            "resourceName": "test resourceName"
        }
    },
    "recipients": ["shlomi.s@dataloop.ai"],
    "notificationId": 1
}

ServiceRunner().email(project_input)
