import config
from turkic.cli import handler, Command, LoadCommand, importparser
from turkic.database import session
import turkic.models
from models import *
import argparse

# this command will load a new set of jobs into the system:
#
# $ turkic create "Wash dishes" "Walk the dog" "Eat food" --number 10
@handler("Adds a new set of actions")
class create(LoadCommand):
    def setup(self):
        parser = argparse.ArgumentParser(parents = [importparser])
        parser.add_argument("activities", nargs="+")
        parser.add_argument("--number", "-n", type = int, default = 1)
        return parser

    def title(self, args):
        return "Upload a video of you performing activities"

    def description(self, args):
        return "Create a video of you performing certain activities."

    def cost(self, args):
        return 0.50

    def keywords(self, args):
        return "video, upload, create, you, film"

    def lifetime(self, args):
        return 1209600

    def duration(self, args):
        return 7200 * 3

    def __call__(self, args, group):
        if args.number < 1:
            print "error: number must be >= 1"
            return

        for _ in range(args.number):
            job = Job(group = group)
            session.add(job)

            for activity in args.activities:
                activity = Activity(text = activity, job = job)
                session.add(activity)

        session.commit()

        if args.number == 1:
            print "Created 1 job."
        else:
            print "Created {0} jobs.".format(args.number)

# this simply dumps all videos with their associated activities
@handler("Dump all the data")
class dump(Command):
    def setup(self):
        parser = argparse.ArgumentParser()
        return parser

    def __call__(self, args):
        query = session.query(Job).filter(turkic.models.HIT.completed == True)
        for job in query:
            print job.storepath
            print job.mimetype
            for activity in job.activities:
                print activity.text
            print ""
