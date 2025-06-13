from django import template
from task_profiler.utils import convert_slack_timestamp as convert_slack_timestamp_util

register = template.Library()

@register.filter
def convert_slack_timestamp(value):
    return convert_slack_timestamp_util(value)