from .models import Comment
from django_filters import rest_framework as filters


class CommentFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    email = filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    # created_at = filters.DateTimeFilter(field_name='created_at', lookup_expr='exact')
    created_at = filters.ChoiceFilter(
        label='Created At Order',
        choices=[('fifo', 'FIFO'), ('lifo', 'LIFO')],
        method='filter_by_created_at'
    )

    class Meta:
        model = Comment
        fields = ['username', 'email', 'created_at']

    def filter_by_created_at(self, queryset, name, value):
        if value == 'fifo':
            return queryset.order_by('created_at')
        elif value == 'lifo':
            return queryset.order_by('-created_at')
        return queryset
