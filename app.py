import os
from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_NAME = os.environ.get("MONGODB_NAME")

app = Flask(__name__)

@app.route('/')
def get_index():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def do_login():
    username = request.form['username']
    return redirect(username)

@app.route("/<username>") 
def get_userpage(username):
    return render_template("index.html", username=username)
    
@app.route("/<username>/get_collections")
def get_collections(username):
     user_lists = load_lists_by_username(username)
     return render_template('collections.html', username=username, user_lists=user_lists)  

@app.route("/<username>/create_new_list", methods=["POST"]) 
def create_list(username):
    collection_name= request.form['collection_name']
    create_list_for_user(username,collection_name)
    return redirect(username + "/get_collections")
    
# @app.route('/delete_category/<category_id>')
# def delete_category(category_id):
#     mongo.db.categories.remove({'_id': ObjectId(category_id)})
#     return redirect(url_for('get_categories'))

# @app.route('/edit_category/<category_id>')
# def edit_category(category_id):
#     return render_template('editcategory.html',
#     category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

    
@app.route("/<username>/<collection_name>") 
def view_list_by_user(username, collection_name):
    list_items = load_list_items_from_mongo(username, collection_name)
    return render_template("collection_items.html", username=username, collection_name=collection_name, list_items=list_items)
    
@app.route("/<username>/<collection_name>/add_item", methods=["POST"]) 
def add_item_to_list(username, collection_name):
    list_item= request.form['list_item']
    description= request.form['description']
    future_log= ""
    priority = 1
    task_type = ""
    unique_id = 1
#    unique_id = find_the_max_id(username.collection_name)
    
    dict2 = {"id": unique_id, "list_item": list_item, "description" : description, "future_log": future_log, "priority": priority, "task_type": task_type}
    save_list_items_to_mongo(username, collection_name, dict2)
    return redirect(username + "/" + collection_name)


#---------------------------------------------------------------------------------------------
    
def create_list_for_user(username, collection_name):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        db[username].insert({'name': collection_name, 'list_items': [] })

# def delete_list_for_user(username, collection_name):
#     with MongoClient(MONGODB_URI) as conn:
#         db = conn[MONGODB_NAME]
#         db[username].delete({'name': collection_name, 'list_items': [] })
        
def load_lists_by_username(username):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        return db[username].find()

def save_list_items_to_mongo(username, collection_name, new_list_item):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        selected_list = db[username].find_one({'name':collection_name})
        selected_list['list_items'].append(new_list_item)
        db[username].save(selected_list)

def load_list_items_from_mongo(username, collection_name):
    with MongoClient(MONGODB_URI) as conn:
        db = conn[MONGODB_NAME]
        return db[username].find({'name':collection_name})

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)