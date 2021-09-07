from django.contrib import admin

from .models import Tag, IssueStatus, IssuePriority, IssueType, Project, Issue, IssueComment

admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(IssueStatus)
admin.site.register(IssuePriority)
admin.site.register(IssueType)
admin.site.register(IssueComment)

