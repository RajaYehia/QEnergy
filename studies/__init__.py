# Copyright (c) 2024 Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path

EXPORT_DIR = Path(__file__).parent.parent / "exports"

BASE_TEXTWIDTH_PT = 472.03123
BASE_TEXTWIDTH_IN = BASE_TEXTWIDTH_PT / 72

FIGSIZE_FULL = (BASE_TEXTWIDTH_IN, BASE_TEXTWIDTH_IN * 9 / 16)
FIGSIZE_HALF = (BASE_TEXTWIDTH_IN / 2, BASE_TEXTWIDTH_IN / 2 * 3 / 4)
