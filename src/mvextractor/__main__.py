import sys
import os
import time
from datetime import datetime
import argparse

import numpy as np
import cv2

from mvextractor.videocap import VideoCap

'''
The JSON will look like:
[
	{
		"source" : <val>,
		"mb_w"  : <val>,
		"mb_h" : <val>,
		"src_x"  : <val>,
		"src_y"  : <val>,
		"dst_x"  : <val>,
		"dst_y"  : <val>,
		"motion_x"  : <val>,
		"motion_y"  : <val>,
     "motion_scale"  : <val>
	},
 ...
]
'''

def dump_motion_vectors(file_path, motion_vectors):
    print(f"Type of motion_vectors: {type(motion_vectors)}")
    print(f"Shape of motion_vectors: {np.shape(motion_vectors)}")

    # dump motion vectors to json file
    with open(file_path, "w") as f:
        f.write("[\n")
        for i, mv in enumerate(motion_vectors):
            f.write("\t{\n")
            f.write(f'\t\t"source" : {mv[0]},\n')
            f.write(f'\t\t"mb_w" : {mv[1]},\n')
            f.write(f'\t\t"mb_h" : {mv[2]},\n')
            f.write(f'\t\t"src_x" : {mv[3]},\n')
            f.write(f'\t\t"src_y" : {mv[4]},\n')
            f.write(f'\t\t"dst_x" : {mv[5]},\n')
            f.write(f'\t\t"dst_y" : {mv[6]},\n')
            f.write(f'\t\t"motion_x" : {mv[7]},\n')
            f.write(f'\t\t"motion_y" : {mv[8]},\n')
            f.write(f'\t\t"motion_scale" : {mv[9]}\n')
            f.write("\t}")
            if i < len(motion_vectors) - 1:
                f.write(",")
            f.write("\n")
        f.write("]\n")


def draw_motion_vectors(frame, motion_vectors, file_path=""):
    if file_path:
        f = open(file_path, "w")

    if len(motion_vectors) > 0:
        num_mvs = np.shape(motion_vectors)[0]
        shift = 2
        factor = (1 << shift)
        for mv in np.split(motion_vectors, num_mvs):
            start_pt = (int((mv[0, 5] + mv[0, 7] / mv[0, 9]) * factor + 0.5), int((mv[0, 6] + mv[0, 8] / mv[0, 9]) * factor + 0.5))
            end_pt = (mv[0, 5] * factor, mv[0, 6] * factor)
            if file_path:
                f.write(f"{int(start_pt[0]), int(start_pt[1])}, {int(end_pt[0]), int(end_pt[1])}\n")
            cv2.arrowedLine(frame, start_pt, end_pt, (0, 0, 255), 1, cv2.LINE_AA, shift, 0.1)
    if file_path:
        f.close()
    return frame


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Extract motion vectors from video.')
    parser.add_argument('video_url', type=str, nargs='?', help='file path or url of the video stream')
    parser.add_argument('-p', '--preview', action='store_true', help='show a preview video with overlaid motion vectors')
    parser.add_argument('-v', '--verbose', action='store_true', help='show detailled text output')
    parser.add_argument('-d', '--dump', nargs='?', const=True,
        help='dump frames, motion vectors, frame types, and timestamps to optionally specified output directory')
    args = parser.parse_args()

    # Extract name of the video file
    video_name = args.video_url.split("/")[-1].split(".")[0]

    if args.dump:
        if isinstance(args.dump, str):
            dumpdir = args.dump
        else:
            # dumpdir = f"out-{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
            dumpdir = os.path.join("outputs", video_name)
            if os.path.exists(dumpdir):
                # remove existing directory, even if it is not empty
                os.system(f"rm -rf {dumpdir}")
        os.makedirs(dumpdir, exist_ok=True)
        for child in ["frames", "motion_vectors", "json"]:
            os.makedirs(os.path.join(dumpdir, child), exist_ok=True)

    cap = VideoCap()

    # open the video file
    ret = cap.open(args.video_url)

    if not ret:
        raise RuntimeError(f"Could not open {args.video_url}")
    
    if args.verbose:
        print("Sucessfully opened video file")

    step = 0
    times = []

    # continuously read and display video frames and motion vectors
    while True:
        if args.verbose:
            print("Frame: ", step, end=" ")

        tstart = time.perf_counter()

        # read next video frame and corresponding motion vectors
        ret, frame, motion_vectors, frame_type, timestamp = cap.read()

        tend = time.perf_counter()
        telapsed = tend - tstart
        times.append(telapsed)

        # if there is an error reading the frame
        if not ret:
            if args.verbose:
                print("No frame read. Stopping.")
            break

        # print results
        if args.verbose:
            print("timestamp: {} | ".format(timestamp), end=" ")
            print("frame type: {} | ".format(frame_type), end=" ")

            print("frame size: {} | ".format(np.shape(frame)), end=" ")
            print("motion vectors: {} | ".format(np.shape(motion_vectors)), end=" ")
            print("elapsed time: {} s".format(telapsed))

        dump_motion_vectors(os.path.join(dumpdir, "json", f"{step}.json"), motion_vectors)

        frame = draw_motion_vectors(frame, motion_vectors, os.path.join(dumpdir, "motion_vectors", f"draw-{step}.txt"))

        # store motion vectors, frames, etc. in output directory
        if args.dump:
            cv2.imwrite(os.path.join(dumpdir, "frames", f"frame-{step}.jpg"), frame)
            np.save(os.path.join(dumpdir, "motion_vectors", f"mvs-{step}.npy"), motion_vectors)
            with open(os.path.join(dumpdir, "timestamps.txt"), "a") as f:
                f.write(str(timestamp)+"\n")
            with open(os.path.join(dumpdir, "frame_types.txt"), "a") as f:
                f.write(frame_type+"\n")

        step += 1

        if args.preview:
            cv2.imshow("Frame", frame)

            # if user presses "q" key stop program
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    if args.verbose:
        print("average dt: ", np.mean(times))

    cap.release()

    # close the GUI window
    if args.preview:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
