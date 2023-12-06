from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
import models as mod
import serializers as ser
import json
# Create your views here.

"""
example API controller function
def dataToReturn(request, custom_url_number): # custom_url_number, represents the "1" in the url below. This is setup in urls.py
    if request.method == "POST"
        #  For anything passed through the uri as a query e.g. https://paddletraffic.net/1/dataOrSomething?username=billy&password=secure
        username = request.POST["username"]  # You can get that data here
        password = request.POST["password"]
    elif request.method == "GET"
        # MODEL -> SERIALIZE -> RESPOND
        stuff = StuffModel.objects.all()  # can do things like .where(...), .filter(...), etc.
        serializer = StuffModelSerializer(stuff, many=True)
        return JsonResponse(serializer.data)
    elif ...
        ...
"""
def locations(request):
    """
    GET /locations
    POST /locations

    :param request:
    :return: JsonResponse
    """
    def post(data):
        serializer = ser.LocationSerializer(data=data)
        if not serializer.is_valid():
            return HttpBadRequestJson()

        new_location = serializer.save()
        return HttpOKRequestJson()

    def get():
        m_locations = mod.Location.objects.all()
        serializer = ser.LocationSerializer(m_locations, many=True)
        return JsonResponse(serializer.data)
    funs = {"POST": post, "GET": get}
    return get_response(request, funs)


def locations_id(request, id):
    """
    GET /locations/{id}
    :param request:
    :param id: id of location
    :return: JsonResponse
    """
    def put(data):
        try:
            existing_location = mod.Location.objects.get(id=id)
        except mod.Location.DoesNotExist:
            return HttpNotFound(str(id))

        serializer = ser.LocationUpdateSerializer(instance=existing_location, data=data)
        if serializer.is_valid():
            updated_location = serializer.save()
        else:
            return HttpResponse("Invalid JSON data", status=400, content_type="text/plain")  # Bad Request

    def get():
        m_locations = mod.Location.objects.filter(id=id)
        serializer = ser.LocationSerializer(m_locations, many=False)
        # return the json formatted as an HTTP response
        return JsonResponse(serializer.data)

    def delete():
        try:
            location = mod.Location.objects.filter(id=id)
            location.delete()
        except mod.Location.DoesNotExist:
            return HttpNotFound(str(id))
        return HttpOK(f"Location {id} deleted")

    funs = {"PUT": put, "GET": get, "DELETE": delete}
    return get_response(request, funs)


def events(request):
    def get():
        m_events = mod.Event.objects.all()
        serializer = ser.EventSerializer(m_events, many=True)
        return JsonResponse(serializer.data)

    def post(data):
        serializer = ser.EventSerializer(data=data)
        if not serializer.is_valid():
            return HttpBadRequestJson()

        new_event = serializer.save()
        return HttpOKRequestJson()

    funs = {"GET": get, "POST": post}
    return get_response(request, funs)



def events_id(request):
    def put(data):
        try:
            existing_event = mod.Event.objects.get(id=id)
        except mod.Event.DoesNotExist:
            return HttpNotFound(str(id))

        serializer = ser.EventUpdateSerializer(instance=existing_event, data=data)
        if serializer.is_valid():
            updated_location = serializer.save()
        else:
            return HttpResponse("Invalid JSON data", status=400, content_type="text/plain")  # Bad Request

    def get():
        m_locations = mod.Event.objects.filter(id=id)
        serializer = ser.EventSerializer(m_locations, many=False)
        # return the json formatted as an HTTP response
        return JsonResponse(serializer.data)

    def delete():
        try:
            location = mod.Event.objects.filter(id=id)
            location.delete()
        except mod.Event.DoesNotExist:
            return HttpNotFound(str(id))
        return HttpOK(f"Location {id} deleted")

    funs = {"PUT": put, "GET": get, "DELETE": delete}
    return get_response(request, funs)


def get_response(request, funs) -> HttpResponse:
    if request.method not in funs.keys():
        return HttpMethodNotAllowed()

    if request.method == "POST":
        if "application/json" not in request.content_type:
            return HttpUnsupportedMedia()

        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return HttpBadRequestJson()
        return funs["POST"](data)

    elif request.method == "GET":
        return funs["GET"]()

    elif request.method == "PUT":
        if not "application/json" in request.content_type:
            return HttpUnsupportedMedia()
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return HttpBadRequestJson()
        return funs["PUT"](data)

    elif request.method == "DELETE":
        return funs["DELETE"]()

    else:  # shouldn't ever get called...
        return HttpMethodNotAllowed()


"""
Status Codes
200 OK: Successful request and processing of JSON data.
400 Bad Request: Invalid JSON data.
405 Method Not Allowed: Request method other than POST is not allowed.
404 Not Found
415 Unsupported Media Type: Requested content type (JSON) is not supported.
"""
def HttpOK(msg):
    return HttpResponse(msg, status=200, content_type="text/plain")  # OK

def HttpBadRequestJson():
    return HttpResponse("Invalid JSON data", status=400, content_type="text/plain")  # Bad Request

def HttpOKRequestJson():
    return HttpResponse("Received and processed JSON data", status=200, content_type="text/plain")  # OK

def HttpUnsupportedMedia():
    return HttpResponse("Unsupported Media Type", status=415, content_type="text/plain")  # Unsupported Media Type

def HttpMethodNotAllowed():
    return HttpResponse("Method Not Allowed", status=405, content_type="text/plain")  # Method Not Allowed

def HttpNotFound(msg):
    return HttpResponse(msg + "Not Found", status=404, content_type="text/plain")