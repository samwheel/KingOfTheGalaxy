from random import choice, choices

class RandomNameGenerator:
    def __init__(self) -> None:
        self.__vowels: list[str] = ["a", "e", "i", "o", "u", "y"]
        self.__alphabet: list[str] = list("abcdefghijklmnopqrstuvwxyz")
        self.__letter_probabilities: list[int] = [1 for _ in self.__alphabet]
        self.__consonants: list[str] = list(set(self.__alphabet) - set(self.__vowels))
        self.__patterns: dict[str, int] = {}

    
    def generate_probabilities(self, text:str) -> None:
        for character in text:
            if character in self.__alphabet:
                self.__letter_probabilities[self.__alphabet.index(character)] += 1

    
    def create_letter_probability(self, vowel_chance: int) -> list[float]:
        full_probability: list[float] = [vowel_chance if letter in self.__vowels else (5 - vowel_chance) for letter in self.__alphabet]
        full_probability = [full_probability[i] * self.__letter_probabilities[i] for i in range(len(full_probability))]
        return full_probability
    

    def random_name(self) -> str:
        name: str = ""
        snippets:list[str] = []
        for value, probability in self.__patterns.items():
            if probability > 0:
                snippets.append(value)
        snippets.extend(["in"])
        snippets = [choice(snippets) for _ in range(5, 10)]
        index = 0

        for _ in range(choice(range(4, 15))):
            vowel_chance = 0
            for i in range(len(name) - 1, -1, -1):
                vowel_chance += 1 if name[i] in self.__consonants else 0
                if vowel_chance == 0:
                    break
            
            similarities = 0
            name += choices(self.__alphabet, self.create_letter_probability(vowel_chance))[0]
            if index < len(snippets) and len(name) > 1:
                for i in range(-1, -3, -1):
                    if name[i] in self.__consonants:
                        if snippets[index] in self.__consonants:
                            similarities += 1
                        else: 
                            break
                    else:
                        if not snippets[index] in self.__vowels:
                            similarities += 1
                        else: 
                            break
                
                if similarities > 1:
                    name = name[:-2]
                    name += snippets[index]
                    index += 1

        return name
    
    def review_names(self, names: list[str], accepted_names: list[str], unaccepted_names: list[str], like_threshold:int = 10) -> list[list[str]]:
        names_to_accept: list[str] = []
        names_to_like: list[str] = []
        self.__patterns = {}
        for name in accepted_names:
            for character in name:
                if name.index(character) != 1:
                    for letter in name[:name.index(character) - 1]:
                        try:
                            self.__patterns[name[name.index(letter):name.index(character)]] += 3
                        except KeyError:
                            self.__patterns[name[name.index(letter):name.index(character)]] = 3
        
        for name in unaccepted_names:
            for character in name:
                if name.index(character) != 1:
                    for letter in name[:name.index(character)]:
                        try:
                            self.__patterns[name[name.index(letter):name.index(character)]] -= 1
                        except KeyError:
                            pass
        
        self.__patterns[""] = 0
        with open("like_prob.dat", "w") as file:
            for pattern, strength in sorted(self.__patterns.items(), key=lambda item: item[1], reverse=True):
                file.write(f"{pattern}, {strength}\n")

        for name in names:
            liked_probability = 0
            for character in name:
                try:
                    liked_probability += self.__patterns[name[:name.index(character)]]
                except KeyError:
                    pass
            if liked_probability > 0:
                print(f"Accepting: {name}")
                print(f"{name}'s liked probability: {liked_probability}")
                
                if liked_probability > like_threshold - 1:
                    print(f"Liking: {name}")
                    names_to_like.append(name)
                else:
                    names_to_accept.append(name)
        
        return [names_to_accept, names_to_like]


generator = RandomNameGenerator()
unaccept_names: str = input("Would you like to move the reviewed names to the unaccepted name file (Y/n)?: ").lower().strip() + " "
if unaccept_names[0] != "n":
    with open("reviewed_names.txt", "r") as reviewed_names:
        with open("unaccepted_names.txt", "a") as unaccepted_names:
            unaccepted_names.writelines(reviewed_names.readlines())

like_threshold = int(input("What liked threshold do you want?: "))

name_string:str = ""
with open("names.txt") as name_file:
    for line in name_file:
        name_string += line.strip()

generator.generate_probabilities(name_string)

with open("generated_names.txt", "w") as name_file:
    for _ in range(1000):
        random_name: str = generator.random_name()
        name_file.write(random_name + "\n")

reviewed_name_list: list[str] = []
liked_name_list: list[str] = []
    
with open("generated_names.txt", "r") as name_file:
    with open("names.txt") as accepted_name_file:
        with open("unaccepted_names.txt", "r") as unaccepted_name_file:
            reviewed_name_list, liked_name_list = generator.review_names(
                [name.strip().lower() for name in name_file.readlines()], 
                [name.strip().lower() for name in accepted_name_file.readlines()], 
                [name.strip().lower() for name in unaccepted_name_file.readlines()],
                like_threshold
            )


with open("reviewed_names.txt", "w") as name_file:
    for name in reviewed_name_list:
        name_file.write(name + "\n")


with open("names.txt", "a") as name_file:
    for name in liked_name_list:
        name_file.write("\n" + name)