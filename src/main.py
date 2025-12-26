from utils import clear_the_fucking_input
from manual_sort import ManualSorter
import generate_list
import os


def prompt_for_bad_processing():
    # start with vad, then uvr, then possibly audiosr?
    from session import session

    print(session)
    audio_processor = AudioProcessor()
    with open(f"{session['Dataset']}/bad.txt") as f:
        files = f.readlines()
        for file in files:
            input(f"Will process {file}. Press enter to continue")
            audio_processor.uvr(file)
    pass


if __name__ == "__main__":
    from session import session

    if session["Dataset name"]:
        while True:
            match input(
                f'Do you want to load the previous session.? <y/n>\nThis will load "{session["Dataset name"]}" '
            ):
                case "y":
                    sorter = ManualSorter(session["Dataset name"], session["Path"])
                    match sorter.main_sort_loop():
                        case "Completed":
                            print("Successfully sorted all files.")
                            break
                        case "Requested Exit":
                            print("Early exit requested")
                            break

                case "n":
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
            "Mode? \n1. Sort\n2. Fix bad\n3. Export as Parquet\n4. Fuck off \n"
        ):
            case "1":
                dataset_name = input("Name of dataset: ")
                dataset_path = input("Provide dataset path: ")

                if os.path.isdir(dataset_path):
                    from session import session

                    session["Dataset name"] = dataset_name
                    session["Path"] = dataset_path

                else:
                    raise AttributeError("Incorrect directory")
                sorter = ManualSorter(dataset_name, dataset_path)
                if sorter.main_sort_loop() == "Completed":
                    print("Successfully sorted all files.")
                    break
            case "2":
                from audio_processor import AudioProcessor

                prompt_for_bad_processing()
            case "3":
                os.system("cls")
                import exporter as Exporter

                print("This will export the existing session: \n")
                print(session)
                if input("Proceed? <y/*>") == "y":
                    exporter = Exporter.Exporter()
                    exporter.move_for_processing()
                    exporter.export_as_parquet()

            case "4":
                exit()
