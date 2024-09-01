import pyshorteners as py

def RecortadorURL(url_largo):
    s=py.Shortener()
    url_acortado=s.tinyurl.short(url_largo)
    return url_acortado