import json
from collections import defaultdict

def load(filename):
    digramFreq = defaultdict(lambda: defaultdict(int))
    
    with open(filename, "r", encoding="utf-8") as fobj:
        for line in fobj:
            digram = line.strip().split(" : ")
            if len(digram) == 2:
                digram, freq = digram
                freq = int(freq)
                try:
                    firstWord, secondWord = digram.split()
                    digramFreq[firstWord][secondWord] = freq
                except ValueError:
                    continue
            else:
                continue
                
    return digramFreq

def predict(digramFreq, currentWord):
    nextWord = digramFreq.get(currentWord, {})
    
    if not nextWord:
        return "Không thể dự đoán."
    
    sortedNextWord = sorted(nextWord.items(), key=lambda item: item[1], reverse=True)
    
    return sortedNextWord

def save_to_json(data, filename):
    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":

    filename = "output.txt" 
    digramFreq = load(filename)
    
    currentWord = input("Nhập từ: ").strip().lower()
    
    nextWord = predict(digramFreq, currentWord)
    
    if isinstance(nextWord, str):
        print(nextWord)
    else:
        result = {}
        for word, freq in nextWord:
            # print(f"{currentWord} {word} : {freq}")
            result[word] = freq
        
        save_to_json(result, "output.json")
