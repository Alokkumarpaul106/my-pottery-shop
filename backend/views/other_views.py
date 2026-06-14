from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages


def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"""
Name: {name}
Phone: {phone}
Email: {email}

Message:
{message}
        """

        send_mail(
            subject,
            full_message,
            'alokkumarpaul22076@gmail.com',   # নিজের email
           ['alokkumarpaul22076@gmail.com'], # receiver
        )
        messages.success(request, "মেসেজ পাঠানো হয়েছে ! শীঘ্রই যোগাযোগ করা হবে। ধন্যবাদ!")
    return render(request, 'shop/contact.html')


def returns(request):
    return render(request,'shop/returns.html')