
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# DB = SQLAlchemy()
# migrate = Migrate()

# # database class

# class Weed(DB.Model):
#     strain = DB.Column(DB.String, primary_key=True)
#     weed_type = DB.Column(DB.String(25))
#     rating = DB.Column(DB.Float, nullable=False)
#     effects = DB.Column(DB.String(100))
#     flavors = DB.column(DB.String(100))
#     description = DB.Column(DB.String(1000))


# here's a list of the flavors,effects and ailments in case we need them

# Flavors = ['Earthy', 'Sweet', 'Citrus', 'Pungent', 'Berry', 'Pine', 'Flowery', 'Woody',
#                'Spicy', 'Herbal', 'Lemon', 'Tropical', 'Blueberry', 'Grape',
#                'Orange', 'Pepper', 'Lime', 'Strawberry', 'Grapefruit', 'Sage',
#                'Minty', 'Pineapple', 'None', 'Lavender',  'Vanilla',  'Apple']

# Effects = ['Happy', 'Relaxed', 'Euphoric', 'Uplifted', 'Creative',
#                    'Sleepy', 'Energetic', 'Focused', 'Hungry', 'Talkative', 'Tingly',
#                    'Giggly', 'Aroused', 'None']

# Ailments = ['Depression', 'Inflammation', 'Insomnia', 'Lack of Appetite',
#                        'Muscle Spasms', 'Nausea', 'Pain', 'Seizures', 'Stress',
#                        'Anxiety', 'Headaches', 'Fatigue']