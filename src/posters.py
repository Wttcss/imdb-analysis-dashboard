# =============================================================================
# 3. 4K POSTER DATABASE
# =============================================================================
POSTER_DB = {
    "avatar": "https://image.tmdb.org/t/p/original/kyeqWdyUXW608qlYkRqosgbbJyK.jpg",
    "titanic": "https://image.tmdb.org/t/p/original/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
    "the avengers": "https://image.tmdb.org/t/p/original/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg",
    "jurassic world": "https://image.tmdb.org/t/p/original/uXZYawqUsChGSj54wcuBtEdUJbh.jpg",
    "furious 7": "https://upload.wikimedia.org/wikipedia/en/b/b8/Furious_7_poster.jpg",
    "avengers: age of ultron": "https://image.tmdb.org/t/p/original/4ssDuvEDkSArWEdyBl2X5EHvYKU.jpg",
    "frozen": "https://upload.wikimedia.org/wikipedia/en/0/05/Frozen_%282013_film%29_poster.jpg",
    "iron man 3": "http://3.bp.blogspot.com/-E-p3JrvqpEA/UX65iuaX6EI/AAAAAAAAFNQ/mGz7Y_-Ctv0/s1600/Iron_Man_3_New_Poster_Final_Latino_V2_Cine_1.jpg",
    "minions": "https://resizing.flixster.com/8KeqKZfuOFJT6OVZLnCgmwthTI4=/206x305/v2/https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p11376954_p_v13_bc.jpg",
    "captain america: civil war": "https://image.tmdb.org/t/p/original/rAGiXaUfPzY7CDEyNKUofk3Kw2e.jpg",
    "transformers: dark of the moon": "https://image.tmdb.org/t/p/original/kvXLZqY0Ngl1XSw7EaMQO0C1CCj.jpg",
    "the lord of the rings: the return of the king": "https://image.tmdb.org/t/p/original/rCzpDGLbOoPwLjy3OAm5NUPOznC.jpg",
    "skyfall": "https://image.tmdb.org/t/p/original/u29Zgu6B47C56X5X5fM1rQ5q.jpg",
    "transformers: age of extinction": "https://image.tmdb.org/t/p/original/ykFh9raB1K6Zf9Wl5sZg1w9eX.jpg",
    "the dark knight rises": "https://image.tmdb.org/t/p/original/85cWkCVftiVs0BV86x0nl1phPTv.jpg",
    "toy story 3": "https://image.tmdb.org/t/p/original/AbbXspMOwdvwWZgVX0dadPrM9Ff.jpg",
    "pirates of the caribbean: dead man's chest": "https://image.tmdb.org/t/p/original/uXEqmloGyP7UXAwd_x7H9C.jpg",
    "pirates of the caribbean: on stranger tides": "https://image.tmdb.org/t/p/original/w2PMyoyLU22YvrGKzsmVM0fKd.jpg",
    "alice in wonderland": "https://image.tmdb.org/t/p/original/1HtWyQsp5O6l9K8sV56hR3aVlZl.jpg",
    "the hobbit: an unexpected journey": "https://image.tmdb.org/t/p/original/yHA9Fc37VmpUA5UncTxxo3rTGVA.jpg",
    "the dark knight": "https://image.tmdb.org/t/p/original/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "star wars: the force awakens": "https://image.tmdb.org/t/p/original/wqnLdwVXoBjKibfR5TRBck12nJ1.jpg",
    "harry potter and the philosopher's stone": "https://image.tmdb.org/t/p/original/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg",
}


def get_smart_poster(title):
    clean_title = str(title).strip().lower()
    if clean_title in POSTER_DB: return POSTER_DB[clean_title]
    for key in POSTER_DB:
        if key in clean_title or clean_title in key: return POSTER_DB[key]
    safe_title = urllib.parse.quote(str(title))
    return f"https://placehold.co/400x600/111/F5C518/png?text={safe_title}&font=roboto"
