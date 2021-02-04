from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param, remove_query_param
from app import constants
import decimal, datetime, math

def getdict(o):
    dic = {}
    
    if o is None:
        return None
    
    for k, v in o.__dict__.items():
        if isinstance(v, decimal.Decimal):
            dic[k] = float(v)
            
        elif isinstance(v, datetime.datetime):
            dic[k] = str(v)
            
        else:
            dic[k] = v
            
    return dic

class UIException(Exception):
    pass

class SortOrder(object):
    ASC = 'asc'
    DESC = 'desc'
    
class Sort(object):
    
    def __init__(self, fieldname, order):
        self.fieldname = fieldname
        self.order = order

    @classmethod
    def from_request(cls, req, defaultfield, map={}):
        s = req.GET.get('sort')
        if s in [None, '']:
            sort = cls(defaultfield, SortOrder.ASC)
            return (str(sort),)

        lis = s.split('$')
        sorts = []
        for k in lis:
            arr = k.split(':')
            fname = arr[0]
            if fname in map:
                fname = map[fname]

            sort = cls(fname, arr[1])
            sorts.append(str(sort))

        return tuple(sorts)

    def __str__(self):
        r = self.fieldname
        if self.order == SortOrder.DESC:
            r = '-{0}'.format(r)

        return r

class JsonModel(object):
    
    def tojson(self):
        return getdict(self)

class ListResultsSetPagination(PageNumberPagination):
    page_size_query_param = '_limit'
    page_query_param = '_page'
    max_page_size = 1000

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        page_number = 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)

    @property
    def headers(self):
        links = []
        firstlink = self.get_first_link()
        prevlink = self.get_previous_link()
        nextlink = self.get_next_link()
        lastlink = self.get_last_link()

        links.append('<{0}>; rel="first"'.format(firstlink))

        if prevlink is not None:
            links.append('<{0}>; rel="prev"'.format(prevlink))

        if nextlink is not None:
            links.append('<{0}>; rel="next"'.format(nextlink))

        links.append('<{0}>; rel="last"'.format(lastlink))

        headers = {
            'link': ', '.join(links),
            'x-total-count': self.page.paginator.count,
            'x-total-pages': self.page.paginator.num_pages,
            'access-control-expose-headers': constants.DEFAULT_HEADERS
        }
        
        return headers
    
class Pager(JsonModel):
    
    def __init__(self, total, pagenum, pagesize):
        self.total = total
        self.pagenum = pagenum
        self.setpagesize(pagesize)
        
    def tojson(self):
        m = super(Pager, self).tojson()
        m['pagenum'] = self.pagenum
        m['pagesize'] = self.pagesize
        m['total'] = self.total
        m['lowerbound'] = self.lowerbound
        m['upperbound'] = self.upperbound
        m['hasnext'] = self.hasnext
        m['hasprev'] = self.hasprev
        m['totalpages'] = self.totalpages
        return m

    @property
    def pagesize(self):
        return self._pagesize
    
    @pagesize.setter
    def pagesize(self, v):
        self.setpagesize(v)
        
    @property
    def startrow(self):
        if self.pagenum == 1:
            return (self.pagenum - 1) * self.pagesize
        
        return ((self.pagenum - 1) * self.pagesize) + 1
    
    @property
    def endrow(self):
        return self.upperbound
        
    @property
    def lowerbound(self):
        return (self.pagenum - 1) * self.pagesize
    
    @property
    def upperbound(self):
        upperbound = self.pagenum * self.pagesize
        
        if self.total < upperbound:
            upperbound = self.total
            
        return upperbound
    
    @property
    def hasnext(self):
        return True if self.total > self.upperbound else False
    
    @property
    def hasprev(self):
        return True if self.lowerbound > 0 else False
        
    @property
    def totalpages(self):
        return int(math.ceil(self.total / float(self.pagesize)))

    def setpagesize(self, pagesize):
        if (self.total < pagesize or pagesize < 1) and self.total > 0:
            self._pagesize = self.total
            
        else:
            self._pagesize = pagesize
            
        if self.totalpages < self.pagenum:
            self.pagenum = self.totalpages
            
        if self.pagenum < 1:
            self.pagenum = 1
    