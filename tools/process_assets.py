import os
import sys
import glob
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

TARGET_SIZES = {
    'hero': 1024,
    'bud': 256,
    'petal': 128,
    'default': 512
}

EXPECTED_FILES = [
    'hero.webp',
    'pink-01.webp', 'pink-02.webp', 'pink-03.webp',
    'rose-01.webp', 'rose-02.webp',
    'peach-01.webp', 'peach-02.webp', 'peach-03.webp',
    'mint-01.webp', 'mint-02.webp',
    'blue-01.webp', 'blue-02.webp',
    'ivory-01.webp', 'ivory-02.webp',
    'bud-pink-01.webp', 'bud-coral-01.webp', 'bud-white-01.webp',
    'petal-01.webp', 'petal-02.webp'
]

def get_target_size(stem_name: str) -> int:
    stem_lower = stem_name.lower()
    if stem_lower.startswith('hero'):
        return TARGET_SIZES['hero']
    elif stem_lower.startswith('bud'):
        return TARGET_SIZES['bud']
    elif stem_lower.startswith('petal'):
        return TARGET_SIZES['petal']
    return TARGET_SIZES['default']

def process_single_image(input_path: str, output_path: str, target_size: int):
    # 1. Đọc ảnh RGB
    pil_img = Image.open(input_path).convert('RGB')
    img = np.array(pil_img)
    h, w, _ = img.shape

    # 2. Phân tích màu nền và bóng đổ (shadows)
    # Nền và bóng trên nền xám đều có đặc trưng là xám trung tính (chênh lệch giữa R, G, B rất nhỏ)
    ch_diff = np.max(img, axis=2).astype(np.int32) - np.min(img, axis=2).astype(np.int32)
    brightness = np.mean(img, axis=2)

    # Lấy mẫu màu viền ảnh
    border_pixels = np.concatenate([
        img[0, :], img[-1, :],
        img[:, 0], img[:, -1]
    ], axis=0)
    bg_color = np.median(border_pixels, axis=0)

    # Khoảng cách Euclidean tới màu viền
    diff = img.astype(np.float32) - bg_color
    euc_dist = np.sqrt(np.sum(diff ** 2, axis=2))

    # Pixel được coi là ứng viên nền/bóng đổ nếu:
    # - Rất gần màu viền (euc_dist < 36) HOẶC
    # - Là pixel xám trung tính (ch_diff < 24) có độ sáng từ tối vừa đến xám (25 <= brightness <= 185)
    is_shadow_or_bg = (euc_dist < 36.0) | ((ch_diff < 24) & (brightness >= 25) & (brightness <= 185))

    # 3. Tìm vùng nền liên thông trực tiếp với 4 cạnh viền ngoài (Connected Components)
    num_labels, labels = cv2.connectedComponents(is_shadow_or_bg.astype(np.uint8))
    border_labels = set(np.unique(np.concatenate([
        labels[0, :], labels[-1, :],
        labels[:, 0], labels[:, -1]
    ])))
    if 0 in border_labels:
        border_labels.remove(0)

    outer_bg = np.isin(labels, list(border_labels))
    fg_mask = ~outer_bg

    # 4. Tạo kênh alpha ban đầu
    alpha = np.zeros((h, w), dtype=np.float32)
    alpha[fg_mask] = 1.0

    # 5. Co alpha 1px để khử răng cưa và mép xám thô
    kernel_1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    alpha_eroded = cv2.erode(alpha, kernel_1, iterations=1)

    # 6. Defringe: trong dải 3px sát biên ngoài, xóa mọi pixel xám trung tính
    kernel_3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    dilated_bg = cv2.dilate(outer_bg.astype(np.uint8), kernel_3) > 0
    boundary_zone = dilated_bg & (alpha_eroded > 0)

    # Xóa pixel xám trung tính sát biên (chênh lệch kênh < 24, độ sáng 45-190)
    neutral_grey_edge = boundary_zone & (ch_diff < 24) & (brightness >= 45) & (brightness <= 190)
    alpha_eroded[neutral_grey_edge] = 0.0

    # 7. Khử viền xám (de-fringing) trên màu RGB ở các pixel bán trong suốt sát biên
    cleaned_img = img.astype(np.float32)
    edge_blend = boundary_zone & (alpha_eroded > 0.05) & (alpha_eroded < 0.95)
    if np.any(edge_blend):
        alpha_3d = np.expand_dims(alpha_eroded, axis=2)
        cleaned_img[edge_blend] = np.clip(
            (cleaned_img[edge_blend] - (1.0 - alpha_3d[edge_blend]) * bg_color) / np.maximum(alpha_3d[edge_blend], 0.2),
            0.0, 255.0
        )

    # Làm mượt alpha 1px nhẹ
    alpha_smooth = cv2.GaussianBlur(alpha_eroded, (3, 3), 0.5)
    alpha_smooth[outer_bg] = 0.0
    alpha_smooth = np.clip(alpha_smooth, 0.0, 1.0)

    rgba = np.dstack([cleaned_img.astype(np.uint8), (alpha_smooth * 255).astype(np.uint8)])

    # 8. Cắt sát viền (Trim bounding box) và chừa 3% đệm
    non_zero = np.where(alpha_smooth > 0.05)
    if len(non_zero[0]) == 0:
        print(f"Cảnh báo: không tìm thấy đối tượng trong {input_path}")
        return

    ymin, ymax = np.min(non_zero[0]), np.max(non_zero[0])
    xmin, xmax = np.min(non_zero[1]), np.max(non_zero[1])

    obj_h = ymax - ymin
    obj_w = xmax - xmin
    side = max(obj_h, obj_w)

    pad = int(side * 0.03)
    center_y = (ymin + ymax) // 2
    center_x = (xmin + xmax) // 2
    half_side = (side // 2) + pad

    crop_ymin = center_y - half_side
    crop_ymax = center_y + half_side
    crop_xmin = center_x - half_side
    crop_xmax = center_x + half_side

    crop_size = 2 * half_side
    cropped = np.zeros((crop_size, crop_size, 4), dtype=np.uint8)

    src_ymin = max(0, crop_ymin)
    src_ymax = min(h, crop_ymax)
    src_xmin = max(0, crop_xmin)
    src_xmax = min(w, crop_xmax)

    dst_ymin = src_ymin - crop_ymin
    dst_ymax = dst_ymin + (src_ymax - src_ymin)
    dst_xmin = src_xmin - crop_xmin
    dst_xmax = dst_xmin + (src_xmax - src_xmin)

    cropped[dst_ymin:dst_ymax, dst_xmin:dst_xmax] = rgba[src_ymin:src_ymax, src_xmin:src_xmax]

    # 9. Resize về kích thước cạnh mong muốn (Lanczos)
    out_pil = Image.fromarray(cropped, mode='RGBA')
    out_pil = out_pil.resize((target_size, target_size), Image.Resampling.LANCZOS)

    # 10. Xuất WebP có alpha chất lượng 85
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out_pil.save(output_path, 'WEBP', quality=85, method=6)

def generate_contact_sheet(flower_dir: Path, output_path: Path):
    """Xuất contact-sheet.png hiển thị từng sprite trên nền xanh trời và nền đen để kiểm tra mắt."""
    files = sorted(list(flower_dir.glob('*.webp')))
    if not files:
        return

    cell_size = 256
    cols = 4
    rows = (len(files) + cols - 1) // cols

    sheet_w = cols * (cell_size * 2 + 20) + 40
    sheet_h = rows * (cell_size + 30) + 40

    sheet = Image.new('RGB', (sheet_w, sheet_h), (245, 245, 248))
    sky_col = (169, 214, 240) # Màu nền trời garden.html
    blk_col = (12, 12, 15)    # Nền đen

    for idx, f in enumerate(files):
        r = idx // cols
        c = idx % cols

        im = Image.open(f).convert('RGBA')
        im_thumb = im.resize((cell_size - 12, cell_size - 12), Image.Resampling.LANCZOS)

        base_x = c * (cell_size * 2 + 20) + 20
        base_y = r * (cell_size + 30) + 20

        # Cột nền xanh trời
        sky_box = Image.new('RGB', (cell_size - 12, cell_size - 12), sky_col)
        sky_box.paste(im_thumb, (0, 0), im_thumb)
        sheet.paste(sky_box, (base_x, base_y))

        # Cột nền đen
        blk_box = Image.new('RGB', (cell_size - 12, cell_size - 12), blk_col)
        blk_box.paste(im_thumb, (0, 0), im_thumb)
        sheet.paste(blk_box, (base_x + cell_size - 6, base_y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(str(output_path), 'PNG')
    print(f"[Contact Sheet] Đã lưu: {output_path} ({len(files)} sprites trên nền xanh & đen)")

def run():
    raw_dir = Path('assets/raw')
    out_dir = Path('assets/flowers')
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_files = list(raw_dir.glob('*.png')) + list(raw_dir.glob('*.jpg')) + list(raw_dir.glob('*.jpeg'))
    processed_stems = set()

    print("=== BÁO CÁO XỬ LÝ ẢNH (PROCESS ASSETS) ===")
    if not raw_files:
        print(f"Chưa tìm thấy ảnh gốc trong thư mục {raw_dir}")
    else:
        for rf in raw_files:
            stem = rf.stem
            target_size = get_target_size(stem)
            out_file = out_dir / f"{stem}.webp"
            try:
                process_single_image(str(rf), str(out_file), target_size)
                processed_stems.add(f"{stem}.webp")
                kb_size = out_file.stat().st_size / 1024
                print(f"[OK] {rf.name} -> {out_file.name} ({target_size}x{target_size}, {kb_size:.1f} KB)")
            except Exception as e:
                print(f"[ERR] Không thể xử lý {rf.name}: {e}")

    # Kiểm tra danh sách file mong muốn
    print("\n--- KIỂM TRA TÀI NGUYÊN assets/flowers/ ---")
    existing_files = set(f.name for f in out_dir.glob('*.webp'))
    missing = []
    total_size = 0

    for exp in EXPECTED_FILES:
        if exp in existing_files:
            sz = (out_dir / exp).stat().st_size
            total_size += sz
            print(f"  [x] {exp:18} ({sz/1024:.1f} KB)")
        else:
            missing.append(exp)
            print(f"  [ ] {exp:18} (CHƯA CÓ)")

    print(f"\nTổng dung lượng hiện có: {total_size/1024:.1f} KB")
    if missing:
        print(f"Còn thiếu {len(missing)}/{len(EXPECTED_FILES)} ảnh. Trang web sẽ dùng sprite dự phòng cho các ảnh thiếu.")
    else:
        print("TẤT CẢ TÀI NGUYÊN ĐÃ ĐẦY ĐỦ!")

    # Tự động xuất contact-sheet.png vào assets/debug/ để kiểm tra trực quan
    generate_contact_sheet(out_dir, Path('assets/debug/contact-sheet.png'))

if __name__ == '__main__':
    run()
