import os, sys
import cv2, decord, numpy as np

# Command line arguments
path = sys.argv[1]
"""The path to the video file"""
output = sys.argv[2]
"""The output directory for the extracted frames"""
startSeconds = float(sys.argv[3]) or 0
"""The starting timestamp in seconds. It allows skipping the opening credits and going directly to the main content."""
endSeconds = float(sys.argv[4]) or None
"""The ending timestamp in seconds. It allows trimming video's ending credits."""
step = float(sys.argv[5]) or 0.5
"""The time interval in seconds between extracted frames"""

def getFrame(timestamp: float) -> np.ndarray:
    """Get the frame at the specified timestamp in seconds."""
    frameIndex = round(timestamp * fps)
    return vr[frameIndex].asnumpy()

# Load the video using decord
vr = decord.VideoReader(path)
fps = vr.get_avg_fps()
# Calculate frame indices for both start and end points
startFrameIndex = round(startSeconds * fps)
# Get the timestamps for all frames in the video
# The function returns two values for each frame: start and end timestamps for that frame. We take the mean to get a single timestamp for each frame.
timestamps = vr.get_frame_timestamp(range(len(vr))).mean(-1)


endSeconds = endSeconds or len(vr) / fps

# Save each frame in the specified range as a JPEG image, named by its timestamp in milliseconds
for i in range(startSeconds, endSeconds, step):
    frame = getFrame(i)
    timestamp = i
    filename = f'{output}/{stamp:.0f}.jpg'
    if os.path.exists(filename):
        print(f'{filename} already exists, skipping')
        continue
    # Save the frame
    cv2.imwrite(f'{output}/{stamp:.0f}.jpg', cv2.cvtColor(frame.asnumpy(), cv2.COLOR_RGB2BGR))