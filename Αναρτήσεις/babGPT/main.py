import llm
import data_stats

def main():
    filename = "greek-language-scrap-kariotakis.txt"
    with open(filename, "r", encoding = "utf8") as file:
        text = file.read()
    model = llm.LLM(text)
    # with open("model.json", "w") as file:
    #     json.dump(model.export(), file, indent = 2)
    # with open("model.txt", "w") as file:
    #     file.write(str(model.export()))
    trials = 20
    for i in range(trials):
        story = model.generate_text()
        print(" ".join(story))
        if i < trials - 1:
            print("=" * 50)

if __name__ == "__main__":
    main()
    filename = "greek-language-scrap-kariotakis.txt"
    # counts = data_stats.counts(filename)
    # print(counts)
    # with open(filename, "r") as file:
    #     text = file.read()
    # print(text[0:50])
