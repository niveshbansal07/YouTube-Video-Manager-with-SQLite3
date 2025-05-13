import sqlite3

connection = sqlite3.connect('YouTube_Videos.db')

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        time TEXT NOT NULL
    );
''')

def get_time():
    while True:
        time_input = input("Enter Video time (HH:MM): ")
        if ":" in time_input:
            hh, mm = time_input.split(":")
            if hh.isdigit() and mm.isdigit():
                hh = int(hh)
                mm = int(mm)
                if 0 <= mm < 60:
                    return f"{hh:02d}:{mm:02d}"
        print("Invalid time format. Please use HH:MM where hours can be any number and minutes 0-59.")

def list_videos():
    cursor.execute("SELECT * FROM videos")
    for row in cursor.fetchall():
        print(row)

def add_video(name, time):
    cursor.execute("INSERT INTO videos (name, time) VALUES (?, ?)", (name, time))
    connection.commit()
    print("- Success! Your video has been added to the library. -")

def update_video(video_id, new_name, new_time):
    cursor.execute("UPDATE videos SET name = ?, time = ? WHERE id = ?", (new_name, new_time, video_id))
    connection.commit()
    print("- Success! Your video has been updated. -")


def delete_video(video_id):
    cursor.execute("DELETE FROM videos where id = ?",(video_id,))
    connection.commit()
    print("- Video deleted successfully! -")

def search_video(video_name):     
    cursor.execute("SELECT id, name, time FROM videos WHERE name LIKE ?", ('%' + video_name + '%',))
    results = cursor.fetchall()
    if results:
        for video_id, name, time in results:
            print("_" * 25)
            print(f"ID       : {video_id}")
            print(f"Name     : {name}")
            print(f"Duration : {time}")
            print("_" * 25)
    else:
        print("- Video is not found -")

def main():
    while True:
        print("\nYOUTUBE MANAGER 💼🚀 with DB")
        print("Choose an option:")
        print("1. List YouTube Videos")
        print("2. Add Videos")
        print("3. Search Videos")
        print("4. Update Videos")
        print("5. Delete Videos")
        print("6. Exit app")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("-" * 25)
            list_videos()
            print("-" * 25)
        elif choice == '2':
            name = input("Enter the video name: ").capitalize()
            time = get_time()
            add_video(name, time)
        elif choice == '3':
            video_name = input("Enter Video name to search: ").capitalize()
            search_video(video_name)
        elif choice == '4':
            list_videos()
            video_id = input("Enter video ID to Update: ")
            new_name = input("Enter the New name of Video: ")
            new_time = input("Enter the New time of Video: ")
            update_video(video_id, new_name, new_time)
        elif choice == '5':
            list_videos()
            video_id = input("Enter video ID to Delete: ")
            delete_video(video_id)
        elif choice == '6':
            break
        else:
            print("Invalid Choice") 

    connection.close()

if __name__ == "__main__":
    main()
