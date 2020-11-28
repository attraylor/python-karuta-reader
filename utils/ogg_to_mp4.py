import subprocess
import argparse
import os

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--sound_dir", type=str, default=None)
	parser.add_argument("--write_dir", type=str, default=None)
	args = parser.parse_args()

	if not os.path.exists(args.write_dir):
		os.makedirs(args.write_dir)

	for f in os.listdir(args.sound_dir):
		old_fp = os.path.join(args.sound_dir, f)
		new_fp = os.path.join(args.write_dir, f.replace(".ogg", ".mp4"))
		if ".ogg" == f[-4:]:
			subprocess.call(["ffmpeg", "-i", old_fp, new_fp])
	print("done")
