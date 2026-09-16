from typing import List


class ColorAgentTools:
    @staticmethod
    def generate_palette(base_hex: str) -> List[str]:
        # Simple rule-based complementary & analogous palette builder
        # Input e.g. '#3A86C8'
        hex_clean = base_hex.lstrip("#")
        r, g, b = tuple(int(hex_clean[i : i + 2], 16) for i in (0, 2, 4))

        # 1. Complementary color
        comp_r, comp_g, comp_b = 255 - r, 255 - g, 255 - b

        # 2. Analogous shifts
        sh1_r, sh1_g, sh1_b = (
            min(255, int(r * 1.2)),
            min(255, int(g * 0.8)),
            min(255, int(b * 0.9)),
        )
        sh2_r, sh2_g, sh2_b = (
            min(255, int(r * 0.8)),
            min(255, int(g * 1.2)),
            min(255, int(b * 1.1)),
        )

        def to_hex(rgb):
            return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

        return [
            base_hex,
            to_hex((comp_r, comp_g, comp_b)),
            to_hex((sh1_r, sh1_g, sh1_b)),
            to_hex((sh2_r, sh2_g, sh2_b)),
        ]

    @staticmethod
    def get_color_psychology(hex_code: str) -> str:
        # Rules mapping colors to mood associations
        if "ff" in hex_code.lower()[:3]:
            return "Energizing and warm, best for dining spaces or active zones."
        if "00" in hex_code.lower()[-3:]:
            return "Calming, promotes productivity and stability, best for study zones."
        return "Neutral harmony, matches modern minimalistic layouts."
