import requests
import json


def get_word(input_word, word_tense):
    payload = {
        "language": "pt",
        "text": str(input_word),
        "pos": str(word_tense)
    }

    with open("Credentials/dictapiUrl.txt", 'r') as out:
        url = str(out.readline())

        r = requests.get(url, params=payload)

        dict_content = json.loads(r.content)
        results = dict_content["results"]

        if bool(results):
            senses = results[0]["senses"]

            if bool(senses):
                definition_list = []

                count = 0
                for i in range(len(senses)):
                    if i < 3:
                        if "definition" in senses[i]:
                            definition_list.append(senses[i]["definition"])
                            count += 1
                        else:
                            if i == 0:
                                definition_list.append("NO DEFINITION FOUND")
                                count += 1
                    else:
                        break

                for i in range(3 - count):
                    definition_list.append("")

                # if len(definition_list) == 0:
                #    definition_list = ["NONE"]

                return definition_list
            else:
                return ["DON'T RECOGNIZE WORD", "", ""]
        else:
            return ["DON'T RECOGNIZE WORD", "", ""]


def convert_file_into_anki_import(input_file, output_file, word_type):
    with open(str(output_file), newline='', mode="w", encoding='utf8') as file_out:
        word_list = []

        with open("Data/Input/" + str(input_file) + ".txt") as file_in:
            for line in file_in:
                word_list.append(line.strip())

        progress_count = 0
        for word in word_list:
            word_to_add = word.lower()

            data = get_word(word_to_add, word_type)

            all_definitions = ""

            for cur_dat in data:
                cur_definition = ";" + cur_dat.lower().capitalize()
                all_definitions += cur_definition

            sound_file = ";" + "[sound:" + input_file + "_" + str(progress_count) + ".mp3]"
            file_out.writelines(word_to_add.capitalize() + sound_file + all_definitions + "\n")

            progress_count += 1
            percentage = round(100.0 * progress_count / len(word_list), 1)
            print("Progress: " + str(percentage) + "%" + " | Current word: " + word)
