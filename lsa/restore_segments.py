import csv
import json
import os
import re

from config import resources
from tools.fsys import files
from tools.text import remove_strong, remove_br, remove_li, remove_ul, remove_spaces, remove_newlines, \
    remove_spec_chars, trim


def find_any_positive_index(struct: dict):
    for s in struct.values():
        if s["endIndexInSegment"] > s["startIndexInSegment"] > 0:
            return s["selectedText"], s["startIndexInSegment"], s["endIndexInSegment"]
    return "", -1, -1


def clear_segments(segments, text):
    for s in segments:
        s["segment_text"] = clear_segment(text, s["start_pos"], s["end_pos"])

    return segments


def clear_segment(text, start, end):
    segment_text = text.strip()
    segment_text = segment_text[start : end]
    segment_text = remove_strong(segment_text)
    segment_text = remove_br(segment_text)
    segment_text = remove_li(segment_text)
    segment_text = remove_ul(segment_text)
    segment_text = remove_spec_chars(segment_text)
    segment_text = remove_spaces(segment_text)
    segment_text = remove_newlines(segment_text)
    segment_text = remove_spaces(segment_text)
    return segment_text


def filter_positions(segments):
    return [s for s in segments if (0 < s["start_pos"] < s["end_pos"])]


def filter_coordinates(segments):
    return [s for s in segments if (0 < s["coordinates"][1] < s["coordinates"][2])]


def assign_positions(segments, text):

    segments[0]["start_pos"] = 0
    for i in range(1, len(segments)):
        try:
            segments[i]["start_pos"] = text.index(f"{segments[i]['coordinates'][0]}") \
                                       - segments[i]['coordinates'][1] - 1
        except ValueError:
            segments[i]["start_pos"] = -1

    for i in range(len(segments) - 1):
        try:
            segments[i]["end_pos"] = segments[i + 1]["start_pos"] + 1
        except ValueError:
            segments[i]["end_pos"] = -1
    segments[-1]["end_pos"] = len(text)

    return segments


def split_segments(segments):
    for s in segments:
        s["paragraphs"] = s["segment_text"].split("\n")

    return segments


def make_segments(annotations_records):
    segments_dict = {
        int(a["segment_id"]): {
            "file_id": a["file_id"],
            "category": a["category"],
            "segment_id": a["segment_id"],
            "coordinates": a["coordinates"]
        }
        for a in annotations_records
    }

    return list(segments_dict.values())


def make_annotations(reader, file):
    return [
        {
            "id": int(rows[0]),
            "file_id": int(re.match(r"^(\d+)_.*", os.path.basename(file[1])).group(1)),
            "policy_id": int(rows[3]),
            "segment_id": int(rows[4]),
            "category": rows[5],
            "coordinates": find_any_positive_index(json.loads(rows[6])),
        }
        for rows in reader
    ]


def restore_segments():
    fs = list(zip(files("datasets/OPP-115/sanitized_policies", r"(\d+)_.*"),
                  files("datasets/OPP-115/annotations", r"(\d+)_.*")))

    all_annotations = []
    all_segments = []

    for f in fs:

        with open(f[0], mode="r") as sanitized:
            text = "\n".join(sanitized.readlines())

        with open(f[1], mode="r") as annotations:
            reader = csv.reader(annotations)
            annotations_records = make_annotations(reader, f)
            all_annotations.extend(annotations_records)

        segments = make_segments(annotations_records)
        segments = filter_coordinates(segments)
        segments = assign_positions(segments, text)
        segments = filter_positions(segments)
        segments = clear_segments(segments, text)
        all_segments.extend(segments)

    all_segments = split_segments(all_segments)

    with open(os.path.join(resources, "all_segments.json"), "w") as f:
        json.dump(all_segments, f, indent=4, sort_keys=True)

    with open(os.path.join(resources, "all_annotations.json"), "w") as f:
        json.dump(all_annotations, f, indent=4, sort_keys=True)
