from audio_separator.separator import Separator


class AudioProcessor:
    def __init__(self):
        print("Will copy files, then process")
        self.preserve_original = True
        self.separator = Separator()
        # self.separator.load_model(
        #     model_filename="Reverb_HQ_By_FoxJoy.onnx"
        # )  # we need this as well as de-echo

        # while True:
        #     match input("Do you want to: \n1. edit the files\n2. Use a copy?"):
        #         case "1":
        #             self.preserve_original = False
        #             self.separator = Separator()

        #         case "2":
        #             self.preserve_original = True
        #             self.separator = Separator(
        #                 output_dir=f"output/{session['Dataset']}/processed_files/"
        #             )
        self.separator.load_model("UVR-DeEcho-DeReverb.pth")

    def format(self, file):
        # save this for ffmpeg
        pass

    def uvr(self, file, agressive=False, de_echo=True):
        # file = self.separator.separate(file)
        # self.separator.load_model("UVR-DeEcho-DeReverb.pth")
        file = self.separator.separate(file)
        # TODO: find the processed one, rename, then move
