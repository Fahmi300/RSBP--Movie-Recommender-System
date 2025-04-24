from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import requests

app = Flask(__name__)
CORS(app)


def fecth_poster(mov_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ddfa63b2b31dd8e658e5d4267e752a5f".format(mov_id)

    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    path="https://image.tmdb.org/t/p/w500/"+poster_path
    return path


    # headers = {
    #     "accept": "application/json",
    #     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZGZhNjNiMmIzMWRkOGU2NThlNWQ0MjY3ZTc1MmE1ZiIsIm5iZiI6MTczMzc3MTcxMi4yNDcsInN1YiI6IjY3NTc0MWMwZjMxZGM4Y2U4OGZkYTg0YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NKJXuG_0B2G3Iu9QlZ3vL25Hdg8UgS81l4-gu4eXoNw"
    # }
    # response = requests.get(url, headers=headers)

    # print(response.text)


@app.route('/recommend', methods=['POST'])
def recommend():

    data = request.get_json()
    movie = data.get('movie', '')

    with open('movies_list.pkl', 'rb') as file:
        loaded_movies = pickle.load(file)
    
    with open('similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)

    movie_recommend=[]

    movie_index = loaded_movies[loaded_movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]: 
        recommend_id = loaded_movies.iloc[i[0]].movie_id

        recommended_title = loaded_movies.iloc[i[0]].title
        movie_recommend.append({
            "title": recommended_title, 
            "poster": fecth_poster(recommend_id)
        })
    
    print(jsonify(movie_recommend))
    return jsonify(movie_recommend)




if __name__ == '__main__':
    app.run(debug=True)
