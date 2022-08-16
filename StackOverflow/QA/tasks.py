from celery import shared_task

@shared_task(bind=True)
def sendEmail(self, sender=False, receiver=False, message=""):
    result = "Notification mail has been sent from "+str(sender)+" to "+str(receiver)+"."
    return result
    