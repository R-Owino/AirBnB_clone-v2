#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models.city import City
from models.amenity import Amenity
from models.review import Review
from os import getenv
from models import *

if getenv("HBNB_TYPE_STORAGE") == "db":
    association_table = Table('place_amenity', Base.metadata,
                              Column('place_id',
                                     String(60),
                                     ForeignKey('places.id'),
                                     primary_key=True,
                                     nullable=False),
                              Column('amenity_id',
                                     String(60),
                                     ForeignKey('amenities.id'),
                                     primary_key=True,
                                     nullable=False))


class Place(BaseModel, Base):
    """Representation of Place """
    __tablename__ = 'places'
    city_id = Column(String(60),
                     ForeignKey("cities.id"),
                     nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id'),
                     nullable=False)
    name = Column(String(128),
                  nullable=False)
    description = Column(String(1024), default="NULL",
                         nullable=True)
    number_rooms = Column(Integer,
                          default=0,
                          nullable=False)
    number_bathrooms = Column(Integer,
                              default=0,
                              nullable=False)
    max_guest = Column(Integer,
                       default=0,
                       nullable=False)
    price_by_night = Column(Integer,
                            default=0,
                            nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship("Review", cascade="all, delete",
                           backref="place")
    amenities = relationship("Amenity",
                             secondary="place_amenity",
                             back_populates="place_amenities",
                             viewonly=False)

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """attribute that returns list of Review instances"""
            values_review = models.storage.all("Review").values()
            list_review = []
            for review in values_review:
                if review.place_id == self.id:
                    list_review.append(review)
            return list_review

        @property
        def amenities(self):
            """attribute that returns list of Amenity instances"""
            values_amenity = models.storage.all("Amenity").values()
            list_amenity = []
            for amenity in values_amenity:
                if amenity.place_id == self.id:
                    list_amenity.append(amenity)
            return list_amenity

        @amenities.setter
        def amenities(self, value):
            """Setter method for amenities"""
            if (type(value) == Amenity):
                self.amenity_ids.append(value.id)
