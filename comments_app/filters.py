from django.db.models import Case, When, Value, IntegerField

from .models import Comment
from django_filters import rest_framework as filters


class CommentFilter(filters.FilterSet):
    username = filters.CharFilter(method='filter_by_username')
    email = filters.CharFilter(method='filter_by_email')
    created_at = filters.ChoiceFilter(
        label='Created At Order',
        choices=[('fifo', 'FIFO'), ('lifo', 'LIFO')],
        method='filter_by_created_at'
    )

    class Meta:
        model = Comment
        fields = ['username', 'email', 'created_at']

    def filter_by_created_at(self, queryset, name, value):
        order_by_fields = ['created_at'] if value == 'fifo' else ['-created_at']

        if 'is_priority' in queryset.query.annotations:
            order_by_fields.insert(0, 'is_priority')

        return queryset.order_by(*order_by_fields)

    def filter_by_username(self, queryset, name, value):
        priority_queryset = queryset.annotate(
            is_priority=Case(
                When(user__username__icontains=value, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        return self.filter_by_created_at(priority_queryset, name, value)

    def filter_by_email(self, queryset, name, value):
        priority_queryset = queryset.annotate(
            is_priority=Case(
                When(user__email__icontains=value, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        return self.filter_by_created_at(priority_queryset, name, value)