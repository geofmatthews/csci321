from pygame.locals import *

class PLAYER:
    SIZE = 32
    COLOR = (255, 100, 0)
    CONTROLS = [K_UP, K_LEFT, K_DOWN, K_RIGHT, K_RCTRL]
    GROUND_ACCELERATION = 700
    AIR_ACCELERATION = 150
    JUMP_ACC = 250
    MAX_AIR_SPEED = 180
    MAX_GROUND_SPEED  = 200
    BRAKE_ACC = 600
    TURN_SPEED = 40
    TURN_RATIO = 5
    BOOST_RATIO = 0.07
    MOVE_FRAME_SPEED = 25 # frames per second
    EYE_FRAME_SPEED = 15
    MOVE_FRAMES = 7
    EYE_FRAMES = 10
    VACUUM_TIME = 5000
    
class PLANET:
    POINT_DISTANCE = 80

class SCREEN:
    WIDTH = 800
    HEIGHT = 600
    
class STAR:
    RADIUS = 20
    D_ANGLE = 60
    D_D_ANGLE = 30
    DECAY_D_D_ANGLE = 10
    DECAY_TIME = 2000
    PULSE_TIME = 500
    
class PLATFORM:
    BORDER = 15
    IMAGE_HEIGHT = 58
    SIDE_GAP = 11
    MIDDLE_WIDTH = 10
    MIN_ANGLE = 60
    MAX_ANGLE = 300

class FLAG:
    RADIUS = 30
    CHANGE_TIME = 250
    FRAMES = 6
    
class BOOSTER:
    FRAMES = 17
    FRAME_SPEED = 30
    
class CAMERA:
    WIDTH = 80
    HEIGHT = 60
    RADIUS = 50
    OFFSET = 40
    RECT_OFFSET = 400
    DELAY_RATIO = 0.3
    SHAKE_DURATION = 800
    SHAKE_THRESHOLD = 360
    SHAKE_RATIO = 0.1
    
class MONSTER:
    TYPE_ANGLE = 'a'
    TYPE_PLATFORM = 'p'
    class Q:
        PAUSE = 500
        SPEED = 150
        RADIUS = 24
        MOVE_FRAMES = 2
        MOVE_FRAME_SPEED = 10 # frames per second
        BULLET_RADIUS = 4
        BULLET_SPEED = 300
        SHOOT_ANGLE = 135
        SHOOT_TIME_FROM = 500
        SHOOT_TIME_TO = 4000
        CADENCE = 20
    class C:
        PAUSE = 500
        SPEED = 50
        RADIUS = 16
        MOVE_FRAMES = 7
        MOVE_FRAME_SPEED = 15 # frames per second
        RELOAD_FRAMES = 12
        RELOAD_FRAME_SPEED = 13
        SHOOT_FRAME = 3
        BULLET_FRAMES = 4
        BULLET_FRAME_SPEED = 15
        MOVING = 1
        SHOOTING = 2
        BULLET_RADIUS = 8
        BULLET_SPEED = 200
    class O:
        PAUSE = 500
        SPEED = 100
        RADIUS = 16
        MOVE_FRAMES = 3
        EYE_FRAMES = 6
        MOVE_FRAME_SPEED = 20 # frames per second
        EYE_FRAME_SPEED = 10
        KEEP_NORMAL = 8 # fps, how long to stay with normal eyes
    class I:
        PAUSE = 1500
        SPEED = 100
        RADIUS = 16
        JUMPING = 1
        PREPARING = 2
        JUMP_SPEED = 450
        JUMP_ACC = 700
        FRAME_SPEED = 40
        FRAMES = 10
    class EYE:
        RADIUS = 10
        FRAME_SPEED = 20
        FRAMES = 10
        LINE_LENGTH = 30
        
STORY = {'menu.txt': [["Aaaarghhh!"],
                      ["Oh Jesus, what happened?!"],
                      ["The last thing that i remember",
                       "was the end of Xo-space...",
                       "I guess i am lucky to be alive"],
                      ["Damn it! My ship is wrecked,",
                       "torn apart! I have to fix it",
                       "as soon as i can..."],
                      ["Well u could ask me,",
                       "why am i here?"],
                      ["I Can't tell you, orders..."],
                      ["The little that i can say is,",
                       "that i am Xoxoan, i live on",
                       "planet XoXoa and i am a pilot."],
                      ["I always wanted to fly... so i",
                       "took this job and... well i was",
                       "happy."],
                      ["So i suppose, that there is",
                       "no other way than searchin'",
                       "parts of my ship."],
                      ["Wait a minute... That means",
                       "that i have to search",
                       "everywhere?!!"],
                      ["For God's sake, i do not",
                       "deserve this!"],
                      ["One day, you are flying in",
                       "a space ship, everythin's",
                       "allright, feet on the table,",
                       "hot xoxola, funny movie and..."],
                      ["BAM! All is gone!", "", "...", "", 
                       "Let's get to work..."]],
      'level01.txt': [["So it seems like this planet",
                       "is called moon. What a weird",
                       "name..."],
                      ["I remember we once learned about",
                       "something.. No! I hope I'm wrong."],
                      ["It was very small planet with",
                       "something like hundred moons."],
                      ["That would mean I must search",
                       "hundred moons?? At least I hope",
                       "it's all save around here..."],
                      ["Hey, what the heck is that??!"]],
      'level02.txt': [["I gotta be home.. What am I",
                       "doin' here? Why is it eyes",
                       "everywhere?"],
                      ["At least I've found anything.",
                       "Still it would make a ship in a",
                       "light year..."],
                      ["I heard some rumors about geysirs",
                       "in this area of space. Well, that",
                       "could come handy!"]],
      'level03.txt': [["Seven hells, what is this?",
                       "Hmph, maybe some kind of",
                       "very rare chewing gum..."],
                      ["Opps! Well, pink color - check,",
                       "but that eye...",
                       "That big eye...",
                       "It's gonna haut me...",
                       "for rest of my days"],
                      ["No, no, no.",
                      " You have to be optimist!",
                       "If i could,...",
                       "i would"]],
      'level04.txt': [["Am i drunk?",
                       "Weird hedgehogs",
                       "Damn fast!!!"],
                      ["I should better",
                       "run, run, run",
                       "If i could,...",
                       "i would"]],
      'level05.txt': [["Eyes flying...",
                       "everywhere",
                       "I got hands!",
                       "No, i don't"],
                      ["Spare my life!",
                       "And let me collect",
                       "parts of",
                       "my ship!"]],
      'level06.txt': [["Gatling..",
                       "guns",
                       "No, thanks"],
                      ["May the force...",
                       "be with me",
                       ]]
        }
                      

#
#One day, you are flying in space ship, all is allright, feet on the table, hot xoxola, funny movie and BAM!
#All is gone!
#Let's get to work...