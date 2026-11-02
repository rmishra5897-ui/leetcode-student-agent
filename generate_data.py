import csv
import random

first_names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
    "Shaurya", "Atharv", "Dhruv", "Kabir", "Rudra", "Rohan", "Ananya", "Diya", "Gauri", "Kavya",
    "Anushka", "Isha", "Aditi", "Riya", "Sneha", "Tanvi", "Pooja", "Priya", "Neha", "Simran",
    "Rahul", "Ritik", "Amit", "Sumit", "Vikas", "Suresh", "Manish", "Deepak", "Nitin", "Harsh",
    "Ayush", "Abhishek", "Shivam", "Saurabh", "Pratik", "Kunal", "Yash", "Kartik", "Mohit", "Tarun"
]

last_names = [
    "Sharma", "Verma", "Mishra", "Gupta", "Singh", "Yadav", "Patel", "Joshi", "Kumar", "Pandey",
    "Tiwari", "Dubey", "Shukla", "Chauhan", "Rajput", "Saxena", "Bhatia", "Malhotra", "Mehta", "Jain"
]

# Real usernames for testing API calls
seed_usernames = ["tourist", "neal_wu", "lee215", "fevl", "awice", "uwi", "savemyself"]

records = []
for i in range(1, 201):
    f_name = random.choice(first_names)
    l_name = random.choice(last_names)
    full_name = f"{f_name} {l_name}"
    roll_no = f"CS2026_{i:03d}"
    
    # Mix of active real usernames and mock usernames
    if i % 15 == 0:
        username = random.choice(seed_usernames)
    else:
        username = f"{f_name.lower()}_{random.randint(10, 99)}"
        
    records.append([full_name, roll_no, username])

with open("students.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "roll_no", "leetcode_username"])
    writer.writerows(records)

print("200 students successfully generated in students.csv!")