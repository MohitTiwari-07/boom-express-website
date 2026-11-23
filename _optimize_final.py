import subprocess
from pathlib import Path
import imageio_ffmpeg

src = Path("static/videos/hero.mp4")
out = Path("static/videos/hero.final.mp4")
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

if out.exists():
    out.unlink()

cmd = [
    ffmpeg, "-y", "-i", str(src),
    "-vf", "scale=1080:-2",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "28",
    "-pix_fmt", "yuv420p",
    "-an",
    "-movflags", "+faststart",
    str(out)
]

result = subprocess.run(cmd)
if result.returncode != 0 or not out.exists():
    raise SystemExit("Compression failed. Existing videos are safe.")

print("\nCOMPRESSION TEST COMPLETE")
print("Original:", round(src.stat().st_size / 1048576, 2), "MB")
print("Previous:", round(Path("static/videos/hero.optimized.mp4").stat().st_size / 1048576, 2), "MB")
print("New:", round(out.stat().st_size / 1048576, 2), "MB")
