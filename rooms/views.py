from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, reverse
from django.core.paginator import Paginator
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                rooms = models.Room.objects.filter(**filter_args)

                for amenity in amenities:
                    rooms = rooms.filter(amenities=amenity)

                for facility in facilities:
                    rooms = rooms.filter(facilities=facility)

                rooms = rooms.order_by("-created")

                paginator = Paginator(rooms, 10)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                if room_type is None:
                    room_type = ""
                if price is None:
                    price = ""
                if guests is None:
                    guests = ""
                if bedrooms is None:
                    bedrooms = ""
                if beds is None:
                    beds = ""
                if baths is None:
                    baths = ""
                current_url = f"/rooms/search/?city={city}&country={country}&room_type={room_type}&price={price}&guests={guests}&bedrooms={bedrooms}&beds={beds}&baths={baths}"

                if instant_book is True:
                    current_url = current_url + "&instant_book=on"
                if superhost is True:
                    current_url = current_url + "&superhost=on"

                if len(amenities) > 0:
                    for a in amenities:
                        current_url = current_url + f"&amenities{a.pk}"
                if len(facilities) > 0:
                    for f in facilities:
                        current_url = current_url + f"&facilities{f.pk}"

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms, "path": current_url},
                )
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})

    # from django.shortcuts import render, redirect
    # from django.core.paginator import Paginator, EmptyPage
    # from . import models
    # from django.http import Http404
    # from django.shortcuts import render

    # def all_rooms(request):
    """ Pagination of Django """
    #     page = request.GET.get("page", 1)
    #     room_list = models.Room.objects.all()
    #     paginator = Paginator(room_list, 10, orphans=5)
    #     try:
    #         rooms = paginator.page(int(page))
    #         return render(request, "rooms/home.html", context={"page": rooms})
    #     except EmptyPage:
    #         return redirect("/")

    """ Pagination of not automatically """
    # page = request.GET.get("page", 1)
    # page = int(page or 1)
    # page_size = 10
    # limit = page_size * page
    # offset = limit - page_size
    # all_rooms = models.Room.objects.all()[offset:limit]
    # page_count = models.Room.objects.count() / page_size
    # return render(
    #     request,
    #     "rooms/home.html",
    #     context={
    #         "rooms": all_rooms,
    #         "page": page,
    #         "page_count": ceil(page_count),
    #         "page_range": range(1, ceil(page_count)),
    #     },
    # )

    """ Room detail FBV """
    # def room_detail(request, pk):
    # try:
    #     room = models.Room.objects.get(pk=pk)
    #     return render(request, "rooms/detail.html", {"room": room})
    # except models.Room.DoesNotExist:
    #     raise Http404()

    """ Search FBV """
    # def search(request):
    # city = request.GET.get("city", "Anywhere")
    # city = str.capitalize(city)
    # country = request.GET.get("country", "KR")
    # room_type = int(request.GET.get("room_type", 0))
    # price = int(request.GET.get("price", 0))
    # guests = int(request.GET.get("guests", 0))
    # bedrooms = int(request.GET.get("bedrooms", 0))
    # beds = int(request.GET.get("beds", 0))
    # baths = int(request.GET.get("baths", 0))
    # instant = bool(request.GET.get("instant", False))
    # superhost = bool(request.GET.get("superhost", False))
    # s_amenities = request.GET.getlist("amenities")
    # s_facilities = request.GET.getlist("facilities")

    # form = {
    #     "city": city,
    #     "s_room_type": room_type,
    #     "s_country": country,
    #     "price": price,
    #     "guests": guests,
    #     "bedrooms": bedrooms,
    #     "beds": beds,
    #     "baths": baths,
    #     "s_amenities": s_amenities,
    #     "s_facilities": s_facilities,
    #     "instant": instant,
    #     "superhost": superhost,
    # }

    # room_types = models.RoomType.objects.all()
    # amenities = models.Amenity.objects.all()
    # facilities = models.Facility.objects.all()

    # choices = {
    #     "countries": countries,
    #     "room_types": room_types,
    #     "amenities": amenities,
    #     "facilities": facilities,
    # }

    # filter_args = {}

    # if city != "Anywhere":
    #     filter_args["city__startswith"] = city

    # filter_args["country"] = country

    # if room_type is not None:
    #     filter_args["room_type__pk"] = room_type

    # if price is not None:
    #     filter_args["price__lte"] = price

    # if guests is not None:
    #     filter_args["guests__gte"] = guests

    # if bedrooms is not None:
    #     filter_args["bedrooms__gte"] = bedrooms

    # if beds is not None:
    #     filter_args["beds__gte"] = beds

    # if baths is not None:
    #     filter_args["baths__gte"] = baths

    # if instant is True:
    #     filter_args["instant_book"] = True

    # if superhost is True:
    #     filter_args["host__superhost"] = True

    # rooms = models.Room.objects.filter(**filter_args)

    # if len(s_amenities) > 0:
    #     for s_amenity in s_amenities:
    #         rooms = rooms.filter(amenities__pk=int(s_amenity))

    # if len(s_facilities) > 0:
    #     for s_facility in s_facilities:
    #         rooms = rooms.filter(facilities__pk=int(s_facility))

    # return render(
    #     request,
    #     "rooms/search.html",
    #     {**form, **choices, "rooms": rooms},
    # )
