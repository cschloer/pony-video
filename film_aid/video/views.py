from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import generic
from django.utils import timezone
import json

from .models import Video, Note

class IndexView(generic.ListView):
    template_name = 'video/index.html'
    context_object_name = 'video_list'

    def get_queryset(self):
        """Return the published videos."""
        return Video.objects.order_by('-pub_date')

def detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    context = {
        'video': video,
    }
    return render(request, 'video/detail.html', context)

def create_note(request, video_id):
    try:
        title = request.POST['title']
        description = request.POST['description']
        note_type = request.POST['note_type']
        ts = request.POST['ts']
    except KeyError as e:
        return HttpResponseBadRequest('Missing a value for the note field')
    video = Video.objects.get(pk=video_id)
    note = video.note_set.create(
        title=title,
        description=description,
        note_type=note_type,
        ts=ts,
        pub_date=timezone.now(),
        user=request.user,
    )
    return JsonResponse({
        'status': 'success',
        'note': {
            'id': note.id,
            'title': title,
            'description': description,
            'note_type': note_type,
            'ts': ts,
        },
    })

