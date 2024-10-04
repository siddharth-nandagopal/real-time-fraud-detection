from starlette.requests import Request
from starlette.responses import JSONResponse


from app import response
from app.models.alert import Alert


class AlertController:

    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            alerts = Alert.objects.all().to_json()
            print(alerts)
            return response.ok(alerts, '')
        except Exception as e:
            print(e)
            return response.badRequest('', f'{e}')