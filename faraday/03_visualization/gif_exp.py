import glob
from PIL import Image


def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.JPG")][0:-1:56]
    frame_one = frames[0]
    frame_one.save("my_awesome.gif", format="GIF", append_images=frames,
                   save_all=True, duration=0.01, loop=0, fps=60)


if __name__ == "__main__":
    make_gif("C:/mnustes_science/images/img_lab/PT_04/f=14.20_a=10.00_gif")