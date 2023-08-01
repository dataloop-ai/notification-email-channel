import dtlpy as dl


class EmailDispatcher:
    @staticmethod
    def dispatch(application_input, compiled_html, attachments):
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