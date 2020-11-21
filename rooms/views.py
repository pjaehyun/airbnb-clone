from django.views.generic import ListView
from django.http import Http404
from django.shortcuts import render
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        raise Http404()

    # from django.shortcuts import render, redirect
    # from django.core.paginator import Paginator, EmptyPage
    # from . import models

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
