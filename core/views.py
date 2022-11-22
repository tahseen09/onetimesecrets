from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.shortcuts import render, HttpResponse
from django.views import View
from core.constants import API_BASE_URL
from core.exceptions import SecretExpiredError, SecretViewedError
from core.models.ots import Secret

from core.services.secret import SecretService


class CreateSecretView(View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        data = request.POST.get("data")
        if not data:
            return render(request, "index.html")

        secret, nonce = SecretService.create_secret(data)
        link = f"{API_BASE_URL}/view/{secret.id}?key={nonce}"
        return render(request, "show.html", {"link": link})


class ShowSecretView(View):
    def get(self, request, secret_id):
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
            return render(request, "show.html", {"data": data})
