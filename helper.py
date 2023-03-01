
import os


from RasaHost import host
host.nlu_path = os.path.join("hybrid", "data/nlu/")
host.stories_path = os.path.join("hybrid", "data/stories/")
host.domain_path = os.path.join("hybrid", "data/domain.yml")
if __name__ == '__main__':    
    host.run()