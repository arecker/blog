from django.shortcuts import render_to_response


def get_home(request):
    return render_to_response("common/base.html")