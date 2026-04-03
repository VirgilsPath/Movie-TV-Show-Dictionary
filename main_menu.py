import tools_tracker

# tools_tracker.init_db()

data = tools_tracker.load_menu()

while True:
    print("----- Main Menu -----")
    print("1. Show Movie List")
    """print("2. Show TV Show List")
    print("3. Show Music List")"""
    print("4. Exit")
    print()

    choice = input("Choose a number to proceed: ")

    if choice == "1":
        # find list
        movie_list = data["Media To Download"]["Movies"]
        
        # check if list has movies
        if len(movie_list) > 0:
            print("----- Movies -----")
            for mov in movie_list:
                print(f"{mov["Name"]}: {mov["Year"]}: {mov["Downloaded"]}")
        else:
            # list is empty
            print("\nYour movie list is empty.")

        user_input = input("Type 'back' to go back or 'exit' to exit: ")

        if user_input.lower() == 'back':
            continue
        elif user_input.lower() == 'exit':
            print("Goodbye!")
            break