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

    def format(self, file):
        # save this for ffmpeg
        pass

    def uvr(self, file, agressive=False, de_echo=True):
        # file = self.separator.separate(file)
        print(file)
        self.separator.load_model("UVR-DeEcho-DeReverb.pth")
        file = self.separator.separate(file)
        print(file)
        pass


if __name__ == "__main__":
    processor = AudioProcessor()
    print(
        processor.uvr(r"F:\Nerd Shit\Python\dataset-creator\chapter4_43_cyrene_102.wav")
    )
    # https://colab.research.google.com/drive/1LoLgL1YHzIQfILEayDmRUZzDZzJpD6rD#scrollTo=UD6BAuTSPWkB

# if __name__ == "__main__":
#     process = AudioProcessor()
#     print(process.uvr("C:\\Users\\Hikari\\Downloads\\maybe\\test.wav"))


# UVR-De-Echo-Aggressive.pth is shit
# Reverb_HQ_By_FoxJoy.onnx + UVR-De-Echo-Aggressive.pth is shit
# Kim_Vocal_2.onnx does nothing
# UVR-DeEcho-DeReverb.pth is shit
# dereverb-echo_mel_band_roformer_sdr_10.0169.ckpt deletes the audio
# UVR_MDXNET_Main.onnx is shit
# i cant lie this is really annoying to go through
# tasukete pls :(
# htdemucs_ft.yaml doesnt work :O
# dereverb-echo_mel_band_roformer_sdr_13.4843_v2.ckpt does nothing
# deverb_bs_roformer_8_384dim_10depth.ckpt does nothing
# dereverb_mel_band_roformer_anvuew_sdr_19.1729.ckpt does nothing

# tldr: UVR-DeEcho-DeReverb.pt is probably thje best and i cba to use uvr anymore

# TURNS OUT THIS DOES WORK FOR SOME FILES
# chapter4_43_cyrene_102.wav WILL WORK WITH UVR-DEECHO-DEREVERB
