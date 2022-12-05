import json

from django.views import View
from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseServerError,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from onetimesecrets.credentials import API_BASE_URL
from core.exceptions import SecretExpiredError, SecretViewedError
from core.models.ots import Secret
from core.services.secret import SecretService


@method_decorator(csrf_exempt, name="dispatch")
class OTS(View):
    def get(self, request, secret_id: str):
        nonce = request.GET.get("key")
        if not nonce:
            message = "Incorrect URL"
            return HttpResponseBadRequest(message)

        try:
            data = SecretService.get_secret_data(secret_id=secret_id, nonce=nonce)
        except Secret.DoesNotExist:
            message = "Secret Not Found"
            return HttpResponseNotFound(message)
        except SecretExpiredError:
            message = "Secret Expired"
            return HttpResponseNotFound(message)
        except SecretViewedError:
            message = "Secret Already Opened"
            return HttpResponseNotFound(message)
        except Exception:
            message = "Server Error"
            return HttpResponseServerError(message)
        else:
            response = {"secret": data}
            return JsonResponse(response)

    def post(self, request):
        body = json.loads(request.body)
        data = body.get("secret")
        if not data:
            return HttpResponseBadRequest("No secret found in Request Body")
        try:
            secret, nonce = SecretService.create_secret(data)
            url = f"{API_BASE_URL}/api/{secret.id}?key={nonce}"
            return JsonResponse({"url": url})
        except Exception:
            message = "Server Error"
            return HttpResponseServerError(message)
