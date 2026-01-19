from utils import clear_the_fucking_input
from manual_sort import ManualSorter
import os
from pathlib import Path, WindowsPath
import time


def init_new_session():
    dataset_name = input("Name of dataset: ")
    dataset_path = input("Provide dataset path: ")

    if os.path.isdir(dataset_path):
        from session import session

        session["Dataset name"] = dataset_name
        session["Path"] = Path(dataset_path).as_posix()

    else:
        raise AttributeError("Incorrect directory")
    while True:
        match input(
            "How is the dataset formatted? "
            "\n 1. Ai Hobbyist (.lab + .wav)"
            "\n 2. LJSpeech (Not Implemented)"
            "\n 3. VCTK (Not Implemented)\n> "
        ):
            case "1":
                session["Dataset format"] = "Ai Hobbyist"
                break
            case "2":
                print("Not implemented yet")
                # break
            case "3":
                print("Not implemented yet")
                # break
            case _:
                print("bro")
    while True:
        match input(
            "What language is the dataset in? "
            "\n 1. English"
            "\n 2. Japanese"
            "\n 3. Chinese"
            "\n 4. Korean"
            "\n 5. Cantonese\n> "
        ):
            case "1":
                session["Language"] = "en"
                break
            case "2":
                session["Language"] = "ja"
                break
            case "3":
                session["Language"] = "zh"
                break
            case "4":
                session["Language"] = "ko"
                break
            case "5":
                session["Language"] = "yue"
                break
            case _:
                print("what")
    session.save()


if __name__ == "__main__":
    from session import session

    if session["Dataset name"]:
        while True:
            match input(
                f'Do you want to load the previous session.? <y/n>\nThis will load "{session["Dataset name"]}" '
            ):
                # # TODO: Add a check for if the sorting is completed,
                case "y":
                    #     sorter = ManualSorter()
                    #     match sorter.main_sort_loop():
                    #         case "Completed":
                    #             print("Successfully sorted all files.")
                    #             break
                    #         case "Requested Exit":
                    #             print("Early exit requested")
                    #             break
                    # import utils

                    # test this another time its 00:34
                    # also either way i can pass and if the user tries to sort it will autoexit

                    # good = open(f"{session['Dataset name']}/good.txt", "r").readlines()
                    # bad = open(f"{session['Dataset name']}/bad.txt", "r").readlines()
                    # all_sorted = True
                    # for file in utils.iter_files(session["Path"], ".wav"):
                    #     if WindowsPath(file) not in good and file not in bad:
                    #         print(f"Unsorted file found: {file}")
                    #         all_sorted = False
                    #         break
                    # if all_sorted:
                    #     while True:
                    #         match input(
                    #             "All files already sorted.\nDo you want to export? <y/n>"
                    #         ):
                    #             case "y":
                    #                 import exporter as Exporter

                    #                 exporter = Exporter.Exporter()
                    #                 exporter.move_for_processing()
                    #                 exporter.export_as_parquet()
                    #                 print(
                    #                     f"Successfully exported the dataset to exports/{session['Dataset name']}.parquet!"
                    #                 )
                    #                 time.sleep(2)
                    #                 input("Press enter to exit...")
                    #                 exit(0)

                    #             case "n":
                    #                 break
                    #             case _:
                    #                 pass

                    break

                case "n":
                    init_new_session()
                    break
                case _:
                    pass

        # else:
        #     print("No previous save found")
        #     try:
        #         os.mkdir("settings")
        #     except FileExistsError:
        #         pass

        #     with open("settings/settings.toml", "w+") as f:
        #         f.write(toml.dumps(save))

    while True:  #
        clear_the_fucking_input()

        match input(
            "Mode? \n1. Sort\n2. Fix bad files\n3. Export as Parquet\n4. Quit \n"
        ):
            case "1":
                sorter = ManualSorter()
                match sorter.main_sort_loop():
                    case "Completed":
                        print("Successfully sorted all files.")
                        break
                    case "Requested Exit":
                        print("Early exit requested")
                        break

            case "2":
                from processing.audio_processor import AudioProcessor

                processor = AudioProcessor()
                processor.prompt_for_bad_processing()  # kinda just fuck off from main loop icl

            case "3":
                os.system("cls")
                import exporter as Exporter

                if session != session._default:
                    print("This will export the existing session: \n")
                    print(session)
                    if input("Proceed? <y/*>") == "y":
                        try:
                            exporter = Exporter.Exporter()
                            exporter.move_for_processing()
                            exporter.export_as_parquet()
                            print(
                                f"Successfully exported the dataset to exports/{session['Dataset name']}.parquet!"
                            )
                            time.sleep(2)
                        except Exception as e:
                            print(e)

                else:
                    dataset_name = input("Name of dataset: ")
                    dataset_path = input("Provide dataset path: ")

            case "4":
                exit()
