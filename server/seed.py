from datetime import datetime
from app import app, db, bcrypt
from models import Wine, Review, User

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")

        # Optionally, clear existing data
        Wine.query.delete()
        Review.query.delete()
        User.query.delete()

        # Create user instances
        users = [
            User(username='Meredith2692'),  
            User(username='Kiana92')        
        ]
    
        users[0].password_hash = hash_password('password123')
        users[1].password_hash = hash_password('securepassword')

        db.session.add_all(users)   
        db.session.commit()

     
        meredith = users[0]
        kiana = users[1]

        # Seed wine data
        wines = [
            Wine(
                name='Shafer TD-9',
                type='Cabernet Sauvignon',
                flavor_profile='It fills the glass with irresistible aromas and flavors of fresh black cherries, black currant, red plum, thyme, rose petal, and cocoa. Lush and mouth-filling, this wine offers the kind of complexity and structure that ensures many years of enjoyment ahead',
                location='Sobo Liquors',
                price=89.0,
                viewed_at=datetime.utcnow(),
                image='https://www.winespectrum.com/wp-content/uploads/2024/11/S4597-1.png'
            ),
            Wine(
                name='2022 Auteur Sonoma Coast',
                type='Chardonnay',
                flavor_profile='Scents of lemon drops and lime leaves give way to a core of honeydew melon and baker’s yeast with a hint of brine.',
                location='Total Wine',
                price=39.0,
                viewed_at=datetime.utcnow(),
                image='https://www.winespectrum.com/wp-content/uploads/2024/12/A1662-1.png'
            ),
            Wine(
                name='NV Ayala ‘Majeur’ Brut',
                type='Sparkling/Champagne',
                flavor_profile='Medium to full body with a very creamy texture and a bright, vivid finish. Comes off dry.',
                location='Total Wine',
                price=69.0,
                viewed_at=datetime.utcnow(),
                image='https://www.winespectrum.com/wp-content/uploads/2024/10/A8943-1.png'
            ),
            Wine(
                name='The Paring',
                type='Sauvignon Blanc',
                flavor_profile='The nose is deliciously exotic, with lemon, melon and white peach soaring out of the glass.',
                location='Total Wine',
                price=29.0,
                viewed_at=datetime.utcnow(),
                image='https://www.winespectrum.com/wp-content/uploads/2024/12/P5732-1.png'
            ),
            Wine(
                name='Merry Edwards',
                type='Pinot Noir',
                flavor_profile='It’s ripe with notes of fresh black cherries, scorched earth, violets, and dark forest earth.',
                location='Total Wine',
                price=73.0,
                viewed_at=datetime.utcnow(),
                image='https://www.winespectrum.com/wp-content/uploads/2024/12/M8553-1.png'
            ),
            Wine(
                name='2015 Jean Vesselle ‘B3’',
                type='Sparkling/Champagne',
                flavor_profile='Persistent in its acidity, it feels a bit more austere and has a phenolic feel on the back.',
                location='Total Wine',
                price=95.0,
                viewed_at=datetime.utcnow(),
                image='https://www.winespectrum.com/wp-content/uploads/2024/08/J3733-1.png'
            ),
            Wine(
                name='Sixteen by Twenty',
                type='Cabernet Sauvignon',
                flavor_profile='Dark nose as well…dark, thick, black and red cherry with sweet mixed berries, currants and plum…none of these fruits dominates the other; it’s just a delightful mix of complexity.',
                location='Total Wine',
                price=60.0,
                viewed_at=datetime.utcnow(),
                image='https://www.winespectrum.com/wp-content/uploads/2024/12/S8374-1.png'
            ),
        ]
       
        # Add wines to session and commit
        db.session.add_all(wines)
        db.session.commit()

        # Seed reviews
        reviews = [
            Review(
                star_review=2,
                comment="Great Wine but hard to come by",
                wine_id=4,
                user_id=meredith.id  
            ),
            Review(
                star_review=4,
                comment="A great chardonnay for a great price",
                wine_id=2,
                user_id=meredith.id 
            ),
            Review(
                star_review=4,
                comment="Great Wine but hard to come by",
                wine_id=3,
                user_id=meredith.id 
            ),
            Review(
                star_review=3,
                comment="Great wine for a great price",
                wine_id=5,
                user_id=meredith.id 
            ),
            Review(
                star_review=4,
                comment="yum! a great wine for a great price",
                wine_id=1,
                user_id=meredith.id 
            ),
            Review(
                star_review=3,
                comment="I love this wine! Would recommend",
                wine_id=7,
                user_id=kiana.id  
            )
        ]

        # Add reviews to session and commit
        db.session.add_all(reviews)
        db.session.commit()

        print("Seeding completed.")
