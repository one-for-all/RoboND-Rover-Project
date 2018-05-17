from moviepy.editor import ImageSequenceClip
import glob

path = '../autonomous_images/*'
output = '../autonomous_video/video.mp4'
img_list = glob.glob(path)
clip = ImageSequenceClip(img_list, fps=60)
clip.write_videofile(output, audio=False)