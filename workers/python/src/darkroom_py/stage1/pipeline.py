import hashlib
import io
from pathlib import Path
from PIL import Image, ImageOps
import cv2
import numpy as np
import rawpy



from photoingest.v1.FilterBasicResult_pb2 import FilterBasicResult, Verdict
from photoingest.v1.ResolvedTargetPhotos_pb2 import PhotoTarget
from temporalio.exceptions import ApplicationError
from temporalio import activity


SUPPORTED_FILE_TYPES = frozenset({
    ".jpg", ".jpeg", ".png", ".heic", ".tif", ".tiff", ".webp", ".raf",
})

MIN_DIMENSION = 128
ANALYSIS_SIZE = 1024


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(photo: PhotoTarget) -> FilterBasicResult:
    file_path = Path(photo.directory, photo.name)

    if not file_path.is_file():
        raise ApplicationError(
            f"Resolved file {file_path}, does not exist",
            type="FileNotExist",
            non_retryable=True
        )
    
    result = FilterBasicResult(name = photo.name, directory=photo.directory)

    if file_path.suffix.lower() not in SUPPORTED_FILE_TYPES:
        result.verdict = Verdict.VERDICT_REJECT
        result.reasons.append("Image type not supported")
        return result
    result.content_hash = _sha256(path=file_path)

    try:
        with open_image(file_path) as raw:
           raw.load()
           img = ImageOps.exif_transpose(raw)
    except (OSError, SyntaxError, ValueError, rawpy.LibRawError) as e:
        activity.logger.warn("unreadable image %s, %s", photo.name, e)
        result.verdict = Verdict.VERDICT_REJECT
        return result
    
    result.width, result.height = img.size
    if min(img.size) <= MIN_DIMENSION:
        result.verdict = Verdict.VERDICT_REJECT
        return result
    
    thumb = img.copy()
    thumb.thumbnail((ANALYSIS_SIZE, ANALYSIS_SIZE))

    grey = np.asarray(thumb.convert("L"))

    result.blur_score = float(cv2.Laplacian(grey, cv2.CV_64F).var())
    result.dark_clip_ratio, result.bright_clip_ratio = _clipping_ratios(grey)

    activity.logger.info(
        "%s blur=%.1f dark=%.3f bright=%.3f",
        photo.name, result.blur_score,
        result.dark_clip_ratio, result.bright_clip_ratio,
    )
    return result


@staticmethod
def _clipping_ratios(grey: np.ndarray) -> tuple[float, float]:
    hist = cv2.calcHist([grey], [0], None, [256], [0, 256]).ravel()
    total = grey.size
    return float(hist[0] / total), float(hist[255] / total)

def open_image(path: Path) -> Image.Image:
    if path.suffix.lower() == ".raf":
        with rawpy.imread(str(path)) as raw:
            thumb = raw.extract_thumb()
        if thumb.format == rawpy.ThumbFormat.JPEG:
            img = Image.open(io.BytesIO(thumb.data))
        else:  # uncompressed bitmap preview
            img = Image.fromarray(thumb.data)
    else:
        img = Image.open(path)
    img.load()
    return img