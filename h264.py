import ffmpeg

# Decodes any video file "in_filename" to a rawvideo file "out_filename"
def h264_decode(in_filename, out_filename, **ffmpeg_kwargs):
    (
        ffmpeg
        .input(in_filename)['v']
        .output(out_filename, vcodec='rawvideo', map='0:v:0', **ffmpeg_kwargs)
        .run()
    )

# Encodes any video file "in_filename" to a H.264 file "out_filename"
def h264_encode(in_filename, out_filename, **ffmpeg_kwargs):
    (
        ffmpeg
        .input(in_filename)
        .output(out_filename, vcodec='libx264', map='0:v:0', **ffmpeg_kwargs)
        .run()
    )

# Takes frame #frame_num in any video file "in_video_filename" and saves it
# as a JPEG file "out_jpeg_filename"
def get_jpeg_frame(in_video_filename, out_jpeg_filename, frame_num):
    (
        ffmpeg
        .input(in_video_filename)
        .filter('select', 'gte(n, {})'.format(frame_num))
        .output(out_jpeg_filename, vframes=1, format='image2', vcodec='mjpeg')
        .run()
    )

# Returns a dictionary with all of the available information about the file
def get_file_info(in_filename):
    return ffmpeg.probe(in_filename)

# Returns a dictionary with the information about the main video stream
def get_video_info(in_filename):
    probe = get_file_info(in_filename)
    return next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')

# Returns a frame size tuple of type (width, height)
def get_video_frame_size(in_filename):
    video_info = get_video_info(in_filename)
    return video_info['width'], video_info['height']