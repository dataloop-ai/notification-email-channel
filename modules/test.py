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
