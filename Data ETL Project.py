import pandas as pd
import matplotlib.pyplot as plt

#Extract
def extract(file_path):
    return pd.read_csv(file_path)

#Transform
def transform(data):
    #Average IMDB rating and total box office by genre
    genre_stats = data.groupby('Genre').agg({
        'IMDB_Rating': 'mean',
        'Box_Office_Millions': 'sum'
    }).reset_index()
    genre_stats.rename(columns={
        'IMDB_Rating': 'Avg_Rating',
        'Box_Office_Millions': 'Total_Box_Office'
    }, inplace=True)
    
    # Find top-rated movie
    top_rated = data.loc[data['IMDB_Rating'].idxmax()]
    
    # Movies by rating categories
    high_rated_movies = data[data['IMDB_Rating'] >= 9].to_dict('records')
    mid_rated_movies = data[(data['IMDB_Rating'] > 8) & (data['IMDB_Rating'] < 9)].to_dict('records')
    
    return genre_stats, top_rated, high_rated_movies, mid_rated_movies

#Load
def load(genre_stats, top_rated, high_rated_movies, mid_rated_movies, output_file):
    genre_stats.to_csv(output_file, index=False)
    
    print("\nTop-Rated Movie:")
    print(f"{top_rated['Title']} ({top_rated['Year']}): {top_rated['IMDB_Rating']}/10")
    
    print("\nHigh-Rated Movies (IMDB ≥ 9):")
    for movie in high_rated_movies:
        print(f"{movie['Title']} ({movie['Year']}): {movie['IMDB_Rating']}/10")
    
    print("\nMid-Rated Movies (IMDB > 8 and < 9):")
    for movie in mid_rated_movies:
        print(f"{movie['Title']} ({movie['Year']}): {movie['IMDB_Rating']}/10")
    
    #Total Box Office by Genre
    plt.figure(figsize=(10, 6))
    plt.bar(genre_stats['Genre'], genre_stats['Total_Box_Office'], color='black')
    plt.title('Box Office Revenue by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Box Office Revenue (Millions)')
    plt.xticks(rotation=45)
    plt.savefig('movies_genre_box_office.png')

if __name__ == "__main__":
    input_file = "movies.csv"
    output_file = "transformed_movies.csv"
    raw_data = extract(input_file)
    genre_summary, top_movie, high_rated, mid_rated = transform(raw_data)
    load(genre_summary, top_movie, high_rated, mid_rated, output_file)
