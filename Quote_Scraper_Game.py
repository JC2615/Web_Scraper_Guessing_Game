import random
import requests
from bs4 import BeautifulSoup

info = []
response = requests.get("http://quotes.toscrape.com")

while(True):
    soup = BeautifulSoup(response.text, "html.parser")
    quote = soup.find_all(class_="quote")
    for q in quote:
        text = q.find_next().text
        author = q.find_next(class_="author").text
        link = q.find_next(class_="author").find_next()["href"]
        info.append([text, author, link])
    try:
        next_button = soup.find(class_="next").find_next()["href"]
    except:
        break
    response = requests.get("http://quotes.toscrape.com" + str(next_button))
    
playing = True
while(playing):
    guesses = 4
    quote = random.choice(info)
    aresponse = requests.get("http://quotes.toscrape.com" + str(quote[2]))
    bio = BeautifulSoup(aresponse.text, "html.parser")
    hint1p1 = bio.find(class_="author-born-date").text 
    hint1p2 = bio.find(class_="author-born-location").text 
    hint2 = quote[1][0]
    hint3 = len(quote[1]) - 1
    hint4 = ""
    for i in range(len(quote[1])):
        if quote[1][i] == " ":
            hint4 = quote[1][i+1]
            break

    while True:
        print(quote[0])
        answer = input("Enter a guess for the quote's author: \n\n").lower()
        if answer == quote[1].lower():
            print("You're absolutely right. Good job!")
            play_again = input("Would you like to play again? Enter y or n:").lower()
            while (play_again != "y" and play_again != "n"):
                play_again = input("Invalid input. Try again: ")
            if play_again == "y":
                break
            else:
                playing = False
                break
        elif answer != quote[1].lower() and guesses == 4:
            guesses -= 1
            print("Sorry, that's wrong.")
            print(f"Here's a hint: The author was born on {hint1p1} in {hint1p2}\n\n")
        elif answer != quote[1].lower() and guesses == 3:
            guesses -= 1
            print("Wrongo!")
            print(f"The author's first initial is {hint2}.\n\n")
        elif answer != quote[1].lower() and guesses == 2:
            guesses -= 1
            print("Do better, dude.")
            print(f"His/her name has {hint3} letters in it.\n\n")
        elif answer != quote[1].lower() and guesses == 1:
            guesses -= 1
            print("You're really bad at this.")
            print(f"His/her last initial is {hint4}.\n\n")
        else:
            print(f"You lost, bud. The author was {quote[1]}")
            play_again = input("Would you like to play again? Enter y or n:\n\n").lower()
            while (play_again != "y" and play_again != "n"):
                play_again = input("Invalid input. Try again: ")
            if play_again == "y":
                break
            else:
                playing = False
                break    
