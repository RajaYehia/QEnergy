# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path

EXPORT_DIR = Path(__file__).parent.parent / "exports"

FULL_TEXTWIDTH_PT = 510
COLUMNWIDTH_PT = 246

BASE_TEXTWIDTH_IN = FULL_TEXTWIDTH_PT / 72
COLUMNWIDTH_IN = COLUMNWIDTH_PT / 72

FIGSIZE_FULL = (BASE_TEXTWIDTH_IN, BASE_TEXTWIDTH_IN * 9 / 16)
FIGSIZE_HALF = (COLUMNWIDTH_IN, COLUMNWIDTH_IN * 3 / 4)
