# Notification SVC Core

This is a hub that plugs providers with repository pattern to send messages **only**

## How to contribute

Create the provider on backend folder and implements the configs, payloads (request) and responses.

Every `backend` provider needs extends the `BaseNotificationBackend` and the `open` and `close` and `send` (mainly) methods must be implemented.

Then you need to implement a repository that extends the `NotificationRepositoryInterface`. The `send` method will need implemented

## TODO:

- [ ] SMTP backend
- [ ] MailChimp backend
- [ ] Amazon SES backend

## Run tests

Create a new `.env` file on `tests/.env` folder

Run tests `pytest tests/services/test_service_push_notification_onesignal.py -s -vv -x --ff`

Run coverage `make coverage`
