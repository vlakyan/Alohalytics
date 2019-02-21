from pyaloha.event import DictEvent, Event


class RouteDictEvent(DictEvent):
    mode_alliases = {
        'astar-bidirectional-pedestrian': 'pedestrian',
        'astar-bidirectional-bicycle': 'bicycle',
        'astar-bidirectional-car': 'vehicle',
        'pedestrian': 'pedestrian',
        'bicycle': 'bicycle',
        'vehicle': 'vehicle',
        'mixed-car': 'vehicle',
        'astar-bidirectional-transit': 'transit',
        'subway': 'transit'
    }

    def __init__(self, *args, **kwargs):
        super(RouteDictEvent, self).__init__(*args, **kwargs)
        mode = self.data.get('router', self.data.get('name', None)).lower()
        self.mode = self.mode_alliases.get(mode, mode)


# ALOHA: Routing_CalculatingRoute [
#   distance=51797.4 elapsed=6.56531
#   finalLat=49.45913 finalLon=35.11263
#   name=vehicle result=NoError
#   startDirectionX=0 startDirectionY=0
#   startLat=49.55215 startLon=34.52105
# ]
#
# Event for route creation with specific props:
# mode: {'vehicle', 'pedestrian'}
# start: (lat, lon)
# destination: None or (lat, lon)
# status: {None, 'NoError', 'Cancelled'}
# distance:

class RouteRequest(RouteDictEvent):
    keys = (
        'Routing_CalculatingRoute',
    )

    def __init__(self, *args, **kwargs):
        super(RouteRequest, self).__init__(*args, **kwargs)

        self.start = self.user_info.get_location() or (
            self.data['startLat'], self.data['startLon']
        )

        try:
            self.destination = (
                self.data['finalLat'], self.data['finalLon']
            )
        except KeyError:
            self.destination = None

        self.status = self.data.get('result')
        self.distance = self.data.get('distance')

# Event for a start of the route with specific props
# with no specific fields
# Android: Routing. Start []
# iOS: Point to point Go [
# Country = 'AR'
# Language = 'ru-UA'
# Orientation = 'Portrait'
# Value: {'From my position', 'Point to point', 'To my position'}
# ]

class RouteStart(Event):
    keys = (
        'Routing. Start',
        'Point to point Go',
    )


# ALOHA: RouteTracking_RouteClosing [
#   distance=513244 percent=0.197765
#   rebuildCount=0 router=vehicle
# ] <utc=0,lat=44.4369109,lon=8.9513113,acc=1.00>
#
# ALOHA: RouteTracking_ReachedDestination [
#   passedDistance=3.1224
#   rebuildCount=0 router=vehicle
# ]

class RouteEnd(RouteDictEvent):
    keys = (
        'RouteTracking_RouteClosing',
        'RouteTracking_ReachedDestination'
    )

    def __init__(self, *args, **kwargs):
        super(RouteEnd, self).__init__(*args, **kwargs)

        try:
            self.rebuild_count = int(self.data['rebuildCount'])
        except KeyError:
            self.rebuild_count = None

        self.distance_done = self.data.get(
            'distance', self.data.get('passedDistance', None)
        )

        self.percent = float(self.data.get('percent', 100))


# ALOHA: RouteTracking_PercentUpdate [
#   percent=75.3459
# ] <utc=0,lat=-9.9709619,lon=-67.8104598,acc=1.00>

class RouteTracking(RouteDictEvent):
    keys = (
        'RouteTracking_PercentUpdate',
    )

    def __init__(self, *args, **kwargs):
        super(RouteTracking, self).__init__(*args, **kwargs)

        self.percent = float(self.data.get('percent', 100))

# ALOHA: Routing_Build_Taxi [ provider=Uber ]
# Event send, when user calculate route on taxi with specific property
# provider = {'Uber', 'Yandex'}


class TaxiRouteRequest(DictEvent):
    keys = (
        'Routing_Build_Taxi',
    )

    def __init__(self, *args, **kwargs):
        super(TaxiRouteRequest, self).__init__(*args, **kwargs)
        self.mode = 'taxi'
        self.provider = self.data.get('provider', 'Unknown')


# ALOHA: $TrafficChangeState [ state=WaitingData ]
# Event send, when user turned on/off traffic jams


class TrafficState(DictEvent):
    keys = (
        '$TrafficChangeState',
    )

    def __init__(self, *args, **kwargs):
        super(TrafficState, self).__init__(*args, **kwargs)
        self.state = self.data.get('state', 'Unknown')


# Event send, when user click on bookmark button after build route
# or after start planning route
# ALOHA:
# ios: Routing_Bookmarks_click [
# Country=IQ
# Language=ar-IQ
# Orientation=Portrait
# mode=planning
# ]
# android: Routing_Bookmarks_click [
# mode=onroute
# ]


class RoutingBookmarksClick(DictEvent):
    keys = (
        'Routing_Bookmarks_click',
    )

    def __init__(self, *args, **kwargs):
        super(RoutingBookmarksClick, self).__init__(*args, **kwargs)
        self.mode = self.data.get('mode')


# Event send, when user added point to route. It can be from placepage
# or on planning page
# ALOHA:
# ios: Routing_Point_add [
# Country=PK
# Language=en-PK
# Orientation=Portrait
# method: {'planning_pp', 'outside_pp'}
# mode: {'planning', 'onroute', None}
# type: {'start', 'finish', 'inner'}
# value: {'gps', 'point'}
# ]
#
# android: Routing_Point_add [
# method: {'planning_pp', 'outside_pp'}
# mode: {'planning', 'onroute', None}
# type: {'start', 'finish', 'inner'}
# value: {'gps', 'point'}
# ]


class RoutingPointAdd(DictEvent):
    keys = (
        'Routing_Point_add',
    )

    def __init__(self, *args, **kwargs):
        super(RoutingPointAdd, self).__init__(*args, **kwargs)
        self.mode = self.data.get('mode', 'onroute')
        self.method = self.data.get('method', 'outside_pp')
        self.type = self.data.get('type', 'unknown')
        self.value = self.data.get('value', 'unknown')


# Event send, when user click on search button after build route
# or after start planning route
# ALOHA:
# ios: Routing_Search_click [
# Country=PK
# Language=en-PK
# Orientation=Portrait
# mode: {'planning', 'onroute'}
# ]
#
# android: Routing_Search_click [
# mode: {'planning', 'onroute'}
# ]


class RoutingSearch(DictEvent):
    keys = (
        'Routing_Search_click',
    )

    def __init__(self, *args, **kwargs):
        super(RoutingSearch, self).__init__(*args, **kwargs)
        self.mode = self.data.get('mode', 'onroute')