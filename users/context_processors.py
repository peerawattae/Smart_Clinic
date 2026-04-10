def notifications_context(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': request.user.notifications.filter(is_read=False).count(),
            'recent_notifications': request.user.notifications.all()[:5]
        }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': []
    }
