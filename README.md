# Untitled

# MKV Embedder

MKV Embedder is a simple command-line tool designed to embed additional information into MKV video files and extract it later. The main goal is to allow MKV files to contain more than just video data—now they can hold extra files (currently ZIP attachments) that may contain metadata or supplementary content.

## Features

- **Embed Attachments:** Insert a ZIP file as an attachment into an MKV video.
- **Extract Attachments:** Retrieve the embedded ZIP file from an MKV video.
- **Size Limiting:** Optionally enforce a maximum total size (in MB) for the video and attachment combined.
- **Testing Samples:** The `sample_videos` folder contains small MKV snippets (around 5 seconds each and under 500KB) that you can use for testing or future storage.

## Installation

1. **Clone the Repository:**
    
    ```
    git clone https://github.com/yourusername/mkv_embedder.git
    cd mkv_embedder
    ```
    
2. **Ensure Dependencies:**
    - This tool requires Python 3.
    - The MKV utilities (`mkvmerge.exe`, `mkvextract.exe`, `mkvinfo.exe`) must be present in the `bin` directory. If they are missing, download and place them there.

## Usage

The tool operates via the command line with two main commands: `embed` and `extract`.

### Embedding an Attachment

To embed a ZIP file into an MKV video, run:

```
python mkv_embedder.py embed -i path/to/input.mkv -a path/to/attachment.zip -o path/to/output.mkv -m 50
```

- `i` / `-input`: Path to the input MKV video file.
- `a` / `-attachment`: Path to the ZIP file to embed.
- `o` / `-output`: Path where the output MKV (with the embedded attachment) will be saved.
- `m` / `-max-size`: (Optional) Maximum allowed total size in MB for the combined video and attachment.

### Extracting an Attachment

To extract an embedded attachment from an MKV video, run:

```
python mkv_embedder.py extract -i path/to/input_with_attachment.mkv
```

- `i` / `-input`: Path to the MKV file from which to extract the attachment.

## Notes

- The tool checks if the combined size of the video and the attachment exceeds the provided maximum size (if set) and aborts if it does.
- If the required MKV utilities are not found in the `bin` directory, the tool will exit with an error message.
- Detailed error messages are provided to help diagnose any issues during embedding or extraction.

## License

This project is licensed under the MIT License.