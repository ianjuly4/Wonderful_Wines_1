from flask import request, session, make_response
from flask_restful import Resource
from config import app, db, Api, CORS, Migrate, bcrypt
from models import Wine, Review, User


app.secret_key = "b'\x1f\r\xa4\xfa\x1f\x17\xf6?\r\x90@\xb0\x1d\x0c\xbb\xc2'"

CORS(app, origins='http://localhost:3000/wines')
migrate = Migrate(app, db)
api = Api(app)


class Index(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Wonderful Wines RESTful API",
        }
        response = make_response((response_dict), 200)
        return response

api.add_resource(Index, '/')


class Wines(Resource):
    def get(self):

        wine_dict_list = [wine.to_dict() for wine in Wine.query.all()]

        if wine_dict_list:
            return (wine_dict_list, 200)
        else:
            return({"message": "No Wines Found"}, 404)

    def post(self):
        
        data = request.get_json()
        print("Request Data:", data)
        user_id = session.get('user_id')
        if not user_id:
            return make_response({"message": "Unauthorized, Please Login to Continue"}, 401)
        else:
            new_wine = Wine(
                name=data.get('name', ''),
                type=data.get('type', ''),
                location=data.get('location', ''),
                price=data.get('price', 0),
                flavor_profile=data.get('flavorProfile', ''),
                image=data.get('image')
            )
            db.session.add(new_wine)
            db.session.commit()

            new_review = Review(
                wine_id=new_wine.id,
                user_id=user_id,
                star_review=data.get('rating', ''),
                comment=data.get('comment','')

            )
            db.session.add(new_review)
            db.session.commit()

            response_data = {
                "wine": new_wine.to_dict(),
                "review": new_review.to_dict()
            }

        
            return make_response(response_data, 201)
   

api.add_resource(Wines, '/wines')

class WinesById(Resource):
    def get(self, id):
        response_dict = Wine.query.filter(Wine.id==id).first().to_dict()
        response = make_response(
            response_dict,
            200,
        )
        return response
    def delete(self, id):
        wine = Wine.query.filter(Wine.id == id).first()
        if not wine:
            return make_response({"error": "Wine not found"}, 404)
        db.session.delete(wine)
        db.session.commit()
        return make_response({"message": "Wine successfully deleted"}, 200)
    def patch(self, id):
        data = request.get_json()
        wine = Wine.query.filter(Wine.id == id).first()
        print(data)
        if not wine:
            return make_response({"error": "Wine not found"}, 404)
        try:
            for attr in data:
                if hasattr(wine, attr):
                    setattr(wine, attr, data[attr])
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response({"error": str(e)}, 400)
        response_dict = wine.to_dict()
        response = make_response(
            response_dict,
            200
        )
        return response
api.add_resource(WinesById, "/wines/<int:id>")


class Reviews(Resource):
    
    def post(self, id):
       
        data = request.get_json()
        print("Request Data:", data)

        wine = Wine.query.filter(Wine.id == id).first()

       
        if not wine:
            return make_response({"message": "Wine not found"}, 404)

        
        user_id = session.get('user_id')
        if not user_id:
            return make_response({"message": "Unauthorized, Please Login to Continue"}, 401)

        
        new_review = Review(
            user_id=user_id,
            wine_id=wine.id, 
            comment=data.get('comment', ''),
            star_review=data.get('star_review', '') 
        )

       
        db.session.add(new_review)
        db.session.commit()

        return make_response(new_review.to_dict(), 201)  
    
    def get(self, id):

        response_dict = Review.query.filter(Review.id==id).first().to_dict()

        response = make_response(
            response_dict,
            200,
        )

        return response
    
    def delete(self, id):

        review = Review.query.filter(Review.id == id).first()

        db.session.delete(review)
        db.session.commit()

        response_dict = {"message": "review successfully deleted"}

        response = make_response(
            response_dict,
            200
        )

        return response
    
    def patch(self, id):
        data = request.get_json()
        print("Received data:", data)  

        review = Review.query.filter(Review.id == id).first()

        if not review:
            return make_response({"message": "Review not found"}, 404)

        for attr, value in data.items():
            print(f"Setting {attr} = {value}") 
            setattr(review, attr, value)

        db.session.commit()

        response_dict = review.to_dict()

        return make_response(response_dict, 200)


    
    
api.add_resource(Reviews, '/reviews/<int:id>')


class Signup(Resource):

    def post(self):
        data = request.get_json()
        print(data)

        if not data:
            return make_response({"message": "Invalid data. No data provided."}, 400)
        
        username = data.get('username')
        password = data.get('password')
       
        if not username or not password:
            return make_response({"message": "Username and password are required."}, 422)
        
        user = User.query.filter(User.username == username).first()
        if user:
            return make_response({"message": "Username already taken."}, 422)

        new_user = User(
            username=username,
        )
        new_user.password_hash = password  

        db.session.add(new_user)
        db.session.commit()

        
        new_user_dict = new_user.to_dict()

        return make_response(new_user_dict, 201)
    
    
api.add_resource(Signup, "/signup")

class Login(Resource):
    def post(self):
        data = request.get_json()  
        username = data['username']
        password = data['password']
       
        user = User.query.filter(User.username==username).first()  
        
        if user and user.authenticate(password):
            session['user_id'] = user.id
            user_dict = user.to_dict()
            response = make_response(
                {'message': 'Login successful', 'user': user_dict}, 200
            )
            return response
        
        else:
            response = make_response(
                {'error': 'Invalid username or password'}, 401
            )
            return response
               
api.add_resource(Login, '/login')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        response  = make_response({'message': 'Logged out successfully'},200 )
        return response

api.add_resource(Logout, '/logout')

class CheckSession(Resource):
    def get(self):
        print(f"Session content: {session}")
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            user_dict = user.to_dict()
            return make_response(
                user_dict,
                200
            )
        else:
            return {"message":"No user currently logged in"}, 401

api.add_resource(CheckSession, '/check_session')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

