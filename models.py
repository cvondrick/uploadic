import turkic.database
import turkic.models
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship, backref
import config

# a Job represents one task on mturk. it has a bunch of attributes and 
# meta data about the file it will store. in addition, there are a bunch of
# other properties that our mturk framework will handle for us.
class Job(turkic.models.HIT):
    __tablename__ = "jobs"
    __mapper_args__ = {"polymorphic_identity": "jobs"}

    id = Column(Integer, ForeignKey(turkic.models.HIT.id),
                primary_key = True)
    mimetype = Column(String(250))
    filename = Column(String(250))

    def getpage(self):
        return "?id={0}".format(self.id)

    @property
    def storepath(self):
        return "{0}/data/{1}-{2}".format(config.root, self.id, self.filename)

# a possible activity. this is really just storing a string to display later
# on to the user.
class Activity(turkic.database.Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key = True)
    text = Column(String(250))
    jobid = Column(Integer, ForeignKey(Job.id))
    job = relationship(Job, backref = backref("activities", 
                                              cascade = "all,delete"))
