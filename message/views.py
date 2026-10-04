from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def message_list(request):
    messages_received = Message.objects.filter(receiver=request.user).select_related('sender').order_by('-created_at')
    return render(request, 'message/list.html', {'messages_received': messages_received})
