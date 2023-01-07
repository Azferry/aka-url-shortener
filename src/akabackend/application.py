from app import create_app
import sys
import os
sys.path.insert(0, os.getcwd())
application = create_app()

if __name__ == '__main__':
  application.run()


# Add logging for start up (what are the env set to, steps in the procrcess )