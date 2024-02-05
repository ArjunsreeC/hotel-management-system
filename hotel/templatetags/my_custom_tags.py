from django import template

register = template.Library()

@register.filter
def star_rating(rating):
    stars = '★' * int(rating)
    return stars
