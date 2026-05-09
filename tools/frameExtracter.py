import os, sys
import cv2, decord, numpy as np

# Command line arguments
# The path to the video file
path = sys.argv[1]
# The output directory for the extracted frames
output = sys.argv[2]
# The starting timestamp in seconds. It allows skipping the opening credits and going directly to the main content.
try:
    startSeconds = float(sys.argv[3])
except IndexError:
    startSeconds = 0
# The ending timestamp in seconds. It allows trimming video's ending credits.
try:
    endSeconds = float(sys.argv[4])
except IndexError:
    endSeconds = None
# The time interval in seconds between extracted frames
try:
    step = float(sys.argv[5])
except IndexError:
    step = 0.5

def getFrame(timestamp: float) -> np.ndarray:
    """Get the frame at the specified timestamp in seconds."""
    frameIndex = round(timestamp * fps)
    return vr[frameIndex].asnumpy()

# Load the video using decord
vr = decord.VideoReader(path)
fps = vr.get_avg_fps()

# Cap the end time to the video's duration
maxSeconds = len(vr) / fps
if endSeconds:
    endSeconds = min(endSeconds, maxSeconds)
else:
    endSeconds = maxSeconds

# Save each frame in the specified range as a JPEG image, named by its timestamp in milliseconds
for timestamp in range(int(startSeconds * 1000), int(endSeconds * 1000), int(step * 1000)):
    frame = getFrame(timestamp / 1000)
    filename = f'{output}/{timestamp:.0f}.jpg'
    if os.path.exists(filename):
        print(f'{filename} already exists, skipping')
        continue
    # Save the frame
    cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))