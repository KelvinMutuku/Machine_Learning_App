from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt  # <-- add
from .forms import IrisForm
from .services import predict_iris
import json


def home(request):
    return render(request, "predictor/predict_form.html", {"form": IrisForm()})


@require_http_methods(["POST"])
def predict_view(request):
    form = IrisForm(request.POST)
    if not form.is_valid():
        return render(request, "predictor/predict_form.html", {"form": form})
    data = form.cleaned_data
    features = [
        data["sepal_length"],
        data["sepal_width"],
        data["petal_length"],
        data["petal_width"],
    ]
    result = predict_iris(features)
    return render(
        request,
        "predictor/predict_form.html",
        {"form": IrisForm(), "result": result, "submitted": True},
    )


@csrf_exempt  # <-- add this line
@require_http_methods(["POST"])
def predict_api(request):
    # Accept JSON only (optional but recommended)
    if request.META.get("CONTENT_TYPE", "").startswith("application/json"):
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
    else:
        # fall back to form-encoded if you want to keep supporting it:
        payload = request.POST.dict()

    required = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    missing = [k for k in required if k not in payload]
    if missing:
        return JsonResponse({"error": f"Missing: {', '.join(missing)}"}, status=400)

    try:
        features = [float(payload[k]) for k in required]
    except ValueError:
        return JsonResponse({"error": "All features must be numeric."}, status=400)

    return JsonResponse(predict_iris(features))