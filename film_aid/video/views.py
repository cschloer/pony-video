from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views import generic



from .models import Video

class IndexView(generic.ListView):
    template_name = 'video/index.html'
    context_object_name = 'video_list'

    def get_queryset(self):
        """Return the published videos."""
        return Video.objects.order_by('-pub_date')

def detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    notes = video.note_set
    print(notes)
    context = {
        'video': video,
        'notes': notes,
    }
    return render(request, 'video/detail.html', context)

