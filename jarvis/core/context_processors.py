# core/context_processors.py

def avatar_processor(request):
    if request.user.is_authenticated:
        
        avatar = request.user.avatar_choice if hasattr(
            request.user, 'avatar_choice') else None
        return {'current_avatar': avatar}
    return {'current_avatar': None}
