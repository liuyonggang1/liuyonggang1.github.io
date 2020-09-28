from browser import document, window

stem = window.location.pathname.split('/')[-1].replace('.html', '')
document['zone_head'] <= document.title
exec (f"import {stem}.{stem}")

