import dtlpy as dl
from modules.main import ServiceRunner

dl.setenv('rc')
notification_input = {
    "notificationInfo": {
        "notificationCode": "Platform.Faas.Service.RestartError",
        "context": {
            "project": "329a6e2f-914f-40c7-9a21-10cfc1089789",
            "org": "org",
            "model": "modelId",
            "pipeline": "pipelineId"
        },
        "priority": 50,
        "eventMessage": {
            "title": "test title",
            "description": "Execution failed due to code/runtime error in service. Traceback (most recent call last):\n  File \"/usr/local/lib/python3.6/dist-packages/dtlpy_agent/services/client_api.py\", line 1303, in _run_execution\n    context=context\n  File \"/usr/local/lib/python3.6/dist-packages/dtlpy_agent/services/client_api.py\", line 1061, in _parse_package_input\n    context=context\n  File \"/usr/local/lib/python3.6/dist-packages/dtlpy_agent/services/client_api.py\", line 953, in _parse_execution_input\n    inputs[name] = self._fetch_single_resource(value=value, output_type=output_type, sdk=sdk)\n  File \"/usr/local/lib/python3.6/dist-packages/dtlpy_agent/services/client_api.py\", line 891, in _fetch_single_resource\n    return getattr(sdk, '{}s'.format(output_type.lower())).get(**params) if params is not None else value\n  File \"/usr/local/lib/python3.6/dist-packages/dtlpy/repositories/items.py\", line 283, in get\n    message='Must choose by at least one. \"filename\" or \"item_id\"')\n  File \"/usr/local/lib/python3.6/dist-packages/dtlpy/exceptions.py\", line 49, in __init__\n    raise exceptions[self.status_code](status_code=self.status_code, message=self.message)\ndtlpy.exceptions.BadRequest: ('400', 'Must choose by at least one. \"filename\" or \"item_id\"')",
            "resourceAction": "test resourceAction",
            "resourceId": "test resourceId",
            "resourceType": "services",
            "resourceName": "test resourceName"
        },
        "body": {
            "id": "2f060744-e26f-405b-a326-80fb59170d7d",
            "name": "TEST_OA_E2E_PROJECT_1707987814973",
            "createdAt": 1707953109612,
            "updatedAt": 1707953109612,
            "url": "https://rc-gate.dataloop.ai/api/v1/projects/2f060744-e26f-405b-a326-80fb59170d7d",
            "archived": None,
            "creator": "playwright@tests.com",
            "org": "54feb3f8-f3a0-4ac3-bf77-0be1f7960f3d",
            "account": "794b6aa7-e772-4d8c-9952-4167bbc88da0",
            "role": "annotator",
            "enrichment": {
                "notificationPath": "Platform.Invitations.ProjectInvitation",
                "recipients": {
                    "0": "dataloop-tester-5-0@dataloop.ai",
                }
            }
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
        },
        "body": {
            "id": "2f060744-e26f-405b-a326-80fb59170d7d",
            "name": "TEST_OA_E2E_PROJECT_1707987814973",
            "createdAt": 1707953109612,
            "updatedAt": 1707953109612,
            "url": "https://rc-gate.dataloop.ai/api/v1/projects/2f060744-e26f-405b-a326-80fb59170d7d",
            "archived": None,
            "creator": "playwright@tests.com",
            "org": "54feb3f8-f3a0-4ac3-bf77-0be1f7960f3d",
            "account": "794b6aa7-e772-4d8c-9952-4167bbc88da0",
            "role": "annotator",
            "enrichment": {
                "notificationPath": "Platform.Invitations.ProjectInvitation",
                "recipients": {
                    "0": "dataloop-tester-5-0@dataloop.ai",
                }
            }
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
