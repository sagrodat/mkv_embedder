import argparse
import subprocess
import os
import sys


def get_exe_path(exe_name):
    """
    Returns the full path to an executable bundled in the 'bin' directory.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(base_dir, "bin", exe_name)
    if not os.path.exists(exe_path):
        sys.exit(f"{exe_name} not found. Make sure it is bundled with the package.")
    return exe_path


def get_mkvmerge_path():
    return get_exe_path("mkvmerge.exe")


def get_mkvextract_path():
    return get_exe_path("mkvextract.exe")


def get_mkvinfo_path():
    return get_exe_path("mkvinfo.exe")


def add_attachment_to_mkv(input_mkv, attachment_path, output_mkv, mime_type="application/zip", max_total_size=None):
    """
    Embeds an attachment into an MKV file using mkvmerge.

    Only .zip file attachments are supported.
    Optionally, if max_total_size (in bytes) is provided, the function checks that the sum of the input video
    and attachment sizes does not exceed that limit.

    Parameters:
      - input_mkv: Path to the input MKV video.
      - attachment_path: Path to the file (e.g., a ZIP file) to attach.
      - output_mkv: Path for the output MKV file.
      - mime_type: MIME type of the attachment (default "application/zip").
      - max_total_size: Optional maximum allowed total size in megabytes.
    """
    # Check total file size if a maximum is provided.
    if max_total_size is not None:
        input_size_mb = os.path.getsize(input_mkv) / (1024 * 1024)
        attachment_size_mb = os.path.getsize(attachment_path) / (1024 * 1024)
        total_size_mb = input_size_mb + attachment_size_mb
        if total_size_mb > max_total_size:
            sys.exit(
                f"Total file size ({total_size_mb:.2f} MB) exceeds the maximum allowed size ({max_total_size} MB). Aborting attachment.")

    mkvmerge_exe = get_mkvmerge_path()
    attachment_name = os.path.basename(attachment_path)

    # Build the mkvmerge command
    command = [
        mkvmerge_exe,
        "-o", output_mkv,
        "--attach-file", attachment_path,
        "--attachment-mime-type", mime_type,
        input_mkv
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Attachment added successfully. Output file: {output_mkv}")
    except subprocess.CalledProcessError as e:
        print("An error occurred while running mkvmerge:", e)


def get_attachment_name_from_mkv(input_mkv):
    """
    Uses mkvinfo to parse the input MKV file and extract the name of the attachment with ID 1
    Returns the attachment file name if found, otherwise exits the program.
    """
    mkvinfo_exe = get_mkvinfo_path()

    try:
        # Force mkvinfo output to English using "--ui-language en"
        result = subprocess.check_output([mkvinfo_exe, "--ui-language", "en", input_mkv],
                                         universal_newlines=True)
    except subprocess.CalledProcessError as e:
        sys.exit("Error running mkvinfo: " + str(e))

    attachment_name = None
    # Look for a line containing "File name:" (that's why English was forced)
    # Example line containing file name :
    # |  + File name: hwi.zip
    for line in result.splitlines():
        line = line.strip()
        if "File name: " in line :
            _, _, potential_name = line.partition(": ") # tuple partition.
            # first not needed -> left of ": "
            # hence second not needed -> just ": "
            # third needed -> right of ": "
            if potential_name.endswith(".zip") : # to make sure
                attachment_name = potential_name

    if attachment_name == None :
        sys.exit("Attachment name not found in the MKV file.")

    print(f"Found attachment with ID 1: {attachment_name}")
    return attachment_name


def extract_attachment_from_mkv(input_mkv):
    """
    Extracts the attachment with ID 1 from the input MKV file.
    The attachment will be saved using its original name (as found by mkvinfo).
    """
    attachment_name = get_attachment_name_from_mkv(input_mkv)
    mkvextract_exe = get_mkvextract_path()

    # Build the mkvextract command:
    # Syntax: mkvextract attachments <input_mkv> 1:<output_filename>
    command = [
        mkvextract_exe,
        "attachments",
        input_mkv,
        f'1:{attachment_name}'
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Attachment extracted successfully as {attachment_name}")
    except subprocess.CalledProcessError as e:
        print("An error occurred while running mkvextract:", e)


def embed_attachment(args):
    # Tutaj wywołujesz funkcję do dołączania załącznika
    # args.input, args.attachment, args.output oraz args.max_size są dostępne
    # Pamiętaj, aby przekonwertować args.max_size, jeśli używasz MB itp.
    add_attachment_to_mkv(
        args.input,
        args.attachment,
        args.output,
        max_total_size=args.max_size
    )

def extract_attachment(args):
    # Tutaj wywołujesz funkcję do ekstrakcji załącznika z pliku MKV
    extract_attachment_from_mkv(args.input)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool for embedding and extracting .ZIP attachments in MKV files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for embedding (attaching)
    embed_parser = subparsers.add_parser("embed", help="Embed a file into an MKV.")
    embed_parser.add_argument(
        "-i", "--input", required=True,
        help="Path to the input MKV video file."
    )
    embed_parser.add_argument(
        "-a", "--attachment", required=True,
        help="Path to the ZIP file to embed."
    )
    embed_parser.add_argument(
        "-o", "--output", required=True,
        help="Path for the output MKV file."
    )
    embed_parser.add_argument(
        "-m", "--max-size", type=float, default=None,
        help="Maximum allowed total size (in MB) for the input video and attachment combined."
    )
    embed_parser.set_defaults(func=embed_attachment)

    # Subparser for extracting
    extract_parser = subparsers.add_parser("extract", help="Extract the attachment from an MKV.")
    extract_parser.add_argument(
        "-i", "--input", required=True,
        help="Path to the MKV file from which to extract the attachment."
    )
    extract_parser.set_defaults(func=extract_attachment)

    args = parser.parse_args()
    args.func(args)