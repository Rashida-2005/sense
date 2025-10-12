from django.shortcuts import redirect


def role_required(allowed_roles =[]):
    def decorator(view_func):
        def wrapper(request,*args,**kwargs):
            if not request.user.is_authenticated:
                return redirect("mayondo_app:dashboard")
            if request.user.role in allowed_roles:
                return view_func(request,*args,**kwargs)
            return redirect('mayondo_app:logout')
        return wrapper
    return decorator