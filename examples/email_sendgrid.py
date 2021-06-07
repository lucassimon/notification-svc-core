from notification_services.backends.sendgrid.config import SendgridConfig
from notification_services.backends.sendgrid.sendgrid_backend import SendgridBackendV3
from notification_services.repositories.sendgrid_repository import SendgridRepository

from notification_services.services import Service

if __name__ == "__main__":
    try:
        email_messages_sendgrid = [1, 2, 3]
        sendgrid_config = SendgridConfig(
            api_key="", sandbox_mode=False, use_queue=False
        )
        sendgrid_repo = SendgridRepository(
            config=sendgrid_config, backend_klass=SendgridBackendV3
        )
        service_sendgrid = Service(sendgrid_repo)

        service_sendgrid.send(email_messages_sendgrid)

    except Exception:
        raise
