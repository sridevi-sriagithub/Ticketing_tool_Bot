"""
Notification model to track Teams message delivery.
Add this model to timer/models.py or import it as a separate app.
"""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Track Teams notifications sent to users."""
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('retrying', 'Retrying'),
    ]
    METHOD_CHOICES = [
        ('graph_1to1', '1:1 via Graph'),
        ('webhook', 'Incoming Webhook'),  File "D:\ticketing tool all\12-11-25\v\Lib\site-packages\billiard\queues.py", line 394, in get_payload
    with self._rlock:
         ^^^^^^^^^^^
  File "D:\ticketing tool all\12-11-25\v\Lib\site-packages\billiard\synchronize.py", line 115, in __enter__
    return self._semlock.__enter__()
           ~~~~~~~~~~~~~~~~~~~~~~~^^
PermissionError: [WinError 5] Access is denied

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "D:\ticketing tool all\12-11-25\v\Lib\site-packages\billiard\pool.py", line 351, in workloop
    req = wait_for_job()
  File "D:\ticketing tool all\12-11-25\v\Lib\site-packages\billiard\pool.py", line 480, in receive
    raise SystemExit(EX_FAILURE)
SystemExit: 1

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "D:\ticketing tool all\12-11-25\v\Lib\site-packages\billiard\pool.py", line 292, in __call__
    sys.exit(self.workloop(pid=pid))
             ~~~~~~~~~~~~~^^^^^^^^^
  File "D:\ticketing tool all\12-11-25\v\Lib\site-packages\billiard\pool.py", line 396, in workloop
    self._ensure_messages_consumed(completed=completed)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "D:\ticketing tool all\12-11-25\v\Lib\site-packages\billiard\pool.py", line 406, in _ensure_messages_consumed
    if self.on_ready_counter.value >= completed:
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 3, in getvalue
PermissionError: [WinError 5] Access is denied
[2025-11-17 17:05:29,158: ERROR/MainProcess] Process 'SpawnPoolWorker-10' pid:199920 exited with 'exitcode 1'
[2025-11-17 17:05:30,376: INFO/SpawnPoolWorker-16] child process 200232 calling self.run()

        ('channel', 'Channel via Graph'),
    ]

    ticket = models.ForeignKey('timer.Ticket', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    recipient_email = models.EmailField(null=True, blank=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='graph_1to1')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    message_id = models.CharField(max_length=200, null=True, blank=True)
    response = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ticket.ticket_id if self.ticket else 'N/A'} -> {self.recipient_email} ({self.status})"
