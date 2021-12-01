from .node_interface import NodeInterface
from Neo4jDriver.settings import *
from Neo4jDriver.db_thread import DBThread
from geopy.distance import geodesic
from datetime import datetime

import json

from neomodel import (config, StructuredNode, StringProperty ,JSONProperty, DateTimeProperty,
    UniqueIdProperty, Relationship)
from neomodel.contrib.spatial_properties import NeomodelPoint, PointProperty
from neomodel.cardinality import ZeroOrOne

#config.DATABASE_URL = bolt_url

class BlueFinWhalesModel (StructuredNode):
    guid = UniqueIdProperty()
    eventId = StringProperty()
    timestamp = DateTimeProperty(default_now=False)
    json = JSONProperty()
    location = PointProperty(crs='wgs-84')
    timeNear = Relationship('BlueFinWhalesModel', 'WITHIN_DAY')
    spaceNear = Relationship('BlueFinWhalesModel', 'WITHIN_5_MILES')


class BlueFinWhales (NodeInterface):
    model = BlueFinWhalesModel
    def load_csv(self, jsonArray):
        whale_point_list = []
        # Either create new node or just add it to the list
        for jsonPoint in jsonArray:
            already = self.model.nodes.get_or_none(eventId=jsonPoint['event-id'])
            if already is not None:
                whale_point_list.append(already)
                # remove existing relationships should they exist
                already.spaceNear.disconnect_all()
                already.timeNear.disconnect_all()
                continue
            else:
                new_whale_point = self.model()

            # Create new node
            new_whale_point.eventId = jsonPoint['event-id']
            new_whale_point.timestamp = datetime.strptime(jsonPoint['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            new_whale_point.json = json.dumps(jsonPoint)
            new_whale_point.location = NeomodelPoint((jsonPoint['location-long'], jsonPoint['location-lat']), crs='wgs-84')
            new_whale_point.save()
            whale_point_list.append(new_whale_point)
        
        # After we have a list of all the nodes set the relationships
        for point in whale_point_list:
            self.make_relationships(point, whale_point_list )

    def distance(self, point1, point2):
        coords1 = (point1.location.latitude, point1.location.longitude)
        coords2 = (point2.location.latitude, point2.location.longitude)
        return  geodesic(coords1, coords2).miles

    def make_relationships(self, point, set):
        closest = None
        second = None
        closest_dist = 0
        second_dist = 0
        for subpoint in set:
            if point.eventId != subpoint.eventId:
                if(closest is None and second is None):
                    closest = second = subpoint
                    closest_dist = second_dist = self.distance(point, subpoint)
                    continue
                dist = self.distance(point, subpoint)
                if dist <= closest_dist:
                    second = closest
                    second_dist = closest_dist
                    closest = subpoint
                    closest_dist = dist
                elif dist <= second_dist:
                    second = subpoint
                    second_dist = dist
        
        point.spaceNear.connect(closest)
        point.spaceNear.connect(second)
        