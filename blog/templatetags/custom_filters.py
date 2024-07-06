from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def adjust_image_sizes(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    for img in images:
        # Adjust width and height attributes as needed
        width = int(img.get('width', 0))
        height = int(img.get('height', 0))
        new_width = width * 0.5  # Example resizing logic
        new_height = height * 0.5  # Example resizing logic
        img['width'] = new_width
        img['height'] = new_height
    return str(soup)